from django.shortcuts import render,redirect
from .forms import UsuarioUserForm,ReservaForm,PagarReserva
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group 
from.models import Reserva





def form(request):
    if request.method == 'POST':
        formulario = UsuarioUserForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.save()

            # Acceder al tipo de grupo seleccionado en el formulario
            tipo_grupo = formulario.cleaned_data["tipo_grupo"]

            # Asignar el grupo correspondiente al usuario creado
            if tipo_grupo == 'Paciente':
                group = Group.objects.get(name='Paciente')
            elif tipo_grupo == 'Secretaria':
                group = Group.objects.get(name='Secretaria')
            elif tipo_grupo == 'Medico':
                group = Group.objects.get(name='Medico')
            else:
                group = None

            if group:
                group.user_set.add(usuario)
            # Autenticar y loguear al usuario recién creado
            user = authenticate(username=usuario.username, password=formulario.cleaned_data["password1"])
            login(request, user)

            return redirect('base')  # Redirigir a la página deseada después de guardar el usuario

    else:
        formulario = UsuarioUserForm()

    data = {'form': formulario}
    return render(request, 'registration/form.html', data)





def base(request):
    return render(request,'core/base.html')  





@login_required
def reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.paciente = request.user  # Asignar el usuario actual a la reserva
            reserva.save()
            return redirect('reserva_exitosa')  # Redirige a la página de reserva exitosa
    else:
        form = ReservaForm()
    
    # Obtener todas las reservas asociadas al usuario actual
    reservas = Reserva.objects.filter(paciente=request.user)
    
    return render(request, 'core/reserva.html', {'form': form, 'reservas': reservas})

@login_required
def reserva_exitosa(request):
    # Verificar si el usuario actual pertenece al grupo 'Secretaria'
    if request.user.groups.filter(name='Secretaria').exists():
        # Si el usuario es del grupo 'Secretaria', mostrar todas las reservas
        reservas = Reserva.objects.all()
    elif request.user.groups.filter(name='Medico').exists():
        # Si el usuario es del grupo 'Medico', mostrar solo las reservas asociadas a ese médico
        reservas = Reserva.objects.filter(medico__usuario=request.user)
    else:
        # Si no es del grupo 'Secretaria' ni 'Medico', mostrar solo las reservas asociadas a ese usuario
        reservas = Reserva.objects.filter(paciente=request.user)
    
    return render(request, 'core/reserva_exitosa.html', {'reservas': reservas})

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('reserva_exitosa')  # Redirige a la página de reserva exitosa
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'core/editar_reserva.html', {'form': form})


@login_required
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reserva_exitosa')  # Redirige a la página de reserva exitosa o a donde desees
    return render(request, 'core/eliminar_reserva.html', {'reserva': reserva})


@user_passes_test(lambda user: user.groups.filter(name='Secretaria').exists())
def realizar_pago(request, reserva_id):
    user_is_secretaria = request.user.groups.filter(name='secretaria').exists()
    # Obtener la instancia de la reserva o devolver un error 404 si no existe
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        # Si la solicitud es un POST, procesar los datos del formulario
        form = PagarReserva(request.POST, instance=reserva)
        if form.is_valid():
            # Si el formulario es válido, guardar los datos de la reserva actualizados
            form.save()
            # Redirigir a la página de éxito de la reserva después de procesar el pago
            return redirect('reserva_exitosa')
    else:
        # Si la solicitud no es un POST, crear una instancia del formulario con la reserva existente
        form = PagarReserva(instance=reserva)

    # Renderizar la plantilla con el formulario apropiado
    return render(request, 'core/realizar_pago.html', {'form': form,'user': request.user})

