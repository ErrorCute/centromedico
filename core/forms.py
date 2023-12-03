from django import forms
from .models import Medico,Paciente,Secretaria,Reserva

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group



class UsuarioUserForm(UserCreationForm):
    TIPO_GRUPO_CHOICES = (
        ('paciente', 'Paciente'),
        ('secretaria', 'Secretaria'),
        ('medico', 'Medico'),
    )
    tipo_grupo = forms.ChoiceField(choices=TIPO_GRUPO_CHOICES)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "tipo_grupo"]

    def clean_tipo_grupo(self):
        tipo_grupo = self.cleaned_data['tipo_grupo']
        # Verificar si el grupo seleccionado es uno de los grupos existentes
        if tipo_grupo not in ['paciente', 'secretaria', 'medico']:
            raise forms.ValidationError("El grupo seleccionado no es válido.")
        return tipo_grupo

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo_grupo = self.cleaned_data.get('tipo_grupo')

        if commit:
            user.save()
            # Obtener el grupo existente correspondiente al tipo de grupo seleccionado
            group = Group.objects.get(name=tipo_grupo.capitalize())  # Asegurar la capitalización correcta
            user.groups.add(group)

        return user


from django.forms.widgets import SelectDateWidget

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['medico', 'fecha', 'hora']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = Medico.objects.all()  # Filtrar la lista de médicos disponibles

        # Usar widget de fecha desplegable y calendario
        self.fields['fecha'].widget = SelectDateWidget(attrs={'class': 'form-control', 'id': 'id_fecha'})
        
        # Limitar las opciones de hora a partir de las 10:00 hasta las 17:00
        horas_disponibles = [(f'{hora:02d}:00', f'{hora:02d}:00') for hora in range(10, 18)]  # Generar lista de horas disponibles
        self.fields['hora'].widget = forms.Select(choices=horas_disponibles)
        



class PagarReserva (forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ["estado"]
        
        
class FormularioMedio(forms.ModelForm):
    
    class Meta:
        model = Medico
        exclude=["user"]