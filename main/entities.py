"""Shared CRUD registry; Pengguna is abstract and has no standalone table/form."""
from dataclasses import dataclass
from django.forms import modelform_factory
from . import models
from .forms import DiagramModelForm


@dataclass(frozen=True)
class Entity:
    key: str
    model: type
    form: type

    @property
    def label(self):
        return self.model.__name__


ENTITIES = {}
for key, model in (
    ('pelanggan', models.Pelanggan), ('alamat_delivery', models.AlamatDelivery),
    ('outlet', models.Outlet), ('koki', models.Koki), ('menu', models.Menu),
    ('menu_outlet', models.MenuOutlet), ('pesanan', models.Pesanan),
    ('detail_pesanan', models.DetailPesanan), ('pembayaran', models.Pembayaran),
):
    form = modelform_factory(
        model, form=DiagramModelForm, fields='__all__',
        exclude=tuple(field.name for field in model._meta.many_to_many),
    )
    ENTITIES[key] = Entity(key, model, form)
