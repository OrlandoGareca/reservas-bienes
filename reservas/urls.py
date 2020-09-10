"""reservas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin
from apps.contratos_largos.views import login_request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login,logout_then_login,password_reset,password_reset_done,password_reset_confirm,password_reset_complete

urlpatterns = [
    url(r'^$',RedirectView.as_view(pattern_name='login',permanent=False)),
    url(r'^admin/', admin.site.urls),
    url(r'^usuario/', include('apps.usuario.urls', namespace="usuario")),
    url(r'^accounts/login/', login_request, name='login'),
    url(r'^contratolargo/', include('apps.contratos_largos.urls', namespace="contratolargo")),
    url(r'^logout/',logout_then_login, name='logout'),
    url(r'^reset/password_reset', password_reset,{'template_name':'registration/password_reset_form.html','email_template_name':'registration/password_reset_email.html'}, name='password_reset'),
    url(r'^reset/password_reset_done', password_reset_done,{'template_name':'registration/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,{'template_name':'registration/password_reset_confirm.html'},name='password_reset_confirm'),
    url(r'^reset/done', password_reset_complete, {'template_name':'registration/password_reset_complete.html'},name='password_reset_complete'),
    url(r'^admin/', include('apps.admin.urls', namespace="administrador")),
]
