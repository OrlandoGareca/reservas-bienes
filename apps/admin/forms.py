from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from ..contratos_largos.models import promediomulta

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    #role = forms.ModelChoiceField(queryset=Group.objects.all())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username',
                  'password']
        # excludes = ['']
        
        label = {
            'password': 'password'
        }

    #def __init__(self, *args, **kwargs):
    #    if kwargs.get('instance'):
    #        # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.                
    #        initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
    #        if kwargs['instance'].groups.all():
    #            initial['role'] = kwargs['instance'].groups.all()[0]
    #        else:
    #            initial['role'] = None

    #    forms.ModelForm.__init__(self, *args, **kwargs)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == None:
            raise forms.ValidationError("Escriba sus Nombre(s)")
        else:
            if not first_name.isdigit():    
                raise forms.ValidationError("Nombre(s) no pueden ser numeros")
            else:
                if len(first_name) > 255:
                    raise forms.ValidationError("Nombre(s) son muy extensos")
        return first_name
class PromedioForm(forms.ModelForm):
    valor = forms.FloatField(required=False, max_value=10, min_value=0, widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"})) 
    class Meta:
        model = promediomulta
        fields = ['valor']
        # excludes = ['']
        label = {
            'valor': 'Valor'
        }