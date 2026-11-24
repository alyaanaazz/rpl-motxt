from django import forms
from django.utils.safestring import SafeString
from .models import *

class PelangganForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Pelanggan
        fields = ('__all__')

class AlamatDeliveryForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = AlamatDelivery
        fields = ('__all__')

class OutletForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Outlet
        fields = ('__all__')

class KokiForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Koki
        fields = ('__all__')

class KurirForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Kurir
        fields = ('__all__')

class MenuForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Menu
        fields = ('__all__')

class PesananForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Pesanan
        fields = ('__all__')

class DetailPesananForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = DetailPesanan
        fields = ('__all__')

class PembayaranForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Pembayaran
        fields = ('__all__')

class NotaPesananForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = NotaPesanan
        fields = ('__all__')

class PengingatForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = Pengingat
        fields = ('__all__')

class KuponDiskonForm(forms.ModelForm):
    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group'>"))

    class Meta:
        model = KuponDiskon
        fields = ('__all__')
