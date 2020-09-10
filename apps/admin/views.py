# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib import messages
from ..admin.forms import UserForm,PromedioForm
from  ..contratos_largos.models import ContratoLargo,Lugar,User_lugar,promediomulta
from django.views.generic import ListView,UpdateView,DeleteView,CreateView,View


#from admin.forms import UserForm
# Create your views here.

def employee_list(request):
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html', context)

def employee_add(request):
   
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()  
            messages.success(request, "Usuario creado correctamente")
            return redirect('administrador:employee_list')
        else:
            messages.error(request, "Error al crear usuario")
            return render(request, 'employee/add.html')
    else:
        user_form = UserForm()
        return render(request, 'employee/add.html',  {'user_form': user_form})


def employee_edit(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()    
            messages.success(request, "Se Actualizo Correctamente")
            return redirect('administrador:employee_list')
        else:
            messages.error(request, "Error al Actualizar")
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form": user_form})


def employee_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Se elimino al usuario")
        return redirect('administrador:employee_list')
       
    else:
      
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
 
    else:
        f = UserCreationForm()
 
    return render(request, 'admin/registrar.html', {'form': f})


class PromedioList(ListView):
    model = promediomulta
    template_name = 'promedio/index.html'
    queryset = promediomulta.objects.all()

def add_porcentaje(request):
    if request.method == 'POST': # si el usuario está enviando el formulario con datos
        form = PromedioForm(request.POST) # Bound form
        if form.is_valid():
            new_persona = form.save() # Guardar los datos en la base de datos

            return HttpResponseRedirect(reverse('administrador:promedio_listar'))
    else:
        form = PromedioForm() # Unbound form

    return render(request, 'promedio/add.html', {'form': form})


class PromedioDelete(DeleteView):
     model = promediomulta
     template_name = 'promedio/delete.html'
    
     def delete(self, request, *args, **kwargs):
        messages.success(request, 'Se elimino correctamente')
        return redirect('administrador:promedio_listar')
    


