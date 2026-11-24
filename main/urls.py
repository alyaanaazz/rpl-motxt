"""
This code is generated using MoTxT,
checkout more about us on https://motxt.ppl.cs.ui.ac.id
"""

from django.urls import path
from .views import (
    landing_page,
    dashboard,
    create_pelanggan,
    get_pelanggan,
    edit_pelanggan,
    delete_pelanggan,create_alamat_delivery,
    get_alamat_delivery,
    edit_alamat_delivery,
    delete_alamat_delivery,create_outlet,
    get_outlet,
    edit_outlet,
    delete_outlet,create_koki,
    get_koki,
    edit_koki,
    delete_koki,create_kurir,
    get_kurir,
    edit_kurir,
    delete_kurir,create_menu,
    get_menu,
    edit_menu,
    delete_menu,create_pesanan,
    get_pesanan,
    edit_pesanan,
    delete_pesanan,create_detail_pesanan,
    get_detail_pesanan,
    edit_detail_pesanan,
    delete_detail_pesanan,create_pembayaran,
    get_pembayaran,
    edit_pembayaran,
    delete_pembayaran,create_nota_pesanan,
    get_nota_pesanan,
    edit_nota_pesanan,
    delete_nota_pesanan,create_pengingat,
    get_pengingat,
    edit_pengingat,
    delete_pengingat,create_kupon_diskon,
    get_kupon_diskon,
    edit_kupon_diskon,
    delete_kupon_diskon,
)

app_name = "main"

urlpatterns = [
    path('', landing_page , name="landing_page"),
    path('dashboard/', dashboard, name="dashboard"),
    # Path for Pelanggan
    path('create-pelanggan/', create_pelanggan, name="create_pelanggan"),
    path('get-all-pelanggan/', get_pelanggan, name="get_pelanggan"),
    path('edit-pelanggan/<int:id>/', edit_pelanggan, name="edit_pelanggan"),
    path('delete-pelanggan/', delete_pelanggan, name="delete_pelanggan"),
    
    # Path for AlamatDelivery
    path('create-alamat_delivery/', create_alamat_delivery, name="create_alamat_delivery"),
    path('get-all-alamat_delivery/', get_alamat_delivery, name="get_alamat_delivery"),
    path('edit-alamat_delivery/<int:id>/', edit_alamat_delivery, name="edit_alamat_delivery"),
    path('delete-alamat_delivery/', delete_alamat_delivery, name="delete_alamat_delivery"),
    
    # Path for Outlet
    path('create-outlet/', create_outlet, name="create_outlet"),
    path('get-all-outlet/', get_outlet, name="get_outlet"),
    path('edit-outlet/<int:id>/', edit_outlet, name="edit_outlet"),
    path('delete-outlet/', delete_outlet, name="delete_outlet"),
    
    # Path for Koki
    path('create-koki/', create_koki, name="create_koki"),
    path('get-all-koki/', get_koki, name="get_koki"),
    path('edit-koki/<int:id>/', edit_koki, name="edit_koki"),
    path('delete-koki/', delete_koki, name="delete_koki"),
    
    # Path for Kurir
    path('create-kurir/', create_kurir, name="create_kurir"),
    path('get-all-kurir/', get_kurir, name="get_kurir"),
    path('edit-kurir/<int:id>/', edit_kurir, name="edit_kurir"),
    path('delete-kurir/', delete_kurir, name="delete_kurir"),
    
    # Path for Menu
    path('create-menu/', create_menu, name="create_menu"),
    path('get-all-menu/', get_menu, name="get_menu"),
    path('edit-menu/<int:id>/', edit_menu, name="edit_menu"),
    path('delete-menu/', delete_menu, name="delete_menu"),
    
    # Path for Pesanan
    path('create-pesanan/', create_pesanan, name="create_pesanan"),
    path('get-all-pesanan/', get_pesanan, name="get_pesanan"),
    path('edit-pesanan/<int:id>/', edit_pesanan, name="edit_pesanan"),
    path('delete-pesanan/', delete_pesanan, name="delete_pesanan"),
    
    # Path for DetailPesanan
    path('create-detail_pesanan/', create_detail_pesanan, name="create_detail_pesanan"),
    path('get-all-detail_pesanan/', get_detail_pesanan, name="get_detail_pesanan"),
    path('edit-detail_pesanan/<int:id>/', edit_detail_pesanan, name="edit_detail_pesanan"),
    path('delete-detail_pesanan/', delete_detail_pesanan, name="delete_detail_pesanan"),
    
    # Path for Pembayaran
    path('create-pembayaran/', create_pembayaran, name="create_pembayaran"),
    path('get-all-pembayaran/', get_pembayaran, name="get_pembayaran"),
    path('edit-pembayaran/<int:id>/', edit_pembayaran, name="edit_pembayaran"),
    path('delete-pembayaran/', delete_pembayaran, name="delete_pembayaran"),
    
    # Path for NotaPesanan
    path('create-nota_pesanan/', create_nota_pesanan, name="create_nota_pesanan"),
    path('get-all-nota_pesanan/', get_nota_pesanan, name="get_nota_pesanan"),
    path('edit-nota_pesanan/<int:id>/', edit_nota_pesanan, name="edit_nota_pesanan"),
    path('delete-nota_pesanan/', delete_nota_pesanan, name="delete_nota_pesanan"),
    
    # Path for Pengingat
    path('create-pengingat/', create_pengingat, name="create_pengingat"),
    path('get-all-pengingat/', get_pengingat, name="get_pengingat"),
    path('edit-pengingat/<int:id>/', edit_pengingat, name="edit_pengingat"),
    path('delete-pengingat/', delete_pengingat, name="delete_pengingat"),
    
    # Path for KuponDiskon
    path('create-kupon_diskon/', create_kupon_diskon, name="create_kupon_diskon"),
    path('get-all-kupon_diskon/', get_kupon_diskon, name="get_kupon_diskon"),
    path('edit-kupon_diskon/<int:id>/', edit_kupon_diskon, name="edit_kupon_diskon"),
    path('delete-kupon_diskon/', delete_kupon_diskon, name="delete_kupon_diskon"),
    
]

