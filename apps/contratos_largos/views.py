# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.db.models.functions import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import datetime
from ..contratos_largos.forms import Select1, SelectCor, modal, FiltroFechas, Modificar
from django.core.urlresolvers import reverse_lazy
from ..contratos_largos.models import ContratoLargo, Lugar, User_lugar
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, View
# from ..contratos_largos.filters import ContratoLargoFilter
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import *
import json
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER

from reportlab.platypus import Table, TableStyle, Spacer, Paragraph
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, landscape, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .BaseReport import *

# Import for PDF documents ReportLab
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Spacer, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate,
                                Table, TableStyle)
from reportlab.platypus import Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter

from django.http import Http404

from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate

from reportlab.lib.units import inch
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet


def index(request):
    return render(request, 'contratos_largos/index.html')


def principal(request):
    return render(request, 'contratos_largos/principal.html')


class ContratoList(ListView):
    model = ContratoLargo
    template_name = 'contratos_largos/contrato_list.html'


class CalendarioList(ListView):
    model = ContratoLargo
    template_name = 'contratos_largos/principal.html'


class ContratoCrear(CreateView):
    model = ContratoLargo
    form_class = Select1
    template_name = 'contratos_largos/contrato_form.html'
    success_url = reverse_lazy('contratolargo:buscar')
    context_object_name = 'contratoLargos'


class ContratoCrearCorto(CreateView):
    model = ContratoLargo
    form_class = SelectCor
    template_name = 'contratos_largos/contrato_form.html'
    success_url = reverse_lazy('contratolargo:buscar')
    context_object_name = 'contratoLargos'


class ContratoUpdate(UpdateView):
    model = ContratoLargo
    form_class = Select1
    template_name = 'contratos_largos/contrato_form.html'
    success_url = reverse_lazy('contratolargo:buscar')


class ContratoDelete(DeleteView):
    model = ContratoLargo
    template_name = 'contratos_largos/contrato_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Se elimino correctamente')
        return redirect('contratolargo:buscarUsr')


def contrato_edit(request, id_contratolargo):
    mascota = ContratoLargo.objects.get(id=id_contratolargo)
    v = mascota.estado
    w = mascota.porcentaje_multa
    # print v
    # print w
    print(mascota.lugar)
    if request.method == 'GET':
        form = Modificar(instance=mascota, lugar=mascota.lugar)
        # form.lugar=mascota.lugar
    else:
        # modificar funciona normal
        # user=request.user.id
        # get_object_or_404(User,id=request.user.id)
        form = Modificar(request.POST, instance=mascota, lugar=mascota.lugar)

        if form.is_valid():
            if mascota.estado == True:
                # print mascota.porcentaje_multa
                qw = mascota.porcentaje_multa
                # print qw
                formulario = form.save(commit=False)

                print formulario.estado
                # print formulario.porcentaje_multa
                formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
                # lugares=get_object_or_404(Lugar,id=co.lugar)

                # formulario.user_id=lugares.name
                formulario.save()
                messages.success(request, "Se Actualizo Correctamente")
                return redirect('contratolargo:buscarUsr')
            else:
                formulario = form.save(commit=False)
                formulario.estado = False
                formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
                formulario.save()
                messages.success(request, "Se Actualizo Correctamente")
                return redirect('contratolargo:buscarUsr')
        else:
            messages.error(request, "Error al Insertar")
    return render(request, 'contratos_largos/modificar.html', {'form': form, "porcentaje": v})


@method_decorator(permission_required('contratos_largos.permiso_url_listlicenciada'), name='dispatch')
class buscar(View):
    context = {}
    model = ContratoLargo
    paginate_by = 10
    via = []
    luga = []
    error = ""

    def cargarDatos(self, uno=True, via=None):
        if uno:
            ContratoLargoList = self.model.objects.all()

        else:
            ContratoLargoList = via
        for co in ContratoLargoList:
            s1 = co.fecha_final
            now = datetime.now(timezone.utc)
            fecha_final = co.fecha_final
            dias = ((now - co.fecha_final).days)  # - 1
            if dias < 0:
                dias = 0

            lugares = get_object_or_404(Lugar, id=co.lugar)
            self.via.append({
                "id": co.id,
                "nombre": co.nombre,
                "dni_nit": co.dni_nit,
                "fecha_inicial": co.fecha_inicial,
                "fecha_final": co.fecha_final,
                "fecha_deposito": co.fecha_deposito,
                "monto_total": co.monto_total,
                "monto_depositado": co.monto_depositado,
                "monto_faltante": co.monto_faltante,
                "estado": co.estado,
                "nombre_completo_actividad": co.nombre_completo_actividad,
                "numero_factura": co.numero_factura,
                "numero_deposito": co.numero_deposito,
                "lugar_name": lugares.name,
                "espacio_name": co.espacio.name,
                "diastotales": dias

            })
        self.cargarlugar()

    def cargarlugar(self):
        lu = Lugar.objects.all()
        self.luga.append({
            "id": "",
            "descripcion": "..."
        })
        for l in lu:
            self.luga.append({
                "id": l.id,
                "descripcion": l.name
            })

    def to_int(self, valor):
        if valor.isdigit():
            return False
        return True

    def vaciar(self):
        self.via = []
        self.luga = []

    def get(self, request, *args, **kwargs):
        fecha_ini = request.GET.get('fecha_ini', None)
        fecha_final = request.GET.get('fecha_fini', None)
        # numero_factura=request.GET.get('num_fact')
        lugar1 = request.GET.get('lugar')
        # Ci_nit=request.GET.get('cedula')

        # self.cargarDatos()
        if fecha_ini == None and fecha_final == None and lugar1 == None:
            print ("entra")

            self.vaciar()
            self.cargarDatos(uno=True)

            self.context = {'filter': self.via, "Lugar": self.luga}
            return render(request, "contratos_largos/contrato_list.html", self.context)
        else:
            # aqui tiene que ir la validacion
            # print (lugar1, fecha_ini,fecha_final)
            if fecha_ini != "" and fecha_final != "":
                fecha_ini = datetime.strptime(str(fecha_ini), '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                fecha_final = datetime.strptime(str(fecha_final), '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            # print (fecha1,fecha2)

            if fecha_ini > fecha_final:
                if fecha_final == "":
                    self.vaciar()
                    self.error = self.error + "INTRODUSCA UNA FECHA INICIAL Y FECHA FINAL"
                    self.cargarlugar()
                    self.context = {'filter': self.via, "Lugar": self.luga, "error": self.error}

                else:
                    self.vaciar()
                    self.error = self.error + "FECHA INICIAL NO PUEDE SER MAYOR A LA FECHA FINAL"
                    self.cargarlugar()
                    self.context = {'filter': self.via, "Lugar": self.luga, "error": self.error}


            else:
                self.vaciar()
                entra = True
                uno = True
                dos = True
                tres = True
                cuatro = True
                # solo lugar
                if lugar1 != "" and fecha_ini == "" and fecha_final == "":
                    # lugares=get_object_or_404(Lugar,id=co.lugar)
                    con = self.model.objects.filter(lugar=lugar1)

                    uno = False
                    dos = False
                    entra = False
                    self.cargarDatos(uno=False, via=con)
                    self.context = {'filter': self.via, "Lugar": self.luga, "lugar_reuqest": lugar1}
                # solo fecha inicial y fecha final
                if uno and fecha_ini != "" and fecha_final != "" and lugar1 == "":
                    factura = self.model.objects.filter(fecha_inicial__gte=fecha_ini, fecha_final__lte=fecha_final)
                    dos = False
                    entra = False
                    self.cargarDatos(uno=False, via=factura)
                    self.context = {'filter': self.via, "Lugar": self.luga, "fecha_ini": fecha_ini,
                                    "fecha_final": fecha_final}
                ### fecha inicial ,fecha final y lugar
                if dos and fecha_ini != "" and fecha_final != "" and lugar1 != "":
                    factura = self.model.objects.filter(fecha_inicial__gte=fecha_ini, fecha_final__lte=fecha_final,
                                                        lugar=lugar1)
                    entra = False
                    print("entra fechas y lugar")
                    self.cargarDatos(uno=False, via=factura)
                    self.context = {'filter': self.via, "Lugar": self.luga, "fecha_ini": fecha_ini,
                                    "fecha_final": fecha_final, "lugar_reuqest": lugar1}
                    # solo ci_nit y numero factura

                ## ci y fechaq
                ## fecha ft numero_factura
                # ci ft lugar
                ## fechas ft ci ft lugar
                # ## fechas ft numero_factura ft lugar
                # fecha ft numero_Facrura ft ci ft lugar
                if entra:
                    self.cargarDatos(uno=True)
                    self.context = {'filter': self.via, "Lugar": self.luga}
                    # print(fecha_ini)
                # print(fecha_final)
                # print(self.via)
            # print(self.context)
            return render(request, "contratos_largos/contrato_list.html", self.context)


def modificarmodal(request, id_contratolargo):
    mascota = ContratoLargo.objects.get(id=id_contratolargo)
    if request.method == 'GET':
        now = datetime.now(timezone.utc)
        fecha_final = mascota.fecha_final
        dias = ((now - fecha_final).days)  # - 1
        if dias < 0:
            dias = 0
            monto_total_multa = mascota.mult_dia * dias
            mascota.monto_faltante = mascota.monto_faltante + monto_total_multa
        monto_total_multa = mascota.mult_dia * dias
        print monto_total_multa
        # print monto_total_multa
        mascota.monto_faltante = mascota.monto_faltante + monto_total_multa
        # print mascota.monto_faltante
        # mascota.monto_total= mascota.monto_total+1        #print mascota.monto_total# esto igual para no perder el valor se realiza
        # mascota.save()
        form = modal(instance=mascota)
        # print datetime.datetime.now(timezone.utc)
        # print dias
    else:
        form = modal(request.POST, instance=mascota)
        if form.is_valid():
            mascota = form.save(commit=False)
            now = datetime.now(timezone.utc)
            print now
            fecha_final = mascota.fecha_final
            print fecha_final
            dias = ((now - fecha_final).days)  # - 1
            print dias
            if dias < 0:
                dias = 0
                monto_total_multa = mascota.mult_dia * dias
                mascota.monto_faltante = mascota.monto_faltante + monto_total_multa
            monto_total_multa = mascota.mult_dia * dias
            print monto_total_multa
            mascota.estado = False
            mascota.monto_depositado = mascota.monto_depositado + mascota.monto_faltante
            print mascota.monto_depositado
            mascota.monto_total = mascota.monto_total + monto_total_multa
            print mascota.monto_total
            mascota.monto_faltante = 0
            mascota.save()
            messages.success(request, "Se Actualizo Correctamente")
            return redirect('contratolargo:buscarUsr')
        else:
            messages.error(request, "Error al Insertar")
    return render(request, 'contratos_largos/modal.html', {'form': form})


def contrato_delete(request, id_contratolargo):
    form = ContratoLargo.objects.get(id=id_contratolargo)
    if request.method == 'POST':
        form.delete()
        messages.success(request, "Se Elimino Correctamente")
        return redirect('contratolargo:buscarUsr')
    return render(request, 'contratos_largos/contrato_delete.html', {'form': form})


def search(request):
    ContratoLargoList = ContratoLargo.objects.all()
    via = []
    for co in ContratoLargoList:
        s1 = co.fecha_final
        now = datetime.now(timezone.utc)
        fecha_final = co.fecha_final
        dias = ((now - co.fecha_final).days)  # - 1
        if dias < 0:
            dias = 0
        # print (dias*(-1))
        via.append({
            "id": co.id,
            "nombre": co.nombre,
            "dni_nit": co.dni_nit,
            "fecha_inicial": co.fecha_inicial,
            "fecha_final": co.fecha_final,
            "fecha_deposito": co.fecha_deposito,
            "monto_total": co.monto_total,
            "monto_depositado": co.monto_depositado,
            "monto_faltante": co.monto_faltante,
            "estado": co.estado,
            "nombre_completo_actividad": co.nombre_completo_actividad,
            "numero_factura": co.numero_factura,
            "numero_deposito": co.numero_deposito,
            "lugar_name": co.lugar.name,
            "espacio_name": co.espacio.name,
            "diastotales": dias
        })
    # print(via)
    contratoLargoFilter = ContratoLargoFilter(request.GET, queryset=ContratoLargoList)
    return render(request, 'contratos_largos/contrato_list_user.html', {'filter': via})


def select_view(request):
    if request.method == 'POST':
        form = Select1(request.POST, user=request.user.id)
        print(form)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
            # print formulario.porcentaje_multa.valor#sirve para abrir el objecto y poder recien multiplicar el valor con el monto
            if formulario.monto_faltante < 0:
                formulario.monto_faltante = 0
                formulario.monto_depositado = formulario.monto_total
                formulario.estado = False
            formulario.mult_dia = formulario.monto_total * formulario.porcentaje_multa.valor
            # print datetime.datetime.now(timezone.utc)
            # print formulario.fecha_final
            now = datetime.now(timezone.utc)
            fecha_final = formulario.fecha_final
            # print ((now-fecha_final).days)-1
            formulario.user = get_object_or_404(User, id=request.user.id)
            formulario.save()
            messages.success(request, "Se Inserto Correctamente")
            return redirect('contratolargo:buscarUsr')
        else:
            messages.error(request, "Error al Insertar")
    else:
        form = Select1(user=request.user.id)
    return render(request, 'contratos_largos/contrato_form.html', {'form': form})


def selectcor_view(request):
    if request.method == 'POST':
        form = SelectCor(request.POST, user=request.user.id)
        if form.is_valid():
            formulario = form.save(commit=False)
            # formulario.user = request.user
            # print formulario.user
            formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
            if formulario.monto_faltante < 0:
                formulario.monto_faltante = 0
                formulario.monto_depositado = formulario.monto_total

            formulario.estado = False
            formulario.user = get_object_or_404(User, id=request.user.id)
            formulario.save()
            messages.success(request, "Se Inserto Correctamente")
            return redirect('contratolargo:buscarUsr')
        else:
            messages.error(request, "Error al Insertar")
    else:
        form = SelectCor(user=request.user.id)
    return render(request, 'contratos_largos/contrato_formcort.html', {'form': form})


def buscarContrato(request):
    if request.is_ajax():
        valorrecibido = request.GET['contrat']
        resultado_list = []
        for co in ContratoLargo.objects.all():
            cii = str(co.dni_nit)

            if cii[:len(valorrecibido)] == str(valorrecibido):
                lugares = get_object_or_404(Lugar, id=co.lugar)
                producto_json = {}
                producto_json['id'] = co.id
                producto_json['nombre'] = co.nombre
                producto_json['dni_nit'] = co.dni_nit
                # producto_json['fecha_inicial']=datetime.datetime.strptime(co.fecha_inicial,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
                # producto_json['fecha_final']=str(co.fecha_final)
                # producto_json['fecha_deposito']=co.fecha_deposito
                producto_json['monto_total'] = co.monto_total
                producto_json['monto_depositado'] = co.monto_depositado
                producto_json['monto_faltante'] = co.monto_faltante
                producto_json['estado'] = co.estado
                producto_json['nombre_completo_actividad'] = co.nombre_completo_actividad
                producto_json['numero_factura'] = co.numero_factura
                producto_json['numero_deposito'] = co.numero_deposito
                producto_json['lugar_name'] = lugares.name
                producto_json['espacio_name'] = co.espacio.name

                resultado_list.append(producto_json)

        # contratos=ContratoLargo.objects.filter(dni_nit__contains=request.GET['contrat'])
        '''enco = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime.datetime)
            or isinstance(obj, datetime.date)
            else None
        )

        json.dumps({'date': datetime.datetime.now()}, default=enco)
        resultado_list=[]        
        for co in contratos:
            lugares=get_object_or_404(Lugar,id=co.lugar)
            producto_json={}
            producto_json['id']=co.id
            producto_json['nombre']=co.nombre
            producto_json['dni_nit']=co.dni_nit           
            #producto_json['fecha_inicial']=datetime.datetime.strptime(co.fecha_inicial,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
            #producto_json['fecha_final']=str(co.fecha_final)
            #producto_json['fecha_deposito']=co.fecha_deposito
            producto_json['monto_total']=co.monto_total
            producto_json['monto_depositado']=co.monto_depositado
            producto_json['monto_faltante']=co.monto_faltante
            producto_json['estado']=co.estado
            producto_json['nombre_completo_actividad']=co.nombre_completo_actividad
            producto_json['numero_factura']=co.numero_factura
            producto_json['numero_deposito']=co.numero_deposito
            producto_json['lugar_name']=lugares.name
            producto_json['espacio_name']=co.espacio.name
             
            
            resultado_list.append(producto_json)'''

        data_json = json.dumps(resultado_list)
        return HttpResponse(data_json, "application/json")


def mostrarid(request):
    return request.user.id


@method_decorator(permission_required('contratos_largos.permiso_url_listusuario'), name='dispatch')
class buscar1(View):
    context = {}
    model = ContratoLargo
    model1 = User_lugar
    via = []
    luga = []
    error = ""

    def cargarDatos1(self, uno=True, via=None):
        if uno:
            lugar_id = self.model1.objects.filter(user_id__id=self.request.user.id)

            for l in lugar_id:
                luga = Lugar.objects.filter(id=l.lugar_trabajo_id)

                for c in luga:
                    # print(c.id)

                    contra = self.model.objects.filter(lugar=c.id)
                    for co in contra:
                        s1 = co.fecha_final
                        now = datetime.now(timezone.utc)
                        fecha_final = co.fecha_final
                        dias = ((now - co.fecha_final).days)  # - 1
                        if dias < 0:
                            dias = 0
                        lugares = get_object_or_404(Lugar, id=co.lugar)
                        self.via.append({
                            "id": co.id,
                            "nombre": co.nombre,
                            "dni_nit": co.dni_nit,
                            "fecha_inicial": co.fecha_inicial,
                            "fecha_final": co.fecha_final,
                            "fecha_deposito": co.fecha_deposito,
                            "monto_total": co.monto_total,
                            "monto_depositado": co.monto_depositado,
                            "monto_faltante": co.monto_faltante,
                            "estado": co.estado,
                            "nombre_completo_actividad": co.nombre_completo_actividad,
                            "numero_factura": co.numero_factura,
                            "numero_deposito": co.numero_deposito,
                            "lugar_name": lugares.name,
                            "espacio_name": co.espacio.name,
                            "diastotales": dias

                        })
            # print(self.via)
            ContratoLargoList = self.via
            # print(self.request.user.id)
        else:
            ContratoLargoList = via
            for co in ContratoLargoList:
                s1 = co.fecha_final
                now = datetime.now(timezone.utc)
                fecha_final = co.fecha_final
                dias = ((now - co.fecha_final).days)  # - 1
                if dias < 0:
                    dias = 0
                lugares = get_object_or_404(Lugar, id=co.lugar)
                self.via.append({
                    "id": co.id,
                    "nombre": co.nombre,
                    "dni_nit": co.dni_nit,
                    "fecha_inicial": co.fecha_inicial,
                    "fecha_final": co.fecha_final,
                    "fecha_deposito": co.fecha_deposito,
                    "monto_total": co.monto_total,
                    "monto_depositado": co.monto_depositado,
                    "monto_faltante": co.monto_faltante,
                    "estado": co.estado,
                    "nombre_completo_actividad": co.nombre_completo_actividad,
                    "numero_factura": co.numero_factura,
                    "numero_deposito": co.numero_deposito,
                    "lugar_name": lugares.name,
                    "espacio_name": co.espacio.name,
                    "diastotales": dias

                })
        self.cargarlugar()

    def cargarlugar(self):
        lu = Lugar.objects.all()
        self.luga.append({
            "id": "",
            "descripcion": "..."
        })
        for l in lu:
            self.luga.append({
                "id": l.id,
                "descripcion": l.name
            })

    def to_int(self, valor):
        if valor.isdigit():
            return False
        return True

    def vaciar(self):
        self.via = []
        self.luga = []

    def get(self, request, *args, **kwargs):
        numero_factura = request.GET.get('num_fact')
        Ci_nit = request.GET.get('cedula')
        # print numero_factura
        # print Ci_nit
        # self.cargarDatos()
        if numero_factura == None and Ci_nit == None:
            self.vaciar()
            self.cargarDatos1(uno=True)
            self.context = {'filter': self.via, "Lugar": self.luga}
            return render(request, "contratos_largos/contrato_list_user.html", self.context)
        else:
            # aqui tiene que ir la validacion
            if Ci_nit != "" and self.to_int(Ci_nit):
                self.vaciar()
                self.error = self.error + "CI TIENE QUE SER NUMEROS"
                self.cargarlugar()
                self.context = {'filter': self.via, "Lugar": self.luga, "error": self.error}
            elif numero_factura != "" and self.to_int(numero_factura):
                self.vaciar()
                self.error = self.error + "EL NUMERO DE FACTURA TIENE QUE SER NUMEROS"
                self.cargarlugar()
                self.context = {'filter': self.via, "Lugar": self.luga, "error": self.error}
            else:
                self.vaciar()
                entra = True
                uno = True
                dos = True

                if numero_factura != "" and Ci_nit == "":
                    # factura=self.model.objects.filter(numero_factura=numero_factura)
                    valorrecibido = numero_factura
                    # print(valorrecibido)
                    # print(request.user.id)
                    resultado_list = []
                    self.via = []
                    for co in ContratoLargo.objects.all():
                        cii = str(co.numero_factura)
                        if cii[:len(valorrecibido)] == str(valorrecibido) and co.user_id == request.user.id:
                            s1 = co.fecha_final
                            now = datetime.now(timezone.utc)
                            fecha_final = co.fecha_final
                            dias = ((now - co.fecha_final).days)  # - 1
                            if dias < 0:
                                dias = 0
                            lugares = get_object_or_404(Lugar, id=co.lugar)
                            self.via.append({
                                "id": co.id,
                                "nombre": co.nombre,
                                "dni_nit": co.dni_nit,
                                "fecha_inicial": co.fecha_inicial,
                                "fecha_final": co.fecha_final,
                                "fecha_deposito": co.fecha_deposito,
                                "monto_total": co.monto_total,
                                "monto_depositado": co.monto_depositado,
                                "monto_faltante": co.monto_faltante,
                                "estado": co.estado,
                                "nombre_completo_actividad": co.nombre_completo_actividad,
                                "numero_factura": co.numero_factura,
                                "numero_deposito": co.numero_deposito,
                                "lugar_name": lugares.name,
                                "espacio_name": co.espacio.name,
                                "diastotales": dias

                            })

                    entra = False
                    uno = False
                    dos = False
                    self.cargarlugar()
                    # self.cargarDatos1(uno=False,via=factura)
                if uno and Ci_nit != "" and numero_factura != "":
                    entra = False
                    dos = False
                    valorrecibido = Ci_nit
                    print(valorrecibido)
                    resultado_list = []
                    self.via = []
                    for co in ContratoLargo.objects.all():
                        cii = str(co.numero_factura)
                        if cii[:len(valorrecibido)] == str(valorrecibido) and co.user_id == request.user.id:
                            s1 = co.fecha_final
                            now = datetime.now(timezone.utc)
                            fecha_final = co.fecha_final
                            dias = ((now - co.fecha_final).days)  # - 1
                            if dias < 0:
                                dias = 0
                            lugares = get_object_or_404(Lugar, id=co.lugar)
                            self.via.append({
                                "id": co.id,
                                "nombre": co.nombre,
                                "dni_nit": co.dni_nit,
                                "fecha_inicial": co.fecha_inicial,
                                "fecha_final": co.fecha_final,
                                "fecha_deposito": co.fecha_deposito,
                                "monto_total": co.monto_total,
                                "monto_depositado": co.monto_depositado,
                                "monto_faltante": co.monto_faltante,
                                "estado": co.estado,
                                "nombre_completo_actividad": co.nombre_completo_actividad,
                                "numero_factura": co.numero_factura,
                                "numero_deposito": co.numero_deposito,
                                "lugar_name": lugares.name,
                                "espacio_name": co.espacio.name,
                                "diastotales": dias

                            })
                            self.cargarlugar()
                    # factura=self.model.objects.filter(dni_nit=Ci_nit,numero_factura=numero_factura)
                    # self.cargarDatos1(uno=False,via=factura)
                    # print("entra aqui")
                ## ci y fecha
                ## fecha ft numero_factura
                # ci ft lugar
                ## fechas ft ci ft lugar
                # ## fechas ft numero_factura ft lugar
                # fecha ft numero_Facrura ft ci ft lugar

                if dos and Ci_nit != "" and numero_factura == "":

                    valorrecibido = Ci_nit
                    print()
                    resultado_list = []
                    self.via = []
                    for co in ContratoLargo.objects.all():
                        cii = str(co.dni_nit)
                        if cii[:len(valorrecibido)] == str(valorrecibido) and co.user_id == request.user.id:
                            s1 = co.fecha_final
                            now = datetime.now(timezone.utc)
                            fecha_final = co.fecha_final
                            dias = ((now - co.fecha_final).days)  # - 1
                            if dias < 0:
                                dias = 0
                            lugares = get_object_or_404(Lugar, id=co.lugar)
                            self.via.append({
                                "id": co.id,
                                "nombre": co.nombre,
                                "dni_nit": co.dni_nit,
                                "fecha_inicial": co.fecha_inicial,
                                "fecha_final": co.fecha_final,
                                "fecha_deposito": co.fecha_deposito,
                                "monto_total": co.monto_total,
                                "monto_depositado": co.monto_depositado,
                                "monto_faltante": co.monto_faltante,
                                "estado": co.estado,
                                "nombre_completo_actividad": co.nombre_completo_actividad,
                                "numero_factura": co.numero_factura,
                                "numero_deposito": co.numero_deposito,
                                "lugar_name": lugares.name,
                                "espacio_name": co.espacio.name,
                                "diastotales": dias

                            })
                            self.cargarlugar()
                    entra = False

                if entra:
                    self.cargarDatos1(uno=True)
                self.context = {'filter': self.via, "Lugar": self.luga}
            return render(request, "contratos_largos/contrato_list_user.html", self.context)


class ReporteViaticosEmp(BasePlatypusReportOther):
    def __init__(self):
        self.begin(orientation='LANDSCAPE', rightMargin=28, leftMargin=28, topMargin=36, bottomMargin=28)

    def get(self, request, *args, **kwargs):
        lugar = self.kwargs.get('idlugar')
        fecha_ini = self.kwargs.get('idfecha_ini')
        fecha_fi = self.kwargs.get('idfecha_final')
        # cedulaidentidad=self.kwargs.get('iddni_nit')
        # factura=self.kwargs.get('idnumero_factura')
        self.draw(lugar, fecha_ini, fecha_fi)

        self.write(onFirstPage=self.title)
        return self.response

    def title(self, canvas, document, **kwargs):

        title = 'BOLETAS REGISTRADAS'
        canvas.saveState()

        archivo_imagen = settings.MEDIA_ROOT + '\images\escudo_gober.png'
        archivo_imagen1 = settings.MEDIA_ROOT + '\images\escudo_potosi.png'

        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawCentredString(self.x_start + self.width_internal / 2, self.y_start - 25,
                                 u"GOBIERNO AUTONOMO DEPARTAMENTAL DE POTOSI")
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawCentredString(self.x_start + self.width_internal / 2, self.y_start - 45,
                                 u"Secretaria Departamental Administracion y Financiera")
        canvas.drawCentredString(self.x_start + self.width_internal / 2, self.y_start - 65,
                                 u"Departamental de Tesoreria")
        canvas.drawImage(archivo_imagen1, self.x_start + 600, self.y_start - 64, 55, 55, preserveAspectRatio=True)
        self.draw_left_image(canvas=canvas,
                             url=archivo_imagen,
                             x=self.x_start + 70,
                             y=self.y_start - 8,
                             w=55,
                             h=55
                             )

    def draw(self, lugar, fecha_ini, fecha_fi):
        self.add(Spacer(1, 90))
        self.draw_table(lugar, fecha_ini, fecha_fi)

    def draw_table(self, lugar=None, fecha_ini=None, fecha_fi=None):
        basic_style_full_doble = self.get_basic_style_full_doble()
        basic_style_body = self.get_basic_style_body()
        basic_style_full_doble_void = self.get_basic_style_full_doble_void()
        viaticos = None
        try:
            # solo lugar
            if str(lugar) != "None" and str(fecha_ini) == "None" and str(fecha_fi) == "None":
                viaticos = ContratoLargo.objects.filter(lugar=lugar)
            # solo fecha inicial y fecha final
            if str(fecha_ini) != "None" and str(fecha_fi) != "None" and str(lugar) == "None":
                print("fechas")
                viaticos = ContratoLargo.objects.filter(fecha_inicial__gte=fecha_ini, fecha_final__lte=fecha_fi)
            # solo fecha inicial, fecha final y lugar
            if str(lugar) != "None" and str(fecha_ini) != "None" and str(fecha_fi) != "None":
                viaticos = ContratoLargo.objects.filter(lugar=lugar, fecha_inicial__gte=fecha_ini,
                                                        fecha_final__lte=fecha_fi)
            # solo cedula de identidad
            # if  str(lugar) == "None" and str(fecha_ini) == "None" and str(fecha_fi) == "None" and str(cedulaidentidad) != "None" and str(factura)=="None":
            #    viaticos=ContratoLargo.objects.filter(dni_nit=cedulaidentidad) 
            # solo numero factura
            # if  str(lugar) == "None" and str(fecha_ini) == "None" and str(fecha_fi) == "None" and str(cedulaidentidad) == "None" and str(factura)!="None":
            #    viaticos=ContratoLargo.objects.filter(numero_factura=factura)
            # factura=self.model.objects.filter(dni_nit=Ci_nit,numero_factura=numero_factura)

            # else:
            # viaticos=ContratoLargo.objects.all()
        except:
            raise Http404
        self.add(self.draw_in_table_top(0, viaticos, self.get_basic_style_full_doble_top(), basic_style_body,
                                        basic_style_full_doble_void, True))
        self.add(Spacer(1, 20))
        # self.add(self.draw_in_table_result(0,viaticos,self.get_basic_style_full_doble_button(), basic_style_body, basic_style_full_doble_void, True))
        # self.add(Spacer(1, 20))
        self.add(self.draw_in_table_resumen(0, viaticos, self.get_basic_style_full_doble_resumen(), basic_style_body,
                                            basic_style_full_doble_void, True))

    def draw_in_table_top(self, index=0, datereference=None, style=None, stylealt=None, stylevoid=None,
                          hasheader=False):

        supercabecera = [
            'N°',
            'Nombre',
            'Dni/Nit',
            'Fecha Inicial',
            'Fecha Final',
            'Fecha Deposito',
            'Monto Total',
            'Monto Depositado',
            'Monto Faltante',
            'Numero Factura',
            'Numero Deposito',
            'Lugar',
            'Espacio',
        ]
        preparandojson = []
        cont = 1
        for via in datereference:
            fehc = str(via.fecha_final)
            lugares = get_object_or_404(Lugar, id=via.lugar)
            preparandojson.append({
                'id': cont,
                'Nombre': via.nombre,
                'Dni/Nit': via.dni_nit,
                'fecha_inicial': fehc[:16],
                'fecha_final': fehc[:16],
                'fecha_depositado': fehc[:16],
                'monto_total': via.monto_total,
                'monto_depositado': via.monto_depositado,
                'monto_faltante': via.monto_faltante,
                'numero_factura': via.numero_factura,
                'numero_deposito': via.numero_deposito,
                # 'lugar':via.lugar,
                'lugar': lugares.name,
                'espacio': via.espacio
            })
            cont = cont + 1

        detalles = [(
            via["id"],
            via["Nombre"],
            via["Dni/Nit"],
            via["fecha_inicial"],
            via["fecha_final"],
            via["fecha_depositado"],
            via["monto_total"],
            via["monto_depositado"],
            via["monto_faltante"],
            via["numero_factura"],
            via["numero_deposito"],
            via["lugar"],
            via["espacio"]
        ) for via in preparandojson]

        cm = 29
        # cm = 23.4
        if hasheader:
            table = Table(
                [supercabecera] + detalles,
                colWidths=[
                    0.5 * cm,
                    2 * cm,
                    2 * cm,
                    2.5 * cm,
                    2.5 * cm,
                    2.5 * cm,
                    2 * cm,
                    2.5 * cm,
                    2 * cm,
                    2 * cm,
                    2 * cm,
                    1.5 * cm,
                    1.5 * cm,

                ],
                splitByRow=1,
                repeatRows=0
            )

        if style:
            if hasheader:
                table.setStyle(style)
            elif stylealt:
                table.setStyle(stylealt)
        return table

    def redondear(self, valor=None):
        leter = str(valor)
        for le in xrange(len(leter)):
            if leter[le] == '.':
                if (le + 2) == len(leter):
                    return '%s%s' % (valor, 0)
                else:
                    return valor

    def draw_in_table_resumen(self, index=0, datereference=None, style=None, stylealt=None, stylevoid=None,
                              hasheader=False):
        cabecera = [
            'RESUMEN',
            ' '
        ]
        Totalsumatoriapasaje = 0
        Totalsumatoriapeaje = 0
        Totalsumatoriaimporte = 0

        for viatico in datereference:
            Totalsumatoriapasaje = Totalsumatoriapasaje + viatico.monto_total
            Totalsumatoriapeaje = Totalsumatoriapeaje + viatico.monto_depositado
            Totalsumatoriaimporte = Totalsumatoriaimporte + viatico.monto_faltante

        detalles = [(
            "DESCRIPCIÓN",
            "IMPORTE EN BS."
        )]
        MONTO_TOTAL = [(
            "MONTO TOTAL",
            Totalsumatoriapasaje
        )]
        MONTO_DEPOSITADO = [(
            "MONTO DEPOSITADO",
            Totalsumatoriapeaje
        )]
        MONTO_FALTANTE = [(
            "MONTO FALTANTE",
            Totalsumatoriaimporte
        )]

        cm = 29
        # cm = 23.4
        if hasheader:
            table = Table(
                [cabecera] + detalles + MONTO_TOTAL + MONTO_DEPOSITADO + MONTO_FALTANTE,
                colWidths=[
                    3 * cm,
                    3 * cm
                ],
                splitByRow=1,
                repeatRows=1
            )
        if style:
            if hasheader:
                table.setStyle(style)
            elif stylealt:
                table.setStyle(stylealt)
        if len(datereference) == 0 and stylevoid is not None:
            table.setStyle(stylevoid)
        return table

    def draw_in_table_result(self, index=0, datereference=None, style=None, stylealt=None, stylevoid=None,
                             hasheader=False):
        Totalsumatoriapasaje = 0
        Totalsumatoriapeaje = 0
        Totalsumatoriaimporte = 0

        for viatico in datereference:
            Totalsumatoriapasaje = Totalsumatoriapasaje + viatico.monto_total
            Totalsumatoriapeaje = Totalsumatoriapeaje + viatico.monto_depositado
            Totalsumatoriaimporte = Totalsumatoriaimporte + viatico.monto_faltante
        detalles = [(
            "TOTAL",
            " ",
            " ",
            " ",
            " ",
            " ",
            12,
            12,
            12321

        )]
        cm = 29
        # cm = 23.4
        if hasheader:
            table = Table(
                detalles,
                colWidths=[
                    0.9 * cm,
                    2 * cm,
                    2.5 * cm,
                    3.5 * cm,
                    3.5 * cm,
                    3.5 * cm,
                    2.5 * cm,
                    3 * cm,
                    3 * cm,
                    3 * cm,
                    1.5 * cm,
                    1.5 * cm,
                    1.5 * cm,
                    2 * cm
                ],
                splitByRow=1,
                repeatRows=1
            )
        if style:
            if hasheader:
                table.setStyle(style)
            elif stylealt:
                table.setStyle(stylealt)
        if len(datereference) == 0 and stylevoid is not None:
            table.setStyle(stylevoid)
        return table


class ReportAnual(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        lugar = self.kwargs.get('idlugar')
        fecha_ini = self.kwargs.get('idfecha_inicial', None)
        fecha_fi = self.kwargs.get('idfecha_final', None)

        print (lugar, fecha_ini, fecha_fi)
        # print (idfecha_final)

        # cedulaidentidad=self.kwargs.get('iddni_nit')
        # factura=self.kwargs.get('idnumero_factura')
        # response['Content-Disposition'] = 'attachment; filename="First-PDF.pdf"'
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                                rightMargin=50,
                                leftMargin=50,
                                topMargin=115,
                                bottomMagin=20,
                                showBoundary=False)

        styles = getSampleStyleSheet()
        flowables = []
        spacer = Spacer(0, 0.25 * inch)
        # Obtener a los operadores
        # operadores = ContratoLargo.objects.all()
        operadores = None
        try:

            if str(lugar) == "None" and str(fecha_ini) == "None" and str(fecha_fi) == "None":
                operadores = ContratoLargo.objects.all()
                print("entra todos")
            # solo lugar
            if str(lugar) != "None" and str(fecha_ini) == "None" and str(fecha_fi) == "None":
                operadores = ContratoLargo.objects.filter(lugar=lugar)
                print("entra lugares")
            # solo fecha inicial y fecha final
            if str(fecha_ini) != "None" and str(fecha_fi) != "None" and str(lugar) == "None":
                print("entra fechas")
                operadores = ContratoLargo.objects.filter(fecha_inicial__gte=fecha_ini, fecha_final__lte=fecha_fi)
            # solo fecha inicial, fecha final y lugar
            if str(lugar) != "None" and str(fecha_ini) != "None" and str(fecha_fi) != "None":
                operadores = ContratoLargo.objects.filter(lugar=lugar, fecha_inicial__gte=fecha_ini,
                                                          fecha_final__lte=fecha_fi)
                print ("lugares y fechas reporte")
            # else:
            # viaticos=ContratoLargo.objects.all()
        except:
            raise Http404
        # print(operadores)
        # print("entra aqui")
        self.reporte(flowables, spacer, styles, operadores, canvas, doc)

        doc.build(flowables, onFirstPage=self.encabezado_pie, onLaterPages=self.encabezado_pie)

        response.write(buffer.getvalue())
        buffer.close()
        return response

    def encabezado_pie(self, pdf, document):
        pdf.saveState()

        logo_transporte = settings.MEDIA_ROOT + '\images\escudo_gober.png'
        logo_gober = settings.MEDIA_ROOT + '\images\escudo_potosi.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(logo_gober, 200, 480, 60, 60, preserveAspectRatio=True)
        pdf.drawImage(logo_transporte, 590, 480, 60, 60)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Times-Bold", 12)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(310, 525, u"Gobierno Autónomo Departamental de Potosí")
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(350, 485, u"Departamento de Tesoreria")
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(290, 505, u"Secretaria Departamental Administrativa y Financiera")
        logo_dakar = settings.MEDIA_ROOT + '\images\escudo_gober.png'
        logo_banderas = settings.MEDIA_ROOT + '\images\escudo_gober.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        # pdf.drawImage(logo_dakar, 100, 10, 60, 50)
        # pdf.drawImage(logo_banderas, 180, 12, 250, 15, mask='auto')
        # pdf.roundRect(450, 10, 100, 40, 5, stroke = 1)
        # pdf.setFont("Times-Roman", 6)
        # pdf.drawString(476, 40, u"Dirección Jurídica")
        #  pdf.drawString(460, 33,"Page %d" % doc.page)
        # pdf.drawString(476, 26, u"Teléfono 62 29292")
        # pdf.drawString(483, 19, u"Fax 6227477")

        pdf.restoreState()

    def reporte(self, floables, spacer, styles, operadores, canvas, doc):

        styles.add(ParagraphStyle(name="reporte", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman"))
        styles.add(ParagraphStyle(name="tittle", alignment=TA_CENTER, fontSize=10, fontName="Times-Bold"))
        styles.add(ParagraphStyle(name="titulotabla", alignment=TA_CENTER, fontSize=10, fontName="Times-Roman"))
        styles.add(ParagraphStyle(name="titulotablaresumida", alignment=TA_CENTER, fontSize=8, fontName="Times-Roman"))
        styles.add(ParagraphStyle(name="montosresu", alignment=TA_RIGHT, fontSize=10, fontName="Times-Roman"))
        styles.add(ParagraphStyle(name="montostabla", alignment=TA_RIGHT, fontSize=8, fontName="Times-Roman"))

        # floables.append(spacer)
        text = '''REPORTE DE RESERVAS'''
        para = Paragraph(text, styles["tittle"])
        floables.append(para)
        floables.append(spacer)

        num = Paragraph('''No.''', styles["titulotabla"])
        nombre = Paragraph("  " + 'Nombre' + "", styles["titulotabla"])
        ci = Paragraph('''Dni/Nit''', styles["titulotabla"])
        fechai = Paragraph('''Fecha Inicial''', styles["titulotabla"])
        fechaf = Paragraph('''Fecha Final   ''', styles["titulotabla"])
        fechad = Paragraph('''Fecha Deposito''', styles["titulotabla"])
        mtotal = Paragraph('''Monto Total''', styles["titulotabla"])
        mdepositado = Paragraph('''Monto Depositado''', styles["titulotabla"])
        mfaltante = Paragraph('''Monto Faltante''', styles["titulotabla"])
        nfactura = Paragraph('''Numero Factura''', styles["titulotabla"])
        ndeposito = Paragraph('''Numero Deposito''', styles["titulotabla"])
        lugar = Paragraph('''Lugar''', styles["titulotabla"])
        espacio = Paragraph('''Espacio''', styles["titulotabla"])

        encabezado_tabla = [num, '    Nombre    ', ci, fechai, fechaf, fechad, mtotal, mdepositado, mfaltante, nfactura,
                            ndeposito, lugar, '   Espacio   ']
        data = [encabezado_tabla]
        num = 1
        for operador in operadores:
            lugares = get_object_or_404(Lugar, id=operador.lugar)
            # print(lugares)
            # print(" entra aqui")
            # upper() para poner todo en mayuscula  %Y-%m-%d %H:%M:%S
            fila = []
            fila.append(Paragraph(str(num), styles["reporte"]))
            fila.append(Paragraph(operador.nombre, styles["reporte"]))
            fila.append(Paragraph(str(operador.dni_nit), styles["reporte"]))
            fila.append(Paragraph(str(operador.fecha_inicial.strftime('%d/%m/%Y %H:%M'))[:16], styles["reporte"]))
            fila.append(Paragraph(str(operador.fecha_final.strftime('%d/%m/%Y %H:%M'))[:16], styles["reporte"]))
            fila.append(Paragraph(str(operador.fecha_deposito.strftime('%d/%m/%Y %H:%M'))[:16], styles["reporte"]))
            fila.append(Paragraph(str(operador.monto_total) + ".bs", styles["montostabla"]))
            fila.append(Paragraph(str(operador.monto_depositado) + ".bs", styles["montostabla"]))
            fila.append(Paragraph(str(operador.monto_faltante) + ".bs", styles["montostabla"]))
            fila.append(Paragraph(str(operador.numero_factura), styles["reporte"]))
            fila.append(Paragraph(str(operador.numero_deposito), styles["reporte"]))
            fila.append(Paragraph(str(lugares), styles["reporte"]))
            fila.append(Paragraph(str(operador.espacio), styles["reporte"]))
            data.append(fila)
            num += 1
        # print(  data.append(fila))
        tabla = Table(data=data, style=[('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ])
        # tabla = Table(data = data, style = [('GRID',(0,0),(-1,-1),0.5,colors.grey),], colWidths=[22,150,60,210] )
        tabla.setStyle(TableStyle(
            [
                ('TEXTCOLOR', (1, -4), (7, -4), colors.red),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]
        ))
        floables.append(tabla)
        floables.append(spacer)
        floables.append(spacer)
        # encabezado_tabla=['  SUM. MONTO TOTAL  ','   SUM. MONTO DEPOSITADO   ' , '  SUM. MONTO FALTANTE   ']
        # data = [encabezado_tabla]
        # num = 1
        Totalsumamontototal = 0
        Totalsumamontodepositado = 0
        Totalsumamontofaltante = 0
        cabecera = [
            'RESUMEN',
            ' '
        ]
        for operador in operadores:
            Totalsumamontototal = Totalsumamontototal + operador.monto_total
            Totalsumamontodepositado = Totalsumamontodepositado + operador.monto_depositado
            Totalsumamontofaltante = Totalsumamontofaltante + operador.monto_faltante
        # fila = []
        # fila.append(Paragraph(str(Totalsumamontototal), styles["reporte"]))
        # fila.append(Paragraph(str(Totalsumamontodepositado), styles["reporte"]))
        # fila.append(Paragraph(str(Totalsumamontofaltante), styles["reporte"]))
        # data.append(fila)
        # num += 1
        # tabla = Table(data = data, style = [('GRID',(0,0),(-1,-1),0.5,colors.grey),])
        # tabla = Table(data = data, style = [('GRID',(0,0),(-1,-1),0.5,colors.grey),], colWidths=[22,150,60,210] )
        # tabla.setStyle(TableStyle(
        # [

        #        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        #        ('TEXTCOLOR',(0, 0),(0, -1),colors.white),
        #        ('FONTSIZE', (0, 0), (-1, -1), 9),
        #        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        #        ('BACKGROUND', (0, 0),(-1, 0),colors.gray),
        #        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        #        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        #        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        #        ('ALIGN', (0, 0 ), (-1, -1), 'CENTER'),
        #        ('VALIGN',(0,0),(-1, -1),'MIDDLE'),
        # ]
        # ))
        # encabezados tabla resumen
        montotal = Paragraph('''MONTO TOTAL''', styles["titulotablaresumida"])
        mondepositado = Paragraph('''MONTO DEPOSITADO''', styles["titulotablaresumida"])
        monfaltante = Paragraph('''MONTO FALTANTE''', styles["titulotablaresumida"])
        # montos tabla resumen
        totalmon = Paragraph(str(Totalsumamontototal) + ".bs", styles["montosresu"])
        depositadomon = Paragraph(str(Totalsumamontodepositado) + ".bs", styles["montosresu"])
        faltantemon = Paragraph(str(Totalsumamontofaltante) + ".bs", styles["montosresu"])
        # print (totalmon,depositadomon,faltantemon)
        detalles = [(
            "DESCRIPCIÓN",
            "IMPORTE EN BS."
        )]
        MONTO_TOTAL = [(
            montotal,
            totalmon
        )]
        MONTO_DEPOSITADO = [(
            mondepositado,
            depositadomon
        )]
        MONTO_FALTANTE = [(
            monfaltante,
            faltantemon
        )]

        cm = 29

        table = Table(
            [cabecera] + detalles + MONTO_TOTAL + MONTO_DEPOSITADO + MONTO_FALTANTE,
            colWidths=[
                4 * cm,
                4 * cm
            ],
            splitByRow=1,
            repeatRows=1,
            style=[('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ]
        )
        # table = Table(data = data, style = [('GRID',(0,0),(-1,-1),0.5,colors.grey),])
        table.setStyle(TableStyle(
            [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('SPAN', (0, 0), (1, 0)),
                ('ALIGN', (0, 0), (1, 4), 'RIGHT'),
                ('ALIGN', (0, 0), (1, 1), 'CENTER'),
            ]
        ))
        # floables.append(tabla)
        floables.append(table)
def login_request(request):
    if request.user.is_authenticated:
        return redirect('contratolargo:principal')
    else:

        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print ("entra")
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print ("entra aqui")
                    # messages.info(request, f"You are now logged in as {username}")
                    return redirect('contratolargo:principal')
                else:
                    messages.error(request, "Usted ya no esta activo")
                    print("Usted ya no esta activo")

                messages.error(request, "Tu usuario o contraseña es incorrecto")
                print("Tu usuario o contraseña es incorrecto")
        form = AuthenticationForm()
        return render(request=request, template_name="index.html", context={"form": form})
