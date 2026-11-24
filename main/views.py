"""CRUD adapted from the MoTxT output for the relational KebabDEL diagram."""
from django.db.models.deletion import ProtectedError, RestrictedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .entities import ENTITIES


def landing_page(request):
    return render(request, 'landing_page.html', {
        'model_info': {key: entity.label for key, entity in ENTITIES.items()},
    })


def dashboard(request):
    return render(request, 'dashboard.html', {'entity_cards': [
        {'label': entity.label, 'count': entity.model.objects.count(),
         'list_url': f'main:get_{key}', 'create_url': f'main:create_{key}',
         'fields': [field.name for field in entity.model._meta.fields]}
        for key, entity in ENTITIES.items()
    ]})


def entity_list(request, entity_key, error=None, status=200):
    entity = ENTITIES[entity_key]
    fields = entity.model._meta.fields
    related = [field.name for field in fields if field.is_relation]
    objects = entity.model.objects.select_related(*related).order_by('pk')
    return render(request, 'diagram_entity_list.html', {
        'entity': entity,
        'fields': [field.verbose_name for field in fields],
        'rows': [
            {'object': obj, 'values': [getattr(obj, field.name) for field in fields],
             'edit_url': reverse(f'main:edit_{entity_key}', args=[obj.pk])}
            for obj in objects
        ],
        'create_url': reverse(f'main:create_{entity_key}'),
        'delete_url': reverse(f'main:delete_{entity_key}'),
        'error': error,
    }, status=status)


def entity_form(request, entity_key, id=None):
    entity = ENTITIES[entity_key]
    instance = get_object_or_404(entity.model, pk=id) if id is not None else None
    form = entity.form(request.POST if request.method == 'POST' else None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'main:get_{entity_key}')
    return render(request, 'diagram_entity_form.html', {
        'entity': entity, 'form': form, 'editing': instance is not None,
        'list_url': reverse(f'main:get_{entity_key}'),
    })


def entity_delete(request, entity_key):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        object_id = int(request.POST.get('object_id'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'ID must be an integer'}, status=400)
    obj = get_object_or_404(ENTITIES[entity_key].model, pk=object_id)
    try:
        obj.delete()
    except (ProtectedError, RestrictedError):
        return entity_list(request, entity_key, error='Data masih dipakai oleh data lain. Hapus relasi yang terkait terlebih dahulu.', status=409)
    return redirect(f'main:get_{entity_key}')
