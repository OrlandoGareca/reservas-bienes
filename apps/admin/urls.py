from django.conf.urls import url,include
from ..admin.views import employee_add,employee_list,employee_delete,employee_edit,PromedioList,add_porcentaje,PromedioDelete

urlpatterns = [
    url(r'^index$', employee_list, name='employee_list'),
    url(r'^add$', employee_add, name="employee_add"),
    #url('<int:id>/details/', employee_details, name="employee_details"),
    url(r'^edit/(?P<id>\d+)/$', employee_edit, name="employee_edit"),
    #url(r'^edit/(?P<id_admin>\d+)/$', employee_edit, name='employee_edit'),
    url(r'^delete/(?P<id>\d+)/$', employee_delete, name="employee_delete"),

    #prmedio
    url(r'^listar$', PromedioList.as_view(), name='promedio_listar'),
    url(r'^nuevo/$',add_porcentaje, name='porcentaje_crear'),
    # url(r'^add/$', views.add_porcentaje, name='padd'),
    url(r'^eliminar/(?P<pk>\d+)/$', PromedioDelete.as_view(), name='promedio_eliminar'),
]