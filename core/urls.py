from django.urls import path
from .views import  base,form,login,reserva,reserva_exitosa,editar_reserva,eliminar_reserva,realizar_pago

urlpatterns=[
  
    path('',base,name="base"),
    path('form/',form, name ="form"),
    path('login',login, name="login"),
    path('reserva/',reserva, name="reserva"),
    path('reserva_exitosa/',reserva_exitosa, name='reserva_exitosa'),
    path('reserva/<int:reserva_id>/editar/', editar_reserva, name='editar_reserva'),
    path('reserva/<int:reserva_id>/eliminar/', eliminar_reserva, name='eliminar_reserva'),
    path('reserva/<int:reserva_id>/realizar_pago/', realizar_pago, name='realizar_pago'),

]