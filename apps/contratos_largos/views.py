# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models.functions import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from ..contratos_largos.forms import Select1,SelectCor,modal,FiltroFechas,Modificar
from django.core.urlresolvers import reverse_lazy
from  ..contratos_largos.models import ContratoLargo,Lugar,User_lugar
from django.views.generic import ListView,UpdateView,DeleteView,CreateView,View
from ..contratos_largos.filters import ContratoLargoFilter
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#Create your views here.


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
     success_url = reverse_lazy('contratolargo:buscar')

def contrato_edit(request,id_contratolargo):
    mascota = ContratoLargo.objects.get(id=id_contratolargo)
    v= mascota.estado
    print(v)
    w = mascota.porcentaje_multa
    #print v
    #print w
    if request.method == 'GET':
        form = Modificar(instance=mascota)
    else:
        #modificar funciona normal 
        form = Modificar(request.POST, instance=mascota)
        if form.is_valid():
            if mascota.estado == True:
                #print mascota.porcentaje_multa
                qw = mascota.porcentaje_multa
                #print qw
                formulario = form.save(commit=False)
                
                print formulario.estado
                #print formulario.porcentaje_multa
                formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
                formulario.save()
                messages.success(request, "Se Actualizo Correctamente")
                return redirect('contratolargo:buscarClas')
            else:    
                formulario = form.save(commit=False)
                formulario.estado = False
                formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
                formulario.save()
                messages.success(request, "Se Actualizo Correctamente")
                return redirect('contratolargo:buscarClas')
        else:
            messages.error(request, "Error al Insertar")
    return render(request,'contratos_largos/modificar.html', {'form': form,"porcentaje":v})

class buscar(View):
    context={}
    model=ContratoLargo
    via=[]
    luga=[]
    error=""
    def cargarDatos(self,uno=True,via=None):
        if uno:
            ContratoLargoList = self.model.objects.all()
            
        else:
            ContratoLargoList=via
        for co in ContratoLargoList:
            s1=co.fecha_final
            now = datetime.datetime.now(timezone.utc)
            fecha_final = co.fecha_final
            dias = ((now-co.fecha_final).days) #- 1
            if dias < 0:
                dias = 0
            self.via.append({
                "id":co.id, 
                "nombre":co.nombre,
                "dni_nit":co.dni_nit,
                "fecha_inicial":co.fecha_inicial,
                "fecha_final":co.fecha_final,
                "fecha_deposito":co.fecha_deposito,
                "monto_total":co.monto_total,
                "monto_depositado":co.monto_depositado,
                "monto_faltante":co.monto_faltante,
                "estado":co.estado,
                "nombre_completo_actividad":co.nombre_completo_actividad,
                "numero_factura":co.numero_factura,
                "numero_deposito":co.numero_deposito,
                "lugar_name":co.lugar.name,
                "espacio_name":co.espacio.name,
                "diastotales":dias
                

            })
        self.cargarlugar()
    def cargarlugar(self):
        lu=Lugar.objects.all()
        self.luga.append({
                "id":"",
                "descripcion":"..."
            })
        for l in lu:
            self.luga.append({
                "id":l.id,
                "descripcion":l.name
            })
    
    def to_int(self,valor):
        if valor.isdigit():
            return False
        return True
    def vaciar(self):
        self.via=[]
        self.luga=[]
    def get(self,request,*args,**kwargs):
                fecha_ini=request.GET.get('fecha_ini')                                                                                  
                fecha_final=request.GET.get('fecha_fini')
                numero_factura=request.GET.get('num_fact')
                lugar1=request.GET.get('lugar')
                Ci_nit=request.GET.get('cedula')
                
                #self.cargarDatos()
                if fecha_ini == None and fecha_final == None and numero_factura == None and lugar1 == None and Ci_nit == None:   
                    self.vaciar()                    
                    self.cargarDatos(uno=True)
                    self.context={'filter': self.via,"Lugar":self.luga}                                                             
                    return render(request,"contratos_largos/contrato_list.html",self.context)
                else:
                    # aqui tiene que ir la validacion
                    if Ci_nit !="" and self.to_int(Ci_nit):
                        self.vaciar()                        
                        self.error=self.error+"CI TIENE QUE SER NUMEROS"                
                        self.cargarlugar()
                        self.context={'filter': self.via,"Lugar":self.luga,"error":self.error}  
                    elif numero_factura !="" and self.to_int(numero_factura):                        
                        self.vaciar()                        
                        self.error=self.error+"EL NUMERO DE FACTURA TIENE QUE SER NUMEROS"                
                        self.cargarlugar()
                        self.context={'filter': self.via,"Lugar":self.luga,"error":self.error} 
                    else:
                        self.vaciar()                        
                        entra=True
                        uno=True
                        dos=True
                        tres=True
                        cuatro=True
                        quinto=True
                        if numero_factura != "" and  lugar1 == "" and fecha_ini == "" and fecha_final == "" and Ci_nit == "":
                            factura=self.model.objects.filter(numero_factura=numero_factura)
                            entra=False
                            uno=False
                            dos=False
                            tres=False
                            cuatro=False
                            quinto=False
                            self.cargarDatos(uno=False,via=factura)
                            # lugar1 !="..."
                        if uno and lugar1 != "" and numero_factura == "" and fecha_ini == "" and fecha_final == "" and Ci_nit == "":
                            con=self.model.objects.filter(lugar__id=lugar1)
                            entra=False
                            dos=False
                            tres=False
                            cuatro=False
                            quinto=False
                            self.cargarDatos(uno=False,via=con)
                        if dos and fecha_ini != "" and fecha_final != "" and lugar1 == "" and numero_factura == "" and Ci_nit == "":
                            factura=self.model.objects.filter(fecha_inicial__gte=fecha_ini,fecha_final__lte=fecha_final)
                            entra=False
                            tres=False
                            cuatro=False
                            quinto=False
                            self.cargarDatos(uno=False,via=factura)
                        ### fecha ft lugar 
                        if tres and  fecha_ini != "" and fecha_final != "" and lugar1 != ""  and numero_factura == "" and Ci_nit == "":
                            factura=self.model.objects.filter(fecha_inicial__gte=fecha_ini,fecha_final__lte=fecha_final,lugar__id=lugar1)
                            entra=False
                            cuatro=False
                            quinto=False
                            self.cargarDatos(uno=False,via=factura)   
                        if cuatro and Ci_nit != "" and  numero_factura != "" and fecha_ini == "" and fecha_final == "" and lugar1 == "":
                            entra=False
                            quinto=False
                            factura=self.model.objects.filter(dni_nit=Ci_nit,numero_factura=numero_factura)
                            self.cargarDatos(uno=False,via=factura)
                            print("entra aqui")
                        ## ci y fecha
                        ## fecha ft numero_factura
                        # ci ft lugar 
                        ## fechas ft ci ft lugar
                        # ## fechas ft numero_factura ft lugar  
                        # fecha ft numero_Facrura ft ci ft lugar  
                        if quinto and Ci_nit != "" and  lugar1 == "" and numero_factura == "" and fecha_ini == "" and fecha_final == "":
                            factura=self.model.objects.filter(dni_nit=Ci_nit)
                            entra=False
                            self.cargarDatos(uno=False,via=factura)
                        
                        if entra:
                            self.cargarDatos(uno=True)
                        self.context={'filter': self.via,"Lugar":self.luga,"lugar_reuqest":lugar1}                                                             
                    return render(request,"contratos_largos/contrato_list.html",self.context)

def modificarmodal(request,id_contratolargo):
    mascota = ContratoLargo.objects.get(id=id_contratolargo)
    if request.method == 'GET':
        now = datetime.datetime.now(timezone.utc)
        fecha_final = mascota.fecha_final
        dias = ((now - fecha_final).days) #- 1
        if dias < 0:
            dias = 0
            monto_total_multa = mascota.mult_dia * dias
            mascota.monto_faltante = mascota.monto_faltante + monto_total_multa
        monto_total_multa = mascota.mult_dia * dias
        print monto_total_multa
        #print monto_total_multa
        mascota.monto_faltante= mascota.monto_faltante+monto_total_multa
        #print mascota.monto_faltante
        #mascota.monto_total= mascota.monto_total+1        #print mascota.monto_total# esto igual para no perder el valor se realiza
        #mascota.save()
        form = modal(instance=mascota)
        #print datetime.datetime.now(timezone.utc)
        #print dias
    else:
        form = modal(request.POST, instance=mascota)
        if form.is_valid():
            mascota=form.save(commit=False)
            now = datetime.datetime.now(timezone.utc)
            print now
            fecha_final = mascota.fecha_final
            print fecha_final
            dias = ((now - fecha_final).days) #- 1
            print dias
            if dias < 0:
                dias = 0
                monto_total_multa = mascota.mult_dia * dias
                mascota.monto_faltante = mascota.monto_faltante + monto_total_multa
            monto_total_multa = mascota.mult_dia * dias
            print monto_total_multa
            mascota.estado = False
            mascota.monto_depositado=mascota.monto_depositado+mascota.monto_faltante
            print mascota.monto_depositado
            mascota.monto_total=mascota.monto_total+monto_total_multa
            print mascota.monto_total
            mascota.monto_faltante=0
            mascota.save()
            messages.success(request, "Se Actualizo Correctamente")
            return redirect('contratolargo:buscarClas')
        else:
            messages.error(request, "Error al Insertar")
    return render(request,'contratos_largos/modal.html', {'form': form})

def contrato_delete(request, id_contratolargo):
    form = ContratoLargo.objects.get(id=id_contratolargo)
    if request.method == 'POST':
        form.delete()
        messages.success(request, "Se Elimino Correctamente")
        return redirect('contratolargo:buscarClas')
    return render(request,'contratos_largos/contrato_delete.html', {'form': form})

def search(request):
    ContratoLargoList = ContratoLargo.objects.all()
    via=[]
    for co in ContratoLargoList:
        s1=co.fecha_final
        now = datetime.datetime.now(timezone.utc)
        fecha_final = co.fecha_final
        dias = ((now-co.fecha_final).days) #- 1
        if dias < 0:
            dias = 0
        #print (dias*(-1))
        via.append({
            "id":co.id, 
            "nombre":co.nombre,
            "dni_nit":co.dni_nit,
            "fecha_inicial":co.fecha_inicial,
            "fecha_final":co.fecha_final,
            "fecha_deposito":co.fecha_deposito,
            "monto_total":co.monto_total,
            "monto_depositado":co.monto_depositado,
            "monto_faltante":co.monto_faltante,
            "estado":co.estado,
            "nombre_completo_actividad":co.nombre_completo_actividad,
            "numero_factura":co.numero_factura,
            "numero_deposito":co.numero_deposito,
            "lugar_name":co.lugar.name,
            "espacio_name":co.espacio.name,
            "diastotales":dias
        })
    #print(via)
    contratoLargoFilter = ContratoLargoFilter(request.GET, queryset=ContratoLargoList)
    return render(request, 'contratos_largos/contrato_list_user.html', {'filter': via})

def select_view(request):
    print(request.user.id)
    print("Entra")
    if request.method == 'POST':
        
        form = Select1(request.POST,user=request.user.id)
        if form.is_valid():
             formulario = form.save(commit=False)
             formulario.monto_faltante = formulario.monto_total - formulario.monto_depositado
             # print formulario.porcentaje_multa.valor#sirve para abrir el objecto y poder recien multiplicar el valor con el monto
             if formulario.monto_faltante < 0:
                formulario.monto_faltante = 0
                formulario.monto_depositado = formulario.monto_total
                formulario.estado=False
             formulario.mult_dia = formulario.monto_total * formulario.porcentaje_multa.valor
             #print datetime.datetime.now(timezone.utc)
             #print formulario.fecha_final
             now = datetime.datetime.now(timezone.utc)
             fecha_final = formulario.fecha_final
             #print ((now-fecha_final).days)-1
             formulario.save()
             messages.success(request, "Se Inserto Correctamente")
             return redirect('contratolargo:buscarClas')
        else:
            messages.error(request, "Error al Insertar")
    else:
        form = Select1(user=request.user.id)
    return render(request,'contratos_largos/contrato_form.html', {'form': form})

def selectcor_view(request):
    print(request.user.id)
    print("Entra")
    if request.method == 'POST':
        form = SelectCor(request.POST,user=request.user.id)
        if form.is_valid():
             formulario = form.save(commit=False)
             formulario.user = request.user
             print formulario.user
             formulario.monto_faltante=formulario.monto_total-formulario.monto_depositado
             if formulario.monto_faltante < 0:
                formulario.monto_faltante = 0
                formulario.monto_depositado = formulario.monto_total
             formulario.estado= False
             formulario.save()
             messages.success(request, "Se Inserto Correctamente")
             return redirect('contratolargo:buscarClas')
        else:
            messages.error(request, "Error al Insertar")
    else:
        form = SelectCor()
    return render(request,'contratos_largos/contrato_formcort.html', {'form': form})



def mostrarid(request):
    return request.user.id

class buscar1(View):
    context={}
    model=ContratoLargo
    model1=User_lugar
    via=[]
    luga=[]
    error=""
    def cargarDatos1(self,uno=True,via=None):
        if uno:
            lugar_id=self.model1.objects.filter(user_id__id=self.request.user.id)
            for l in lugar_id:
                luga=Lugar.objects.filter(id=l.lugar_trabajo_id)
            
                for c in luga:
                    #print(c.id)
                    contra=self.model.objects.filter(lugar__id=c.id)
                    for co in contra:
                        s1=co.fecha_final
                        now = datetime.datetime.now(timezone.utc)
                        fecha_final = co.fecha_final
                        dias = ((now-co.fecha_final).days) #- 1
                        if dias < 0:
                            dias = 0
                        self.via.append({
                            "id":co.id, 
                            "nombre":co.nombre,
                            "dni_nit":co.dni_nit,
                            "fecha_inicial":co.fecha_inicial,
                            "fecha_final":co.fecha_final,
                            "fecha_deposito":co.fecha_deposito,
                            "monto_total":co.monto_total,
                            "monto_depositado":co.monto_depositado,
                            "monto_faltante":co.monto_faltante,
                            "estado":co.estado,
                            "nombre_completo_actividad":co.nombre_completo_actividad,
                            "numero_factura":co.numero_factura,
                            "numero_deposito":co.numero_deposito,
                            "lugar_name":co.lugar.name,
                            "espacio_name":co.espacio.name,
                            "diastotales":dias
                            

                        })
            #print(self.via)
            ContratoLargoList = self.via
            #print(self.request.user.id)
        else:
            ContratoLargoList=via
            for co in ContratoLargoList:
                s1=co.fecha_final
                now = datetime.datetime.now(timezone.utc)
                fecha_final = co.fecha_final
                dias = ((now-co.fecha_final).days) #- 1
                if dias < 0:
                    dias = 0
                self.via.append({
                    "id":co.id, 
                    "nombre":co.nombre,
                    "dni_nit":co.dni_nit,
                    "fecha_inicial":co.fecha_inicial,
                    "fecha_final":co.fecha_final,
                    "fecha_deposito":co.fecha_deposito,
                    "monto_total":co.monto_total,
                    "monto_depositado":co.monto_depositado,
                    "monto_faltante":co.monto_faltante,
                    "estado":co.estado,
                    "nombre_completo_actividad":co.nombre_completo_actividad,
                    "numero_factura":co.numero_factura,
                    "numero_deposito":co.numero_deposito,
                    "lugar_name":co.lugar.name,
                    "espacio_name":co.espacio.name,
                    "diastotales":dias
                    

                })
        self.cargarlugar()
    def cargarlugar(self):
        lu=Lugar.objects.all()
        self.luga.append({
                "id":"",
                "descripcion":"..."
            })
        for l in lu:
            self.luga.append({
                "id":l.id,
                "descripcion":l.name
            })
    
    def to_int(self,valor):
        if valor.isdigit():
            return False
        return True
    def vaciar(self):
        self.via=[]
        self.luga=[]
    def get(self,request,*args,**kwargs):
                numero_factura=request.GET.get('num_fact')
                Ci_nit=request.GET.get('cedula')
                #print numero_factura
                #print Ci_nit
                #self.cargarDatos()
                if numero_factura == None and Ci_nit == None:   
                    self.vaciar()                    
                    self.cargarDatos1(uno=True)
                    self.context={'filter': self.via,"Lugar":self.luga}                                                             
                    return render(request,"contratos_largos/contrato_list_user.html",self.context)
                else:
                    # aqui tiene que ir la validacion
                    if Ci_nit !="" and self.to_int(Ci_nit):
                        self.vaciar()                        
                        self.error=self.error+"CI TIENE QUE SER NUMEROS"                
                        self.cargarlugar()
                        self.context={'filter': self.via,"Lugar":self.luga,"error":self.error}  
                    elif numero_factura !="" and self.to_int(numero_factura):                        
                        self.vaciar()                        
                        self.error=self.error+"EL NUMERO DE FACTURA TIENE QUE SER NUMEROS"                
                        self.cargarlugar()
                        self.context={'filter': self.via,"Lugar":self.luga,"error":self.error} 
                    else:
                        self.vaciar()                        
                        entra=True
                        uno=True
                        dos=True
                       
                        if numero_factura != "" and Ci_nit == "":
                            factura=self.model.objects.filter(numero_factura=numero_factura)
                            entra=False
                            uno=False
                            dos=False
                           
                            self.cargarDatos1(uno=False,via=factura)     
                        if uno and Ci_nit != "" and  numero_factura != "":
                            entra=False
                            dos=False
                            factura=self.model.objects.filter(dni_nit=Ci_nit,numero_factura=numero_factura)
                            self.cargarDatos1(uno=False,via=factura)
                            print("entra aqui")
                        ## ci y fecha
                        ## fecha ft numero_factura
                        # ci ft lugar 
                        ## fechas ft ci ft lugar
                        # ## fechas ft numero_factura ft lugar  
                        # fecha ft numero_Facrura ft ci ft lugar  

                        if dos and Ci_nit != "" and  numero_factura == "":
                            factura=self.model.objects.filter(dni_nit=Ci_nit)
                            entra=False
                            self.cargarDatos1(uno=False,via=factura)
                        if entra:
                            self.cargarDatos1(uno=True)
                        self.context={'filter': self.via,"Lugar":self.luga}                                                             
                    return render(request,"contratos_largos/contrato_list_user.html",self.context)



















