"""Keep MoTxT route conventions for the nine concrete diagram entities."""
from functools import partial
from django.urls import path
from . import views
from .entities import ENTITIES

app_name = 'main'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
for key in ENTITIES:
    urlpatterns += [
        path(f'get-all-{key}/', partial(views.entity_list, entity_key=key), name=f'get_{key}'),
        path(f'create-{key}/', partial(views.entity_form, entity_key=key), name=f'create_{key}'),
        path(f'edit-{key}/<int:id>/', partial(views.entity_form, entity_key=key), name=f'edit_{key}'),
        path(f'delete-{key}/', partial(views.entity_delete, entity_key=key), name=f'delete_{key}'),
    ]
