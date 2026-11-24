"""Forms for the concrete classes in the enrichment diagram."""
from django import forms
from django.utils.safestring import mark_safe


class DiagramModelForm(forms.ModelForm):
    def as_div(self):
        return mark_safe(super().as_div().replace('<div>', '<div class="form-group">'))

    def clean(self):
        data = super().clean()
        name = self._meta.model.__name__
        if name == 'Pesanan':
            alamat, pelanggan = data.get('alamat_delivery'), data.get('pelanggan')
            koki, outlet = data.get('koki'), data.get('outlet')
            if alamat and pelanggan and alamat.pelanggan_id != pelanggan.pk:
                self.add_error('alamat_delivery', 'Alamat harus milik pelanggan yang dipilih.')
            if koki and outlet and koki.outlet_id != outlet.pk:
                self.add_error('koki', 'Koki harus bekerja di outlet yang dipilih.')
        if name == 'DetailPesanan':
            pesanan, menu = data.get('pesanan'), data.get('menu')
            if pesanan and menu and not menu.menu_outlet.filter(outlet=pesanan.outlet).exists():
                self.add_error('menu', 'Menu harus ditawarkan pada outlet pesanan.')
        return data
