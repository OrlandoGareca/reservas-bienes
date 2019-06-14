# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.


class Lugar(models.Model):
    name = models.CharField(max_length=80)
    #personal = models.ForeignKey(User)
    def __str__(self):
        return '{}'.format(self.name)

class Espacio(models.Model):
    name = models.CharField(max_length=80)
    estado = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    

    def __str__(self):
        return '{}'.format(self.name)

class promediomulta(models.Model):

    valor = models.FloatField(max_length=7)
    def __str__(self):
        return '{}'.format(self.valor)
    class Meta:
        ordering = ["id"]

class ContratoLargo(models.Model):
    # si no hay id tonce django lo pone autoincrementable
    id = models.AutoField( max_length=10,primary_key=True)
    user = models.ForeignKey(User)
    nombre = models.CharField(max_length=50,blank=True)
    dni_nit= models.BigIntegerField(null=True,validators=[MaxValueValidator(10000000000),MinValueValidator(0)])
    fecha_inicial = models.DateTimeField(max_length=16)
    fecha_final = models.DateTimeField(max_length=16)
    fecha_deposito = models.DateTimeField(max_length=16)
    monto_total = models.BigIntegerField(null=True,validators=[MinValueValidator(1)])
    monto_depositado = models.BigIntegerField(null=True,validators=[MaxValueValidator(monto_total),MinValueValidator(1)])
    monto_faltante = models.BigIntegerField(null=True,validators=[MinValueValidator(0)])
    nombre_completo_actividad = models.CharField(max_length=255,blank=True)
    numero_factura = models.BigIntegerField(null=True,validators=[MaxValueValidator(10000000000),MinValueValidator(0)])
    numero_deposito = models.BigIntegerField(null=True,validators=[MaxValueValidator(10000000000),MinValueValidator(0)])
    #lugar = models.ForeignKey(Lugar,null=True,blank=True)
    lugar =models.IntegerField(null=True,blank=True)
    espacio = models.ForeignKey(Espacio,null=True,blank=True)
    estado = models.BooleanField(default=True)
    porcentaje_multa=models.ForeignKey(promediomulta,null=True,blank=True)
    mult_dia=models.PositiveIntegerField(null=True)
    
    #
    def __str__(self):
        return "%s" % self.nombre_completo_actividad

    class Meta:
        ordering = ["id"]
        permissions = (
            ('ver_formLic', 'ver formulario licenciada'),
            ('ver_formUsr', 'Ver formulario usuario'),
            ('editarUsr', 'Ver editar usuario'),
            ('Registrar', 'insertar registros'),
            ('FiltroLIc', 'filtrado fechas lugar'),
            
        )
#ContratoLargo.objects.values('monto_faltante').annotate(resta=int('monto_total') - int('monto_depositado'))
class User_lugar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lugar_trabajo = models.ForeignKey(Lugar, on_delete=models.CASCADE)

