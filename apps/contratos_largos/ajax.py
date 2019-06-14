from django.http import JsonResponse

from .models import  Espacio


def get_municipios(request):
    #estado_id = request.GET.get('id')
    lugar_id = request.GET.get('lugar_id')

    municipios = Espacio.objects.none()
    options = '<option value="" selected="selected">------------------</option>'
    if lugar_id:
        municipios = Espacio.objects.filter(estado_id=lugar_id)
    for municipio in municipios:
        options += '<option value="%s">%s</option>' % (
            municipio.id,
            municipio.name
        )
    response = {}
    response['municipios'] = options
    return JsonResponse(response)


