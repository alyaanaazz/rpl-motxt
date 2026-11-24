from django.db import models
from django.utils import timezone


class Pelanggan(models.Model):
    id_pelanggan = models.IntegerField()
    nama = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=255)
    
    pass

class AlamatDelivery(models.Model):
    id_alamat = models.IntegerField()
    alamat_lengkap = models.CharField(max_length=255)
    catatan = models.CharField(max_length=255)
    
    pass

class Outlet(models.Model):
    id_outlet = models.IntegerField()
    nama_outlet = models.CharField(max_length=255)
    daerah = models.CharField(max_length=255)
    alamat_outlet = models.CharField(max_length=255)
    
    pass

class Koki(models.Model):
    id_koki = models.IntegerField()
    nama_koki = models.CharField(max_length=255)
    
    pass

class Kurir(models.Model):
    id_kurir = models.IntegerField()
    nama_kurir = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=255)
    
    pass

class Menu(models.Model):
    id_menu = models.IntegerField()
    nama_menu = models.CharField(max_length=255)
    jenis_kebab = models.CharField(max_length=255)
    harga = models.IntegerField()
    tersedia = models.BooleanField(default=False)
    
    pass

class Pesanan(models.Model):
    id_pesanan = models.IntegerField()
    tanggal_pesanan = models.DateTimeField(default=timezone.now, null=True, blank=True)
    metode_layanan = models.CharField(max_length=255)
    status_pesanan = models.CharField(max_length=255)
    total_harga = models.IntegerField()
    
    pass

class DetailPesanan(models.Model):
    id_detail = models.IntegerField()
    jumlah = models.IntegerField()
    subtotal = models.IntegerField()
    
    pass

class Pembayaran(models.Model):
    id_pembayaran = models.IntegerField()
    metode = models.CharField(max_length=255)
    status_transaksi = models.CharField(max_length=255)
    waktu_bayar = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    pass

class NotaPesanan(models.Model):
    id_nota = models.IntegerField()
    jumlah_pesanan = models.IntegerField()
    file_jpg = models.CharField(max_length=255)
    
    pass

class Pengingat(models.Model):
    id_pengingat = models.IntegerField()
    durasi_pengulangan = models.CharField(max_length=255)
    daftar_pembelian = models.CharField(max_length=255)
    is_aktif = models.BooleanField(default=False)
    
    pass

class KuponDiskon(models.Model):
    id_kupon = models.IntegerField()
    kode_kupon = models.CharField(max_length=255)
    potongan_harga = models.IntegerField()
    
    pass

