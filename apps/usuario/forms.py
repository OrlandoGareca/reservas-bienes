from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active', 


        ]
        labels = {
            'username': 'Nombre De Usuario :',
            'first_name': 'Nombre(s) :',
            'last_name': 'Apellido(s) :',
            'email': 'Correo Electronico :',
            'is_staff':'admin',
            'is_active':'superuser',


        }