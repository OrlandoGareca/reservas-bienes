import django_filters
from django.forms import DateInput, Select
from forms import Select1, SelectCor
from ..contratos_largos.models import ContratoLargo


class ContratoLargoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    numero_deposito = django_filters.NumberFilter(lookup_expr='icontains')
    fecha_inicial = django_filters.DateTimeFilter(
        widget=DateInput(
            attrs={
                'class': 'datein',
                'placeholder':'dd/mm/aaaa'
            }
        )
    )
    class Meta:
        model = ContratoLargo
        fields = ['id', 'fecha_inicial', 'numero_deposito', 'nombre']

