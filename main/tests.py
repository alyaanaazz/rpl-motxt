from io import StringIO

from django.core.management import call_command
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.forms.models import model_to_dict
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from .entities import ENTITIES
from .management.commands.seed_demo import seed_demo
from .models import (
    Pengguna, Pelanggan, Outlet, Koki, AlamatDelivery, Menu, MenuOutlet,
    Pesanan, DetailPesanan, Pembayaran,
)


class DiagramTests(TestCase):
    def setUp(self):
        seed_demo()
        self.outlet = Outlet.objects.get(id_outlet=9001)
        self.pelanggan = Pelanggan.objects.get(id_pengguna=9001)
        self.pesanan = Pesanan.objects.get(id_pesanan=9001)
        self.menu = Menu.objects.get(id_menu=9001)

    def url(self, action, key, *args):
        return reverse(f'main:{action}_{key}', args=args)

    def test_abstract_inheritance_and_entity_set(self):
        self.assertTrue(Pengguna._meta.abstract)
        self.assertTrue(issubclass(Pelanggan, Pengguna))
        self.assertTrue(issubclass(Koki, Pengguna))
        self.assertEqual(len(ENTITIES), 9)
        self.assertNotIn('main_pengguna', connection.introspection.table_names())
        self.assertNotIn('kurir', ENTITIES)

    def test_all_pages_and_foreign_key_prefills(self):
        for page in ('landing_page', 'dashboard'):
            self.assertEqual(self.client.get(reverse(f'main:{page}')).status_code, 200)
        for key, entity in ENTITIES.items():
            obj = entity.model.objects.first()
            with self.subTest(entity=key):
                self.assertEqual(self.client.get(self.url('get', key)).status_code, 200)
                self.assertEqual(self.client.get(self.url('create', key)).status_code, 200)
                response = self.client.get(self.url('edit', key, obj.pk))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['form'].instance.pk, obj.pk)
                for field in entity.model._meta.fields:
                    if field.is_relation:
                        self.assertContains(response, f'value="{getattr(obj, field.attname)}" selected')

    def test_crud_for_every_concrete_entity(self):
        fresh_customer = Pelanggan.objects.create(id_pengguna=9900, nama_lengkap='Extra', nomor_telepon='0800000000', email='extra@example.test')
        fresh_order = Pesanan.objects.create(id_pesanan=9900, pelanggan=fresh_customer, outlet=self.outlet, jenis_layanan='pickup', status_pesanan='baru', total_harga=25000)
        fresh_menu = Menu.objects.create(id_menu=9900, nama_menu='Extra', harga_dasar=25000, deskripsi='Extra')
        MenuOutlet.objects.create(outlet=self.outlet, menu=fresh_menu, status_tersedia=True)
        fresh_outlet = Outlet.objects.create(id_outlet=9900, nama_outlet='Extra', lokasi_outlet='Bogor')
        order_customer = Pelanggan.objects.create(id_pengguna=9901, nama_lengkap='Order Customer', nomor_telepon='0800000000', email='order@example.test')
        overrides = {
            'pelanggan': {'id_pengguna': 9991, 'email': 'new@example.test'},
            'koki': {'id_pengguna': 9992}, 'outlet': {'id_outlet': 9991},
            'alamat_delivery': {'id_alamat': 9991}, 'menu': {'id_menu': 9991},
            'menu_outlet': {'outlet': fresh_outlet.pk},
            'pesanan': {'id_pesanan': 9991, 'pelanggan': order_customer.pk, 'alamat_delivery': '', 'koki': ''},
            'detail_pesanan': {'menu': fresh_menu.pk},
            'pembayaran': {'id_pembayaran': 9991, 'pesanan': fresh_order.pk},
        }
        for key, entity in ENTITIES.items():
            with self.subTest(entity=key):
                original = entity.model.objects.order_by('pk').first()
                payload = model_to_dict(original, exclude=['id', 'menu'] if key in ('outlet', 'pesanan') else ['id'])
                for name, value in list(payload.items()):
                    if hasattr(value, 'strftime'):
                        payload[name] = value.isoformat()
                payload.update(overrides[key])
                old_ids = set(entity.model.objects.values_list('pk', flat=True))
                response = self.client.post(self.url('create', key), payload)
                self.assertEqual(response.status_code, 302, response.context['form'].errors if response.status_code == 200 else '')
                obj = entity.model.objects.exclude(pk__in=old_ids).get()
                if key == 'menu_outlet':
                    payload['status_tersedia'] = False
                elif key == 'detail_pesanan':
                    payload['kuantitas'] = 3
                else:
                    field = next(f for f in entity.model._meta.fields if f.get_internal_type() in ('CharField', 'EmailField'))
                    payload[field.name] = 'updated@example.test' if field.get_internal_type() == 'EmailField' else 'Updated demo'
                response = self.client.post(self.url('edit', key, obj.pk), payload)
                self.assertEqual(response.status_code, 302)
                obj.refresh_from_db()
                if key == 'menu_outlet':
                    self.assertFalse(obj.status_tersedia)
                elif key == 'detail_pesanan':
                    self.assertEqual(obj.kuantitas, 3)
                self.assertEqual(self.client.post(self.url('delete', key), {'object_id': obj.pk}).status_code, 302)
                self.assertFalse(entity.model.objects.filter(pk=obj.pk).exists())

    def test_invalid_input_and_missing_objects(self):
        for key, entity in ENTITIES.items():
            with self.subTest(entity=key):
                before = entity.model.objects.count()
                response = self.client.post(self.url('create', key), {})
                # A standalone BooleanField may be unchecked, but the through FKs are required.
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertEqual(entity.model.objects.count(), before)
                self.assertEqual(self.client.get(self.url('edit', key, 999999)).status_code, 404)
                self.assertEqual(self.client.get(self.url('delete', key)).status_code, 405)
                self.assertEqual(self.client.post(self.url('delete', key), {'object_id': 'abc'}).status_code, 400)
                self.assertEqual(self.client.post(self.url('delete', key), {'object_id': 999999}).status_code, 404)

    def test_one_customer_one_order_and_one_payment(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Pesanan.objects.create(id_pesanan=9999, pelanggan=self.pelanggan, outlet=self.outlet, jenis_layanan='pickup', status_pesanan='baru', total_harga=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Pembayaran.objects.create(id_pembayaran=9999, pesanan=self.pesanan, metode_bayar='demo', status_bayar='demo')

    def test_association_class_attributes_and_pair_uniqueness(self):
        self.assertEqual(self.outlet.menu.get(), self.menu)
        self.assertEqual(self.pesanan.menu.get(), self.menu)
        self.assertTrue(MenuOutlet.objects.get().status_tersedia)
        self.assertEqual(DetailPesanan.objects.get().kuantitas, 2)
        self.assertEqual(DetailPesanan.objects.get().sub_total, 50000)
        for model, values in (
            (MenuOutlet, {'outlet': self.outlet, 'menu': self.menu}),
            (DetailPesanan, {'pesanan': self.pesanan, 'menu': self.menu, 'kuantitas': 1, 'sub_total': 25000}),
        ):
            with self.subTest(model=model), self.assertRaises(IntegrityError), transaction.atomic():
                model.objects.create(**values)

    def test_optional_address_and_cook(self):
        customer = Pelanggan.objects.create(id_pengguna=9999, nama_lengkap='Pickup', nomor_telepon='0800000000', email='pickup@example.test')
        response = self.client.post(self.url('create', 'pesanan'), {
            'id_pesanan': 9999, 'pelanggan': customer.pk, 'outlet': self.outlet.pk,
            'jenis_layanan': 'pickup', 'status_pesanan': 'baru', 'total_harga': 25000,
            'waktu_pesan': '2026-11-24 15:00:00',
        })
        self.assertEqual(response.status_code, 302)
        order = Pesanan.objects.get(id_pesanan=9999)
        self.assertIsNone(order.alamat_delivery)
        self.assertIsNone(order.koki)

    def test_composition_and_protected_delete(self):
        response = self.client.post(self.url('delete', 'outlet'), {'object_id': self.outlet.pk})
        self.assertEqual(response.status_code, 409)
        self.assertContains(response, 'Data masih dipakai', status_code=409)
        self.pesanan.delete()
        self.assertFalse(Pembayaran.objects.exists())
        self.assertFalse(DetailPesanan.objects.exists())
        self.pelanggan.delete()
        self.assertFalse(AlamatDelivery.objects.exists())

    def test_csrf_and_idempotent_seed(self):
        self.assertEqual(Client(enforce_csrf_checks=True).post(self.url('delete', 'menu'), {'object_id': self.menu.pk}).status_code, 403)
        self.pelanggan.nama_lengkap = 'Existing name'
        self.pelanggan.save()
        call_command('seed_demo', stdout=StringIO())
        call_command('seed_demo', stdout=StringIO())
        self.pelanggan.refresh_from_db()
        self.assertEqual(self.pelanggan.nama_lengkap, 'Existing name')
        for entity in ENTITIES.values():
            self.assertEqual(entity.model.objects.count(), 1)

    def test_form_validates_association_data(self):
        form = ENTITIES['detail_pesanan'].form(data={
            'pesanan': self.pesanan.pk, 'menu': self.menu.pk, 'kuantitas': 0, 'sub_total': 0,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('kuantitas', form.errors)


class LegacyMigrationTests(TransactionTestCase):
    def test_existing_scalar_data_is_archived(self):
        executor = MigrationExecutor(connection)
        old_target = [('main', '0001_initial')]
        new_target = [('main', '0003_diagram_kebabdel')]
        try:
            executor.migrate(old_target)
            old_apps = executor.loader.project_state(old_target).apps
            old_apps.get_model('main', 'Pelanggan').objects.create(id_pelanggan=8123, nama='Preserved legacy', no_hp='0800000000')
            executor = MigrationExecutor(connection)
            executor.migrate(new_target)
            with connection.cursor() as cursor:
                cursor.execute('SELECT nama FROM legacy_main_pelanggan WHERE id_pelanggan = %s', [8123])
                self.assertEqual(cursor.fetchone()[0], 'Preserved legacy')
            self.assertEqual(Pelanggan.objects.count(), 0)
        finally:
            MigrationExecutor(connection).migrate(new_target)
