from django.db import models
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy




class Secretaria(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField()
    
    def __str__(self):
        return self.user.username


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField()
    box=models.IntegerField(default=1)
    valor_consulta =models.IntegerField()
    
    
    def __str__(self):
        return f'Nombre: {self.nombre} Especialidad: {self.especialidad} Box: {self.box}'

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    telefono = models.IntegerField()
    correo = models.EmailField()
    edad = models.IntegerField()
    
    def __str__(self):
        return self.user.username
 
    
# Modelo para las horas disponibles
class Reserva(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado=models.BooleanField(default=False)
    
    def __str__(self):
        return f'Reserva  el {self.fecha} a las {self.hora} para Medico {self.medico}'

        
        

