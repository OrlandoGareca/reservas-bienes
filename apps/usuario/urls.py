from django.conf.urls import url
from ..usuario.views import RegistroUsuario
from django.contrib.auth.decorators import login_required
from .views import user_edit
urlpatterns =[
    url(r'^registrar', login_required(RegistroUsuario.as_view()), name="registrar"),
    url(r'^editar/(?P<id_user>\d+)/$', login_required(user_edit), name='usuario_actualizar'),

]