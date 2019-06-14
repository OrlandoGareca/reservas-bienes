# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from models import Lugar,Espacio,ContratoLargo,promediomulta,User_lugar
# Register your models here.
admin.site.register(Lugar)
admin.site.register(Espacio)
admin.site.register(ContratoLargo)
admin.site.register(promediomulta)
admin.site.register(User_lugar)
