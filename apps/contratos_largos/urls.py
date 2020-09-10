from django.conf.urls import url,include
from .ajax import get_municipios
from django.contrib.auth.decorators import login_required
from ..contratos_largos.views import index,select_view,selectcor_view,contrato_delete,contrato_edit,modificarmodal, \
    ContratoList,ContratoCrear,ContratoUpdate,ContratoDelete,search,principal,ContratoCrearCorto,ReporteViaticosEmp,buscar,login_request

from .views import buscar,buscar1,buscarContrato,ReportAnual

urlpatterns = [
    url(r'^$', login_required(index),name='index'),
    url(r'^nuevo$', login_required(select_view), name='contratolargo_crear'),
    url(r'^nuevocorto$', login_required(selectcor_view), name='contratolargo_crear_corto'),
    url(r'^buscar/$',login_required(search), name='buscar'),
    url(r'^buscarClas/$',login_required(buscar.as_view()), name='buscarClas'),
    url(r'^buscarUsr/$',login_required(buscar1.as_view()), name='buscarUsr'),
    url(r'^principal/',login_required(principal), name='principal'),

    url(r'^eliminar/(?P<pk>\d+)/$', login_required(ContratoDelete.as_view()), name='contratolargo_eliminar'),
    url(r'^editar/(?P<id_contratolargo>\d+)/$', login_required(contrato_edit), name='contratolargo_actualizar'),
    url(r'^ajax/get_municipios/$', login_required(get_municipios), name='get_municipios'),
    url(r'^mod/(?P<id_contratolargo>\d+)/$',login_required(modificarmodal), name='modificar'),
    url(r'^buscarContrato/$',login_required(buscarContrato),name='buscarContrato'),
    url(r'^reporte/(?P<idlugar>[-\w]+)/(?P<idfecha_inicial>[-\w]+)/(?P<idfecha_final>[-\w]+)/$', ReporteViaticosEmp.as_view(), name='reportes'),
    url(r'^reportes/(?P<idlugar>[-\w]+)/(?P<idfecha_inicial>.+?)/(?P<idfecha_final>.+?)/$', login_required(ReportAnual.as_view()), name='reporte_anual_operador'),    

]