from .entities import ENTITIES


def diagram_entities(request):
    return {'diagram_entities': ENTITIES.values()}
