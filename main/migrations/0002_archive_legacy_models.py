"""Keep the old scalar-only data in legacy tables before applying the diagram.

There is no reliable way to infer the missing associations from the old data.
No old rows are deleted or guessed into the new relational model.
"""
from django.db import migrations


LEGACY_MODELS = (
    'Pelanggan', 'AlamatDelivery', 'Outlet', 'Koki', 'Kurir', 'Menu',
    'Pesanan', 'DetailPesanan', 'Pembayaran', 'NotaPesanan', 'Pengingat', 'KuponDiskon',
)


class Migration(migrations.Migration):
    dependencies = [('main', '0001_initial')]
    operations = [
        migrations.AlterModelTable(name=name, table=f'legacy_main_{name.lower()}')
        for name in LEGACY_MODELS
    ] + [
        migrations.SeparateDatabaseAndState(
            state_operations=[migrations.DeleteModel(name=name) for name in LEGACY_MODELS],
            database_operations=[],
        )
    ]
