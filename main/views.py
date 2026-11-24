from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from django.apps import apps
from django.utils import timezone
from datetime import datetime


def landing_page(request):

    model_info = {}
    model_info["pelanggan"] = "Pelanggan"
    model_info["alamat_delivery"] = "Alamatdelivery"
    model_info["outlet"] = "Outlet"
    model_info["koki"] = "Koki"
    model_info["kurir"] = "Kurir"
    model_info["menu"] = "Menu"
    model_info["pesanan"] = "Pesanan"
    model_info["detail_pesanan"] = "Detailpesanan"
    model_info["pembayaran"] = "Pembayaran"
    model_info["nota_pesanan"] = "Notapesanan"
    model_info["pengingat"] = "Pengingat"
    model_info["kupon_diskon"] = "Kupondiskon"
    

    return render(request, 'landing_page.html', {'model_info': model_info})

def dashboard(request):
    entity_cards = [
        {
            'label': 'Pelanggan',
            'count': Pelanggan.objects.count(),
            'list_url': 'main:get_pelanggan',
            'create_url': 'main:create_pelanggan',
            'fields': [field.name for field in Pelanggan._meta.get_fields()],
        }
,
        {
            'label': 'AlamatDelivery',
            'count': AlamatDelivery.objects.count(),
            'list_url': 'main:get_alamat_delivery',
            'create_url': 'main:create_alamat_delivery',
            'fields': [field.name for field in AlamatDelivery._meta.get_fields()],
        }
,
        {
            'label': 'Outlet',
            'count': Outlet.objects.count(),
            'list_url': 'main:get_outlet',
            'create_url': 'main:create_outlet',
            'fields': [field.name for field in Outlet._meta.get_fields()],
        }
,
        {
            'label': 'Koki',
            'count': Koki.objects.count(),
            'list_url': 'main:get_koki',
            'create_url': 'main:create_koki',
            'fields': [field.name for field in Koki._meta.get_fields()],
        }
,
        {
            'label': 'Kurir',
            'count': Kurir.objects.count(),
            'list_url': 'main:get_kurir',
            'create_url': 'main:create_kurir',
            'fields': [field.name for field in Kurir._meta.get_fields()],
        }
,
        {
            'label': 'Menu',
            'count': Menu.objects.count(),
            'list_url': 'main:get_menu',
            'create_url': 'main:create_menu',
            'fields': [field.name for field in Menu._meta.get_fields()],
        }
,
        {
            'label': 'Pesanan',
            'count': Pesanan.objects.count(),
            'list_url': 'main:get_pesanan',
            'create_url': 'main:create_pesanan',
            'fields': [field.name for field in Pesanan._meta.get_fields()],
        }
,
        {
            'label': 'DetailPesanan',
            'count': DetailPesanan.objects.count(),
            'list_url': 'main:get_detail_pesanan',
            'create_url': 'main:create_detail_pesanan',
            'fields': [field.name for field in DetailPesanan._meta.get_fields()],
        }
,
        {
            'label': 'Pembayaran',
            'count': Pembayaran.objects.count(),
            'list_url': 'main:get_pembayaran',
            'create_url': 'main:create_pembayaran',
            'fields': [field.name for field in Pembayaran._meta.get_fields()],
        }
,
        {
            'label': 'NotaPesanan',
            'count': NotaPesanan.objects.count(),
            'list_url': 'main:get_nota_pesanan',
            'create_url': 'main:create_nota_pesanan',
            'fields': [field.name for field in NotaPesanan._meta.get_fields()],
        }
,
        {
            'label': 'Pengingat',
            'count': Pengingat.objects.count(),
            'list_url': 'main:get_pengingat',
            'create_url': 'main:create_pengingat',
            'fields': [field.name for field in Pengingat._meta.get_fields()],
        }
,
        {
            'label': 'KuponDiskon',
            'count': KuponDiskon.objects.count(),
            'list_url': 'main:get_kupon_diskon',
            'create_url': 'main:create_kupon_diskon',
            'fields': [field.name for field in KuponDiskon._meta.get_fields()],
        }
    ]

    return render(request, 'dashboard.html', {
        'entity_cards': entity_cards,
    })
	
#-------------- CRUD methods for Class Pelanggan ---------------
def create_pelanggan(request):
    if request.method == 'POST':
        form = PelangganForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_pelanggan')
    else:
        form = PelangganForm()
    return render(request, 'create_pelanggan.html', {'form': form})

def edit_pelanggan(request, id):
    pelanggan_obj = Pelanggan.objects.get(pk=id)
    form = PelangganForm(request.POST or None, instance=pelanggan_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_pelanggan')

    return render(request, 'edit_pelanggan.html', {'form': form})

def get_pelanggan(request):
    pelanggans = Pelanggan.objects.all()
    
    all_fields = [field.name for field in Pelanggan._meta.get_fields()]
    pelanggan_data = []
    form = PelangganForm()
    
    for pelanggan in pelanggans:
        pelanggan_dict = {}
        for field_name in all_fields:
            try:
                field = Pelanggan._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(pelanggan, field_name).all()
                    pelanggan_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    pelanggan_dict[field_name] = getattr(pelanggan, field_name)
            except:
                pelanggan_dict[field_name] = "N/A"
        pelanggan_data.append((pelanggan, pelanggan_dict))
    
    return render(request, 'pelanggan_list.html', {
        'pelanggan_data': pelanggan_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_pelanggan(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Pelanggan.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_pelanggan')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Pelanggan ----------------

#-------------- CRUD methods for Class AlamatDelivery ---------------
def create_alamat_delivery(request):
    if request.method == 'POST':
        form = AlamatDeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_alamat_delivery')
    else:
        form = AlamatDeliveryForm()
    return render(request, 'create_alamat_delivery.html', {'form': form})

def edit_alamat_delivery(request, id):
    alamat_delivery_obj = AlamatDelivery.objects.get(pk=id)
    form = AlamatDeliveryForm(request.POST or None, instance=alamat_delivery_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_alamat_delivery')

    return render(request, 'edit_alamat_delivery.html', {'form': form})

def get_alamat_delivery(request):
    alamat_deliverys = AlamatDelivery.objects.all()
    
    all_fields = [field.name for field in AlamatDelivery._meta.get_fields()]
    alamat_delivery_data = []
    form = AlamatDeliveryForm()
    
    for alamat_delivery in alamat_deliverys:
        alamat_delivery_dict = {}
        for field_name in all_fields:
            try:
                field = AlamatDelivery._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(alamat_delivery, field_name).all()
                    alamat_delivery_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    alamat_delivery_dict[field_name] = getattr(alamat_delivery, field_name)
            except:
                alamat_delivery_dict[field_name] = "N/A"
        alamat_delivery_data.append((alamat_delivery, alamat_delivery_dict))
    
    return render(request, 'alamat_delivery_list.html', {
        'alamat_delivery_data': alamat_delivery_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_alamat_delivery(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = AlamatDelivery.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_alamat_delivery')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class AlamatDelivery ----------------

#-------------- CRUD methods for Class Outlet ---------------
def create_outlet(request):
    if request.method == 'POST':
        form = OutletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_outlet')
    else:
        form = OutletForm()
    return render(request, 'create_outlet.html', {'form': form})

def edit_outlet(request, id):
    outlet_obj = Outlet.objects.get(pk=id)
    form = OutletForm(request.POST or None, instance=outlet_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_outlet')

    return render(request, 'edit_outlet.html', {'form': form})

def get_outlet(request):
    outlets = Outlet.objects.all()
    
    all_fields = [field.name for field in Outlet._meta.get_fields()]
    outlet_data = []
    form = OutletForm()
    
    for outlet in outlets:
        outlet_dict = {}
        for field_name in all_fields:
            try:
                field = Outlet._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(outlet, field_name).all()
                    outlet_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    outlet_dict[field_name] = getattr(outlet, field_name)
            except:
                outlet_dict[field_name] = "N/A"
        outlet_data.append((outlet, outlet_dict))
    
    return render(request, 'outlet_list.html', {
        'outlet_data': outlet_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_outlet(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Outlet.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_outlet')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Outlet ----------------

#-------------- CRUD methods for Class Koki ---------------
def create_koki(request):
    if request.method == 'POST':
        form = KokiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_koki')
    else:
        form = KokiForm()
    return render(request, 'create_koki.html', {'form': form})

def edit_koki(request, id):
    koki_obj = Koki.objects.get(pk=id)
    form = KokiForm(request.POST or None, instance=koki_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_koki')

    return render(request, 'edit_koki.html', {'form': form})

def get_koki(request):
    kokis = Koki.objects.all()
    
    all_fields = [field.name for field in Koki._meta.get_fields()]
    koki_data = []
    form = KokiForm()
    
    for koki in kokis:
        koki_dict = {}
        for field_name in all_fields:
            try:
                field = Koki._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(koki, field_name).all()
                    koki_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    koki_dict[field_name] = getattr(koki, field_name)
            except:
                koki_dict[field_name] = "N/A"
        koki_data.append((koki, koki_dict))
    
    return render(request, 'koki_list.html', {
        'koki_data': koki_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_koki(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Koki.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_koki')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Koki ----------------

#-------------- CRUD methods for Class Kurir ---------------
def create_kurir(request):
    if request.method == 'POST':
        form = KurirForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_kurir')
    else:
        form = KurirForm()
    return render(request, 'create_kurir.html', {'form': form})

def edit_kurir(request, id):
    kurir_obj = Kurir.objects.get(pk=id)
    form = KurirForm(request.POST or None, instance=kurir_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_kurir')

    return render(request, 'edit_kurir.html', {'form': form})

def get_kurir(request):
    kurirs = Kurir.objects.all()
    
    all_fields = [field.name for field in Kurir._meta.get_fields()]
    kurir_data = []
    form = KurirForm()
    
    for kurir in kurirs:
        kurir_dict = {}
        for field_name in all_fields:
            try:
                field = Kurir._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(kurir, field_name).all()
                    kurir_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    kurir_dict[field_name] = getattr(kurir, field_name)
            except:
                kurir_dict[field_name] = "N/A"
        kurir_data.append((kurir, kurir_dict))
    
    return render(request, 'kurir_list.html', {
        'kurir_data': kurir_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_kurir(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Kurir.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_kurir')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Kurir ----------------

#-------------- CRUD methods for Class Menu ---------------
def create_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_menu')
    else:
        form = MenuForm()
    return render(request, 'create_menu.html', {'form': form})

def edit_menu(request, id):
    menu_obj = Menu.objects.get(pk=id)
    form = MenuForm(request.POST or None, instance=menu_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_menu')

    return render(request, 'edit_menu.html', {'form': form})

def get_menu(request):
    menus = Menu.objects.all()
    
    all_fields = [field.name for field in Menu._meta.get_fields()]
    menu_data = []
    form = MenuForm()
    
    for menu in menus:
        menu_dict = {}
        for field_name in all_fields:
            try:
                field = Menu._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(menu, field_name).all()
                    menu_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    menu_dict[field_name] = getattr(menu, field_name)
            except:
                menu_dict[field_name] = "N/A"
        menu_data.append((menu, menu_dict))
    
    return render(request, 'menu_list.html', {
        'menu_data': menu_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_menu(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Menu.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_menu')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Menu ----------------

#-------------- CRUD methods for Class Pesanan ---------------
def create_pesanan(request):
    if request.method == 'POST':
        form = PesananForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_pesanan')
    else:
        form = PesananForm()
    return render(request, 'create_pesanan.html', {'form': form})

def edit_pesanan(request, id):
    pesanan_obj = Pesanan.objects.get(pk=id)
    form = PesananForm(request.POST or None, instance=pesanan_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_pesanan')

    return render(request, 'edit_pesanan.html', {'form': form})

def get_pesanan(request):
    pesanans = Pesanan.objects.all()
    
    all_fields = [field.name for field in Pesanan._meta.get_fields()]
    pesanan_data = []
    form = PesananForm()
    
    for pesanan in pesanans:
        pesanan_dict = {}
        for field_name in all_fields:
            try:
                field = Pesanan._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(pesanan, field_name).all()
                    pesanan_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    pesanan_dict[field_name] = getattr(pesanan, field_name)
            except:
                pesanan_dict[field_name] = "N/A"
        pesanan_data.append((pesanan, pesanan_dict))
    
    return render(request, 'pesanan_list.html', {
        'pesanan_data': pesanan_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_pesanan(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Pesanan.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_pesanan')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Pesanan ----------------

#-------------- CRUD methods for Class DetailPesanan ---------------
def create_detail_pesanan(request):
    if request.method == 'POST':
        form = DetailPesananForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_detail_pesanan')
    else:
        form = DetailPesananForm()
    return render(request, 'create_detail_pesanan.html', {'form': form})

def edit_detail_pesanan(request, id):
    detail_pesanan_obj = DetailPesanan.objects.get(pk=id)
    form = DetailPesananForm(request.POST or None, instance=detail_pesanan_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_detail_pesanan')

    return render(request, 'edit_detail_pesanan.html', {'form': form})

def get_detail_pesanan(request):
    detail_pesanans = DetailPesanan.objects.all()
    
    all_fields = [field.name for field in DetailPesanan._meta.get_fields()]
    detail_pesanan_data = []
    form = DetailPesananForm()
    
    for detail_pesanan in detail_pesanans:
        detail_pesanan_dict = {}
        for field_name in all_fields:
            try:
                field = DetailPesanan._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(detail_pesanan, field_name).all()
                    detail_pesanan_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    detail_pesanan_dict[field_name] = getattr(detail_pesanan, field_name)
            except:
                detail_pesanan_dict[field_name] = "N/A"
        detail_pesanan_data.append((detail_pesanan, detail_pesanan_dict))
    
    return render(request, 'detail_pesanan_list.html', {
        'detail_pesanan_data': detail_pesanan_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_detail_pesanan(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = DetailPesanan.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_detail_pesanan')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class DetailPesanan ----------------

#-------------- CRUD methods for Class Pembayaran ---------------
def create_pembayaran(request):
    if request.method == 'POST':
        form = PembayaranForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_pembayaran')
    else:
        form = PembayaranForm()
    return render(request, 'create_pembayaran.html', {'form': form})

def edit_pembayaran(request, id):
    pembayaran_obj = Pembayaran.objects.get(pk=id)
    form = PembayaranForm(request.POST or None, instance=pembayaran_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_pembayaran')

    return render(request, 'edit_pembayaran.html', {'form': form})

def get_pembayaran(request):
    pembayarans = Pembayaran.objects.all()
    
    all_fields = [field.name for field in Pembayaran._meta.get_fields()]
    pembayaran_data = []
    form = PembayaranForm()
    
    for pembayaran in pembayarans:
        pembayaran_dict = {}
        for field_name in all_fields:
            try:
                field = Pembayaran._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(pembayaran, field_name).all()
                    pembayaran_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    pembayaran_dict[field_name] = getattr(pembayaran, field_name)
            except:
                pembayaran_dict[field_name] = "N/A"
        pembayaran_data.append((pembayaran, pembayaran_dict))
    
    return render(request, 'pembayaran_list.html', {
        'pembayaran_data': pembayaran_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_pembayaran(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Pembayaran.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_pembayaran')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Pembayaran ----------------

#-------------- CRUD methods for Class NotaPesanan ---------------
def create_nota_pesanan(request):
    if request.method == 'POST':
        form = NotaPesananForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_nota_pesanan')
    else:
        form = NotaPesananForm()
    return render(request, 'create_nota_pesanan.html', {'form': form})

def edit_nota_pesanan(request, id):
    nota_pesanan_obj = NotaPesanan.objects.get(pk=id)
    form = NotaPesananForm(request.POST or None, instance=nota_pesanan_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_nota_pesanan')

    return render(request, 'edit_nota_pesanan.html', {'form': form})

def get_nota_pesanan(request):
    nota_pesanans = NotaPesanan.objects.all()
    
    all_fields = [field.name for field in NotaPesanan._meta.get_fields()]
    nota_pesanan_data = []
    form = NotaPesananForm()
    
    for nota_pesanan in nota_pesanans:
        nota_pesanan_dict = {}
        for field_name in all_fields:
            try:
                field = NotaPesanan._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(nota_pesanan, field_name).all()
                    nota_pesanan_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    nota_pesanan_dict[field_name] = getattr(nota_pesanan, field_name)
            except:
                nota_pesanan_dict[field_name] = "N/A"
        nota_pesanan_data.append((nota_pesanan, nota_pesanan_dict))
    
    return render(request, 'nota_pesanan_list.html', {
        'nota_pesanan_data': nota_pesanan_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_nota_pesanan(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = NotaPesanan.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_nota_pesanan')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class NotaPesanan ----------------

#-------------- CRUD methods for Class Pengingat ---------------
def create_pengingat(request):
    if request.method == 'POST':
        form = PengingatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_pengingat')
    else:
        form = PengingatForm()
    return render(request, 'create_pengingat.html', {'form': form})

def edit_pengingat(request, id):
    pengingat_obj = Pengingat.objects.get(pk=id)
    form = PengingatForm(request.POST or None, instance=pengingat_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_pengingat')

    return render(request, 'edit_pengingat.html', {'form': form})

def get_pengingat(request):
    pengingats = Pengingat.objects.all()
    
    all_fields = [field.name for field in Pengingat._meta.get_fields()]
    pengingat_data = []
    form = PengingatForm()
    
    for pengingat in pengingats:
        pengingat_dict = {}
        for field_name in all_fields:
            try:
                field = Pengingat._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(pengingat, field_name).all()
                    pengingat_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    pengingat_dict[field_name] = getattr(pengingat, field_name)
            except:
                pengingat_dict[field_name] = "N/A"
        pengingat_data.append((pengingat, pengingat_dict))
    
    return render(request, 'pengingat_list.html', {
        'pengingat_data': pengingat_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_pengingat(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = Pengingat.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_pengingat')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class Pengingat ----------------

#-------------- CRUD methods for Class KuponDiskon ---------------
def create_kupon_diskon(request):
    if request.method == 'POST':
        form = KuponDiskonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:get_kupon_diskon')
    else:
        form = KuponDiskonForm()
    return render(request, 'create_kupon_diskon.html', {'form': form})

def edit_kupon_diskon(request, id):
    kupon_diskon_obj = KuponDiskon.objects.get(pk=id)
    form = KuponDiskonForm(request.POST or None, instance=kupon_diskon_obj)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:get_kupon_diskon')

    return render(request, 'edit_kupon_diskon.html', {'form': form})

def get_kupon_diskon(request):
    kupon_diskons = KuponDiskon.objects.all()
    
    all_fields = [field.name for field in KuponDiskon._meta.get_fields()]
    kupon_diskon_data = []
    form = KuponDiskonForm()
    
    for kupon_diskon in kupon_diskons:
        kupon_diskon_dict = {}
        for field_name in all_fields:
            try:
                field = KuponDiskon._meta.get_field(field_name)
                if field.is_relation and field.many_to_many:
                    related_objects = getattr(kupon_diskon, field_name).all()
                    kupon_diskon_dict[field_name] = ", ".join([str(obj) for obj in related_objects]) or "None"
                else:
                    kupon_diskon_dict[field_name] = getattr(kupon_diskon, field_name)
            except:
                kupon_diskon_dict[field_name] = "N/A"
        kupon_diskon_data.append((kupon_diskon, kupon_diskon_dict))
    
    return render(request, 'kupon_diskon_list.html', {
        'kupon_diskon_data': kupon_diskon_data,
        'fields': all_fields,
        'form': form,
        
    })

def delete_kupon_diskon(request):
    if request.method == 'POST':
        object_id = request.POST.get('object_id')

        if object_id is None:
            return JsonResponse({"error": "ID is required"}, status=400)

        obj = KuponDiskon.objects.get(pk=object_id)
        obj.delete()
        return redirect('main:get_kupon_diskon')
    return JsonResponse({"error": "Invalid request method"}, status=405)


#-------------- end of Class KuponDiskon ----------------


