"""Create a small connected KebabDEL graph without overwriting existing data."""
from django.core.management.base import BaseCommand
from django.db import transaction
from main.models import (
    Pelanggan, Outlet, Koki, AlamatDelivery, Menu, MenuOutlet,
    Pesanan, DetailPesanan, Pembayaran,
)


def seed_demo():
    created = 0

    def ensure(model, lookup, **defaults):
        nonlocal created
        obj, new = model.objects.get_or_create(**lookup, defaults=defaults)
        created += new
        return obj

    pelanggan = ensure(Pelanggan, {'id_pengguna': 9001}, nama_lengkap='Pelanggan Demo', nomor_telepon='080000009001', email='demo@example.test')
    outlet = ensure(Outlet, {'id_outlet': 9001}, nama_outlet='Baba Tomi Demo', lokasi_outlet='Depok')
    koki = ensure(Koki, {'id_pengguna': 9002}, nama_lengkap='Koki Demo', nomor_telepon='080000009002', nip_koki='KOKI-DEMO-01', outlet=outlet)
    alamat = ensure(AlamatDelivery, {'id_alamat': 9001}, detail_alamat='Jl. Contoh No. 1, Depok', pelanggan=pelanggan)
    menu = ensure(Menu, {'id_menu': 9001}, nama_menu='Kebab Sapi Demo', harga_dasar=25000, deskripsi='Data fiktif demonstrasi')
    ensure(MenuOutlet, {'outlet': outlet, 'menu': menu}, status_tersedia=True)
    pesanan = ensure(Pesanan, {'pelanggan': pelanggan}, id_pesanan=9001, jenis_layanan='delivery', status_pesanan='diproses', total_harga=50000, outlet=outlet, koki=koki, alamat_delivery=alamat)
    ensure(DetailPesanan, {'pesanan': pesanan, 'menu': menu}, kuantitas=2, sub_total=50000)
    ensure(Pembayaran, {'pesanan': pesanan}, id_pembayaran=9001, metode_bayar='OVO (simulasi)', status_bayar='sukses')
    return created


class Command(BaseCommand):
    help = 'Tambahkan contoh data berelasi sesuai diagram; data lama tidak ditimpa.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'{seed_demo()} data demo ditambahkan.'))
