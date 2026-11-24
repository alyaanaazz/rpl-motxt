"""Django mapping of diagrams/KebabDEL.uml, corrected after MoTxT generation.

See docs/eksperimen-motxt.md for the raw generator findings and manual changes.
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Pengguna(models.Model):
    id_pengguna = models.IntegerField(unique=True)
    nama_lengkap = models.CharField(max_length=255)
    nomor_telepon = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nama_lengkap} ({self.id_pengguna})"


class Pelanggan(Pengguna):
    email = models.EmailField(max_length=255)


class Outlet(models.Model):
    id_outlet = models.IntegerField(unique=True)
    nama_outlet = models.CharField(max_length=255)
    lokasi_outlet = models.CharField(max_length=255)
    menu = models.ManyToManyField('Menu', through='MenuOutlet', related_name='outlet')

    def __str__(self):
        return self.nama_outlet


class Koki(Pengguna):
    nip_koki = models.CharField(max_length=255)
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name='koki')


class AlamatDelivery(models.Model):
    id_alamat = models.IntegerField(unique=True)
    detail_alamat = models.CharField(max_length=255)
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE, related_name='alamat_delivery')

    def __str__(self):
        return self.detail_alamat


class Menu(models.Model):
    id_menu = models.IntegerField(unique=True)
    nama_menu = models.CharField(max_length=255)
    harga_dasar = models.PositiveIntegerField()
    deskripsi = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_menu


class Pesanan(models.Model):
    id_pesanan = models.IntegerField(unique=True)
    waktu_pesan = models.DateTimeField(default=timezone.now)
    jenis_layanan = models.CharField(max_length=255)
    status_pesanan = models.CharField(max_length=255)
    total_harga = models.PositiveIntegerField()
    # The diagram and the user's confirmation specify 1:1, not 1:N.
    pelanggan = models.OneToOneField(Pelanggan, on_delete=models.PROTECT, related_name='pesanan')
    koki = models.ForeignKey(Koki, on_delete=models.SET_NULL, null=True, blank=True, related_name='pesanan')
    outlet = models.ForeignKey(Outlet, on_delete=models.PROTECT, related_name='pesanan')
    alamat_delivery = models.ForeignKey(AlamatDelivery, on_delete=models.SET_NULL, null=True, blank=True, related_name='pesanan')
    menu = models.ManyToManyField(Menu, through='DetailPesanan', related_name='pesanan')

    def __str__(self):
        return f"Pesanan {self.id_pesanan}"


class Pembayaran(models.Model):
    id_pembayaran = models.IntegerField(unique=True)
    waktu_bayar = models.DateTimeField(default=timezone.now)
    metode_bayar = models.CharField(max_length=255)
    status_bayar = models.CharField(max_length=255)
    pesanan = models.OneToOneField(Pesanan, on_delete=models.CASCADE, related_name='pembayaran')

    def __str__(self):
        return f"Pembayaran {self.id_pembayaran}"


class DetailPesanan(models.Model):
    pesanan = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='detail_pesanan')
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, related_name='detail_pesanan')
    kuantitas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    sub_total = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['pesanan', 'menu'], name='unique_detail_pesanan_menu')]

    def __str__(self):
        return f"{self.pesanan} - {self.menu}"


class MenuOutlet(models.Model):
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, related_name='menu_outlet')
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, related_name='menu_outlet')
    status_tersedia = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['outlet', 'menu'], name='unique_menu_outlet')]

    def __str__(self):
        return f"{self.outlet} - {self.menu}"
