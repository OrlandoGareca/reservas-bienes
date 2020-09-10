from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404

from ..contratos_largos.models import ContratoLargo, Lugar, User_lugar
from .models import *
from django.forms.fields import DateField, DateTimeField
from bootstrap3_datetime.widgets import DateTimePicker

TRUE_FALSE_CHOICES = (
    (True, 'Activo'),
    (False, 'Inactivo')
    # (None,' Descartado')

)
# no_ue=[]
# no_ue.append(('','....'))
# for item in SecresubSecre.objects.filter(gestion=2018).order_by('ue').values_list("ue",flat = True).distinct():
#    no_ue.append((item,valor))
# class name(forms.ModelForms):
#	ue = forms.ChoiceField(choices=no_ue, label="U.E.",widget=forms.Select(attrs={'class':'input form-control'}))
#	class Meta:
#	-----
'''def devolver(request):
    return request.user.id
id=devolver()'''


class Select1(forms.ModelForm):
    # lugar = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Lugar",widget=forms.Select(attrs={'class':'form-control'}))
    # fecha_inicial=forms.TextInput(label="Nombre",widget=forms.DateTimeInput(format=['%m/%d/%Y %H:%M'],attrs={'class': 'form-control','type':"datetime-local" })),
    numero_factura = forms.CharField(required=False, widget=forms.NumberInput())
    numero_deposito = forms.CharField(required=False, widget=forms.NumberInput())
    fecha_inicial = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "DD/MM/YYYY HH:mm", "pickSeconds": False}))
    fecha_final = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "DD/MM/YYYY HH:mm", "pickSeconds": False}))
    fecha_deposito = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "DD/MM/YYYY HH:mm", "pickSeconds": False}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(Select1, self).__init__(*args, **kwargs)
        # super(self.__class__,self).__init__(*args, **kwargs)
        self.fields['espacio'].required = False
        # asi vuelves tus campos no requeridos
        self.fields['monto_faltante'].required = False
        no_lugar = []
        no_lugar.append(('', '---------'))
        # print(User_lugar.objects.filter(user_id__id=self.user))
        for item in User_lugar.objects.filter(user_id__id=self.user):
            lugares = get_object_or_404(Lugar, id=item.lugar_trabajo.id)
            no_lugar.append((lugares.id, lugares.name))
        # self.fields['lugar'] = forms.ModelChoiceField(queryset=Lugar.objects.values_list('Lugar',flat=True).filter(id=item.lugar_trabajo.id))
        print(no_lugar)
        # self.fields['lugar'].queryset = forms.ChoiceField(choices=no_lugar)
        # print (self.fields['lugar'].queryset = forms.ChoiceField(choices=no_lugar))
        self.fields['lugar'] = forms.ChoiceField(choices=no_lugar, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ContratoLargo
        fields = [
            'nombre', 'dni_nit', 'fecha_inicial', 'fecha_final', 'fecha_deposito',
            'porcentaje_multa', 'monto_total', 'monto_depositado', 'estado', 'nombre_completo_actividad',
            'numero_factura', 'numero_deposito', 'lugar', 'espacio', 'monto_faltante',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre'}),
            'dni_nit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),

            # 'fecha_inicial': forms.DateTimeInput(format=('%Y%m/%d %H:%M:%S %Z'),attrs={'class': 'form-control','type':"datetime-local" }),
            # 'fecha_final': forms.DateTimeInput(attrs={'class': 'form-control','type':"datetime-local" }),
            # 'fecha_deposito': forms.DateTimeInput(attrs={'class': 'form-control','type':"datetime-local" }),

            # 'fecha_inicial': forms.DateTimeInput(attrs={'class': 'datein', 'placeholder':'dd/mm/aaaa hh:mm'}),
            # 'fecha_final': forms.DateTimeInput(attrs={'class': 'datefi', 'placeholder':'dd/mm/aaaa hh:mm'}),
            # 'fecha_deposito': forms.DateTimeInput(attrs={'class': 'datede','placeholder':'dd/mm/aaaa hh:mm'}),
            'porcentaje_multa': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'monto_depositado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'estado': forms.Select(attrs={'disabled': 'True'}, choices=TRUE_FALSE_CHOICES),
            'nombre_completo_actividad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0-255 caracteres'}),
            # 'numero_factura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            # 'numero_deposito': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            # 'lugar': forms.Select(attrs={'class':'form-control'}),
            'espacio': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 255:
            raise forms.ValidationError("El nombre tiene que tener maximo 255 caracteres")
        return nombre

    def clean_dni_nit(self):
        dni_nit = self.cleaned_data.get('dni_nit')
        if len(str(dni_nit)) > 10:
            raise forms.ValidationError("El numero de DNI/NIT tiene que tener maximo 10 caracteres")
        else:
            return dni_nit

    def clean_nombre_completo_actividad(self):
        nombre_completo_actividad = self.cleaned_data.get('nombre_completo_actividad')
        if len(nombre_completo_actividad) > 255:
            raise forms.ValidationError("El nombre de la actividad tiene que tener maximo 255 caracteres")
        return nombre_completo_actividad

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        num_fac = ContratoLargo.objects.filter(numero_factura=numero_factura).exists()
        if len(str(numero_factura)) > 10:
            raise forms.ValidationError("El numero de factura tiene que tener maximo 10 caracteres")
        else:
            if num_fac:
                raise forms.ValidationError("El numero de factura ya existe")
        return numero_factura

    def clean_numero_deposito(self):
        numero_deposito = self.cleaned_data.get('numero_deposito')
        num_dep = ContratoLargo.objects.filter(numero_deposito=numero_deposito).exists()
        if len(str(numero_deposito)) > 10:
            raise forms.ValidationError("El numero de deposito tiene que tener maximo 10 caracteres")
        else:
            if num_dep:
                raise forms.ValidationError("El numero de deposito ya existe")
        return numero_deposito

    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if len(str(monto_total)) > 8:
            raise forms.ValidationError("El monto total tiene que tener maximo 8 digitos")
        return monto_total

    def clean_monto_depositado(self):
        monto_depositado = self.cleaned_data.get('monto_depositado')
        monto_total = self.cleaned_data.get('monto_total')
        if (monto_depositado == monto_total):
            raise forms.ValidationError("El monto depositado no puede ser igual al monto total")
        else:
            if (monto_total < monto_depositado):
                raise forms.ValidationError("El monto depositado no puede ser mayor al monto total")
            else:
                if len(str(monto_depositado)) > 8:
                    raise forms.ValidationError("El monto depositado tiene que tener maximo 8 digitos")
        return monto_depositado

    def clean_fecha_inicial(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        if (fecha_inicial == None):
            raise forms.ValidationError("Introdusca una fecha inicial")
        return fecha_inicial

    def clean_fecha_final(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')

        if (fecha_final == None):
            raise forms.ValidationError("Introdusca una fecha final")
        else:
            if (fecha_inicial == fecha_final):
                raise forms.ValidationError("La fecha final no puede ser igual a la fecha inicial")
            else:
                if fecha_final < fecha_inicial:
                    raise forms.ValidationError("Fecha final no puede ser menor a la fecha inicial")
        return fecha_final

    def clean_fecha_deposito(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        fecha_deposito = self.cleaned_data.get('fecha_deposito')

        if (fecha_deposito == None):
            raise forms.ValidationError("Introdusca una fecha de deposito")
        else:
            if (fecha_final == None):
                raise forms.ValidationError("Introdusca una fecha inicial o fecha final valida")
            else:
                if (fecha_deposito > fecha_final):
                    raise forms.ValidationError("Fecha de deposito no puede ser mayor a la fecha final")
        return fecha_deposito

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if (lugar == None):
            raise forms.ValidationError("Seleccione un lugar")
        return lugar

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        if (espacio == None):
            raise forms.ValidationError("Seleccione un espacio")
        return espacio


'''def devolver(request):
    return request.user.id
id=devolver()'''


class SelectCor(forms.ModelForm):
    # lugar = forms.ChoiceField(choices=no_lugar, label="Lugar",widget=forms.Select(attrs={'class':'form-control'}))
    fecha_inicial = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}, attrs={'placeholder': 'dd/mm/aaaa hh:mm'}))
    fecha_final = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}, attrs={'placeholder': 'dd/mm/aaaa hh:mm'}))
    fecha_deposito = forms.DateTimeField(required=False, widget=DateTimePicker(
        options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False}, attrs={'placeholder': 'dd/mm/aaaa hh:mm'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SelectCor, self).__init__(*args, **kwargs)
        # super(self.__class__,self).__init__(*args, **kwargs)
        self.fields['espacio'].required = False
        # asi vuelves tus campos no requeridos
        no_lugar = []
        no_lugar.append(('', '---------'))
        # print(User_lugar.objects.filter(user_id__id=self.user))
        for item in User_lugar.objects.filter(user_id__id=self.user):
            lugares = get_object_or_404(Lugar, id=item.lugar_trabajo.id)
            no_lugar.append((lugares.id, lugares.name))
        # self.fields['lugar'] = forms.ModelChoiceField(queryset=Lugar.objects.values_list('Lugar',flat=True).filter(id=item.lugar_trabajo.id))
        print(no_lugar)
        # self.fields['lugar'].queryset = forms.ChoiceField(choices=no_lugar)
        # print (self.fields['lugar'].queryset = forms.ChoiceField(choices=no_lugar))
        self.fields['lugar'] = forms.ChoiceField(choices=no_lugar, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ContratoLargo
        fields = [
            'nombre', 'dni_nit', 'fecha_inicial', 'fecha_final', 'fecha_deposito', 'monto_total', 'monto_depositado',
            'nombre_completo_actividad', 'numero_factura', 'numero_deposito', 'lugar', 'espacio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre'}),
            'dni_nit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'monto_depositado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'nombre_completo_actividad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0-255 caracteres'}),
            'numero_factura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'numero_deposito': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            # 'lugar': forms.Select(attrs={'class':'form-control'}),
            'espacio': forms.Select(attrs={'class': 'form-control'})
        }

    '''def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        print(self.user)
        super(self.__class__,self).__init__(*args, **kwargs)
        self.fields['espacio'].required = False
        # asi vuelves tus campos no requeridos
        self.fields['monto_faltante'].required = False 
        no_lugar=[]
        no_lugar.append(('','---------'))
        for item in User_lugar.objects.filter(user_id__id=self.user):
            print(item)       
            lugar=get_object_or_404(Lugar, id = item.lugar_trabajo.id)
            no_lugar.append((lugar.id,lugar.name))
        self.fields['lugar'] = forms.ChoiceField(choices=no_lugar)
        #self.fields['lugar'].queryset = forms.ChoiceField(choices=TRUE_FALSE_CHOICES)'''

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 255:
            raise forms.ValidationError("El nombre tiene que tener maximo 255 caracteres")
        return nombre

    def clean_dni_nit(self):
        dni_nit = self.cleaned_data.get('dni_nit')
        if len(str(dni_nit)) > 10:
            raise forms.ValidationError("El numero de DNI/NIT tiene que tener maximo 10 caracteres")
        else:
            return dni_nit

    def clean_nombre_completo_actividad(self):
        nombre_completo_actividad = self.cleaned_data.get('nombre_completo_actividad')
        if len(nombre_completo_actividad) > 255:
            raise forms.ValidationError("El nombre de la actividad tiene que tener maximo 255 caracteres")
        return nombre_completo_actividad

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        num_fac = ContratoLargo.objects.filter(numero_factura=numero_factura).exists()
        if len(str(numero_factura)) > 10:
            raise forms.ValidationError("El numero de factura tiene que tener maximo 10 caracteres")
        else:
            if num_fac:
                raise forms.ValidationError("El numero de factura ya existe")
        return numero_factura

    def clean_numero_deposito(self):
        numero_deposito = self.cleaned_data.get('numero_deposito')
        num_dep = ContratoLargo.objects.filter(numero_deposito=numero_deposito).exists()
        if len(str(numero_deposito)) > 10:
            raise forms.ValidationError("El numero de deposito tiene que tener maximo 10 caracteres")
        else:
            if num_dep:
                raise forms.ValidationError("El numero de deposito ya existe")
        return numero_deposito

    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if len(str(monto_total)) > 8:
            raise forms.ValidationError("El monto total tiene que tener maximo 8 digitos")
        return monto_total

    def clean_monto_depositado(self):
        monto_depositado = self.cleaned_data.get('monto_depositado')
        monto_total = self.cleaned_data.get('monto_total')
        if (monto_total < monto_depositado):
            raise forms.ValidationError("El monto depositado no puede ser mayor al monto total")
        else:
            if (monto_total > monto_depositado):
                raise forms.ValidationError("El monto depositado no puede ser menor al monto total")
            else:
                if len(str(monto_depositado)) > 8:
                    raise forms.ValidationError("El monto depositado tiene que tener maximo 8 caracteres")
        return monto_depositado

    def clean_fecha_inicial(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        if (fecha_inicial == None):
            raise forms.ValidationError("Introdusca una fecha inicial")
        return fecha_inicial

    def clean_fecha_final(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')

        if (fecha_final == None):
            raise forms.ValidationError("Introdusca una fecha final")
        else:
            if (fecha_inicial == fecha_final):
                raise forms.ValidationError("La fecha final no puede ser igual a la fecha inicial")
            else:
                if fecha_final < fecha_inicial:
                    raise forms.ValidationError("Fecha final no puede ser menor a la fecha inicial")
        return fecha_final

    def clean_fecha_deposito(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        fecha_deposito = self.cleaned_data.get('fecha_deposito')

        if (fecha_deposito == None):
            raise forms.ValidationError("Introdusca una fecha de deposito")
        else:
            if (fecha_final == None):
                raise forms.ValidationError("Introdusca una fecha inicial o fecha final valida")
            else:
                if (fecha_deposito > fecha_final):
                    raise forms.ValidationError("Fecha de deposito no puede ser mayor a la fecha final")
        return fecha_deposito

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if (lugar == None):
            raise forms.ValidationError("Seleccione un lugar")
        return lugar

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        if (espacio == None):
            raise forms.ValidationError("Seleccione un espacio")
        return espacio


class modal(forms.ModelForm):
    class Meta:
        model = ContratoLargo
        fields = [
            'monto_total',
            'monto_depositado',
            'monto_faltante',
            'porcentaje_multa',
            'estado',
        ]
        widgets = {
            'monto_faltante': forms.NumberInput(
                attrs={'class': 'form-.input', 'placeholder': '1-10 digitos', 'readonly': 'readonly'}),
            'monto_total': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '1-10 digitos', 'readonly': 'readonly'}),
            'monto_depositado': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '1-10 digitos', 'readonly': 'readonly'}),
            'porcentaje_multa': forms.Select(attrs={'class': 'form-control', 'disabled': 'True'}),
            'estado': forms.Select(attrs={'disabled': 'True'}, choices=TRUE_FALSE_CHOICES),
        }


class FiltroFechas(forms.ModelForm):
    class Meta:
        model = ContratoLargo
        fields = ['fecha_inicial', 'fecha_final']
        widgets = {
            'fecha_inicial': forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',),
                                             attrs={'class': 'form-control entrada',
                                                    'placeholder': 'Seleccione la fecha Correcta'}),
            'fecha_final': forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',),
                                           attrs={'class': 'form-control salida',
                                                  'placeholder': 'Seleccione la fecha Correcta'})
        }


class form_lugar(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Lugar.objects.all())

    class Meta:
        model = Lugar
        exclude = []


class Modificar(forms.ModelForm):
    class Meta:
        model = ContratoLargo
        fields = [
            'nombre',
            'dni_nit',
            'fecha_inicial',
            'fecha_final',
            'fecha_deposito',
            'porcentaje_multa',
            'monto_total',
            'monto_depositado',
            'estado',
            'nombre_completo_actividad',
            'numero_factura',
            'numero_deposito',
            'lugar',
            'espacio',
            'monto_faltante',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre'}),
            'dni_nit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'fecha_inicial': forms.DateTimeInput(attrs={'class': 'datein', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'fecha_final': forms.DateTimeInput(attrs={'class': 'datefi', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'fecha_deposito': forms.DateTimeInput(attrs={'class': 'datede', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'porcentaje_multa': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'monto_depositado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'estado': forms.Select(attrs={'disabled': 'True'}, choices=TRUE_FALSE_CHOICES),
            'nombre_completo_actividad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0-255 caracteres'}),
            'numero_factura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'numero_deposito': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'lugar': forms.Select(attrs={'class': 'form-control'}),
            'espacio': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # aqio tienes ir hacer bro
        self.user = kwargs.pop('lugar')
        super(Modificar, self).__init__(*args, **kwargs)
        self.fields['espacio'].required = False
        # asi vuelves tus campos no requeridos
        self.fields['monto_faltante'].required = False
        no_lugar = []
        no_lugar.append(('', '---------'))
        # print(User_lugar.objects.filter(user_id__id=self.user))
        # lugar_trabajo_id
        # i=1
        # if i > 0:
        for item in User_lugar.objects.filter(lugar_trabajo_id__id=self.user):
            lugares = get_object_or_404(Lugar, id=item.lugar_trabajo.id)
            no_lugar.append((lugares.id, lugares.name))
            # i=i-1
            break
            # self.fields['lugar'] = forms.ModelChoiceField(queryset=Lugar.objects.values_list('Lugar',flat=True).filter(id=item.lugar_trabajo.id))
        print(no_lugar)
        self.fields['lugar'] = forms.ChoiceField(choices=no_lugar, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 255:
            raise forms.ValidationError("El nombre tiene que tener maximo 255 caracteres")
        return nombre

    def clean_dni_nit(self):
        dni_nit = self.cleaned_data.get('dni_nit')
        if len(str(dni_nit)) > 10:
            raise forms.ValidationError("El numero de DNI/NIT tiene que tener maximo 10 caracteres")
        else:
            return dni_nit

    def clean_nombre_completo_actividad(self):
        nombre_completo_actividad = self.cleaned_data.get('nombre_completo_actividad')
        if len(nombre_completo_actividad) > 255:
            raise forms.ValidationError("El nombre de la actividad tiene que tener maximo 255 caracteres")
        return nombre_completo_actividad

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        if len(str(numero_factura)) > 10:
            raise forms.ValidationError("El numero de factura tiene que tener maximo 10 caracteres")
        return numero_factura

    def clean_numero_deposito(self):
        numero_deposito = self.cleaned_data.get('numero_deposito')
        if len(str(numero_deposito)) > 10:
            raise forms.ValidationError("El numero de deposito tiene que tener maximo 10 caracteres")
        else:
            return numero_deposito

    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if len(str(monto_total)) > 8:
            raise forms.ValidationError("El monto total tiene que tener maximo 8 digitos")
        return monto_total

    def clean_monto_depositado(self):
        monto_depositado = self.cleaned_data.get('monto_depositado')
        monto_total = self.cleaned_data.get('monto_total')
        if (monto_total < monto_depositado):
            raise forms.ValidationError("El monto depositado no puede ser mayor al monto total")
        else:
            if len(str(monto_depositado)) > 8:
                raise forms.ValidationError("El monto depositado tiene que tener maximo 8 digitos")
        return monto_depositado

    def clean_fecha_inicial(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        if (fecha_inicial == None):
            raise forms.ValidationError("Introdusca una fecha inicial")
        return fecha_inicial

    def clean_fecha_final(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')

        if (fecha_final == None):
            raise forms.ValidationError("Introdusca una fecha final")
        else:
            if (fecha_inicial == fecha_final):
                raise forms.ValidationError("La fecha final no puede ser igual a la fecha inicial")
            else:
                if fecha_final < fecha_inicial:
                    raise forms.ValidationError("Fecha final no puede ser menor a la fecha inicial")
        return fecha_final

    def clean_fecha_deposito(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        fecha_deposito = self.cleaned_data.get('fecha_deposito')

        if (fecha_deposito == None):
            raise forms.ValidationError("Introdusca una fecha de deposito")
        else:
            if (fecha_final == None):
                raise forms.ValidationError("Introdusca una fecha inicial o fecha final valida")
            else:
                if (fecha_deposito > fecha_final):
                    raise forms.ValidationError("Fecha de deposito no puede ser mayor a la fecha final")
        return fecha_deposito

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if (lugar == None):
            raise forms.ValidationError("Seleccione un lugar")
        return lugar

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        if (espacio == None):
            raise forms.ValidationError("Seleccione un espacio")
        return espacio


class ModificarCor(forms.ModelForm):
    class Meta:
        model = ContratoLargo
        fields = [
            'nombre',
            'dni_nit',
            'fecha_inicial',
            'fecha_final',
            'fecha_deposito',
            'monto_total',
            'monto_depositado',
            'nombre_completo_actividad',
            'numero_factura',
            'numero_deposito',
            'lugar',
            'espacio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre'}),
            'dni_nit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'fecha_inicial': forms.DateTimeInput(attrs={'class': 'datein', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'fecha_final': forms.DateTimeInput(attrs={'class': 'datefi', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'fecha_deposito': forms.DateTimeInput(attrs={'class': 'datede', 'placeholder': 'dd/mm/aaaa hh:mm'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'monto_depositado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'nombre_completo_actividad': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': '0-255 caracteres'}),
            'numero_factura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'numero_deposito': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-10 digitos'}),
            'lugar': forms.Select(attrs={'class': 'form-control'}),
            'espacio': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['espacio'].required = False

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) > 255:
            raise forms.ValidationError("El nombre tiene que tener maximo 255 caracteres")
        return nombre

    def clean_dni_nit(self):
        dni_nit = self.cleaned_data.get('dni_nit')
        if len(str(dni_nit)) > 10:
            raise forms.ValidationError("El numero de DNI/NIT tiene que tener maximo 10 caracteres")
        else:
            return dni_nit

    def clean_nombre_completo_actividad(self):
        nombre_completo_actividad = self.cleaned_data.get('nombre_completo_actividad')
        if len(nombre_completo_actividad) > 255:
            raise forms.ValidationError("El nombre de la actividad tiene que tener maximo 255 caracteres")
        return nombre_completo_actividad

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        if len(str(numero_factura)) > 10:
            raise forms.ValidationError("El numero de factura tiene que tener maximo 10 caracteres")
        return numero_factura

    def clean_numero_deposito(self):
        numero_deposito = self.cleaned_data.get('numero_deposito')
        if len(str(numero_deposito)) > 10:
            raise forms.ValidationError("El numero de deposito tiene que tener maximo 10 caracteres")
        else:
            return numero_deposito

    def clean_monto_total(self):
        monto_total = self.cleaned_data.get('monto_total')
        if len(str(monto_total)) > 8:
            raise forms.ValidationError("El monto total tiene que tener maximo 8 digitos")
        return monto_total

    def clean_monto_depositado(self):
        monto_depositado = self.cleaned_data.get('monto_depositado')
        monto_total = self.cleaned_data.get('monto_total')
        if (monto_total < monto_depositado):
            raise forms.ValidationError("El monto depositado no puede ser mayor al monto total")
        else:
            if (monto_total > monto_depositado):
                raise forms.ValidationError("El monto depositado no puede ser menor al monto total")
            else:
                if len(str(monto_depositado)) > 8:
                    raise forms.ValidationError("El monto depositado tiene que tener maximo 8 caracteres")
        return monto_depositado

    def clean_fecha_inicial(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        if (fecha_inicial == None):
            raise forms.ValidationError("Introdusca una fecha inicial")
        return fecha_inicial

    def clean_fecha_final(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')

        if (fecha_final == None):
            raise forms.ValidationError("Introdusca una fecha final")
        else:
            if (fecha_inicial == fecha_final):
                raise forms.ValidationError("La fecha final no puede ser igual a la fecha inicial")
            else:
                if fecha_final < fecha_inicial:
                    raise forms.ValidationError("Fecha final no puede ser menor a la fecha inicial")
        return fecha_final

    def clean_fecha_deposito(self):
        fecha_inicial = self.cleaned_data.get('fecha_inicial')
        fecha_final = self.cleaned_data.get('fecha_final')
        fecha_deposito = self.cleaned_data.get('fecha_deposito')

        if (fecha_deposito == None):
            raise forms.ValidationError("Introdusca una fecha de deposito")
        else:
            if (fecha_final == None):
                raise forms.ValidationError("Introdusca una fecha inicial o fecha final valida")
            else:
                if (fecha_deposito > fecha_final):
                    raise forms.ValidationError("Fecha de deposito no puede ser mayor a la fecha final")
        return fecha_deposito

    def clean_lugar(self):
        lugar = self.cleaned_data.get('lugar')
        if (lugar == None):
            raise forms.ValidationError("Seleccione un lugar")
        return lugar

    def clean_espacio(self):
        espacio = self.cleaned_data.get('espacio')
        if (espacio == None):
            raise forms.ValidationError("Seleccione un espacio")
        return espacio
