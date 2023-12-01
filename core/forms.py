from django import forms
from .models import Medico,Paciente,Secretaria,Reserva

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class UsuarioUserForm(UserCreationForm):
    # Campo adicional para seleccionar el tipo de grupo
    TIPO_GRUPO_CHOICES = (
        ('paciente', 'Paciente'),
        ('secretaria', 'Secretaria'),
        ('medico', 'Medico'),
    )
    tipo_grupo = forms.ChoiceField(choices=TIPO_GRUPO_CHOICES)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "tipo_grupo"]
        
        

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