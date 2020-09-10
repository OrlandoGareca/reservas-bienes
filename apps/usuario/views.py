# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from ..usuario.forms import RegistroForm


class RegistroUsuario(CreateView):
    model = User
    template_name = "usuario/registrar.html"
    form_class = RegistroForm
    success_url = reverse_lazy('contratolargo:principal')


def user_edit(request, id_user):
    user = User.objects.get(id=id_user)
    if request.method == 'GET':
        form = RegistroForm(instance=user)
    else:
        form = RegistroForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Se Actualizo Correctamente")
            return redirect('contratolargo:principal')
        else:
            messages.error(request, "Error al Actualizar Datos")
    return render(request, 'usuario/actualizar_usuario.html', {'form': form})
