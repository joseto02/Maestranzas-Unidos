from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Producto, Movimiento
from .forms import ProductoForm, LoginForm, UserRegistroForm, UserUpdateForm
# Create your views here.

def inicio(request):
    return render(request, 'inventario/inicio.html')

def inventario(request):
    productos = Producto.objects.all()
    return render(request, 'productos/index.html', {'productos': productos})

def crear_producto(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        producto = formulario.save()

        # Registrar movimiento de creación
        Movimiento.objects.create(
            componente=producto,
            tipo="creación",
            cantidad=0,
            origen="Nuevo producto",
            responsable=request.user if request.user.is_authenticated else None,
        )

        return redirect('inventario')

    return render(request, 'productos/crear.html', {'formulario': formulario})


def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()

        Movimiento.objects.create(
            componente=producto,
            tipo="edición",
            cantidad=0,
            origen="Modificación manual",
            responsable=request.user if request.user.is_authenticated else None,
        )

        return redirect('inventario')
    
    return render(request, 'productos/editar.html', {'formulario': formulario, 'producto': producto})


def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)

    Movimiento.objects.create(
        componente=producto,
        tipo="eliminación",
        cantidad=0,
        origen=f"Producto eliminado: {producto.nombre}",
        responsable=request.user if request.user.is_authenticated else None,
    )

    producto.delete()
    return redirect('inventario')


@login_required
def listar_productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()
    return render(request, 'productos/index.html', {'productos': productos})

def registrar_entrada(request):
    if request.method == "POST":
        componente_id = request.POST["componente_id"]
        cantidad = int(request.POST["cantidad"])
        origen = request.POST["origen"]

        componente = Producto.objects.get(id=componente_id)
        componente.stock += cantidad
        componente.save()

        Movimiento.objects.create(
            componente=componente,
            tipo="entrada",
            cantidad=cantidad,
            origen=origen,
            responsable=request.user,
        )

        return redirect("inventario") 
    else:
        componentes = Producto.objects.all()
        return render(
            request, "productos/registrar_entrada.html", {"componentes": componentes}
        )


def registrar_salida(request):
    if request.method == "POST":
        componente_id = request.POST["componente_id"]
        cantidad = int(request.POST["cantidad"])
        destino = request.POST["destino"]

        componente = Producto.objects.get(id=componente_id)

        if cantidad > componente.stock:
            return render(
                request,
                "productos/registrar_salida.html",
                {
                    "componentes": Producto.objects.all(),
                    "error": "Stock insuficiente para realizar esta salida.",
                },
            )

        componente.stock -= cantidad
        componente.save()

        Movimiento.objects.create(
            componente=componente,
            tipo="salida",
            cantidad=cantidad,
            destino=destino,
            responsable=request.user,
        )

        return redirect("inventario")
    else:
        componentes = Producto.objects.all()
        return render(
            request, "productos/registrar_salida.html", {"componentes": componentes}
        )


def historial_movimientos(request, componente_id):
    componente = Producto.objects.get(id=componente_id)

    movimientos = Movimiento.objects.filter(componente=componente)

    # Filtro por fecha
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    if fecha_inicio:
        movimientos = movimientos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        movimientos = movimientos.filter(fecha__lte=fecha_fin)

    return render(
        request,
        "productos/historial.html",
        {"componente": componente, "movimientos": movimientos},
    )

# --------------------------------------------------------------------------

def historial_general(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')

    componente = request.GET.get('componente')
    if componente:
        movimientos = movimientos.filter(componente__nombre__icontains=componente)

    return render(request, 'productos/historial_general.html', {'movimientos': movimientos})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('inventario')
                else:
                    return render(request, 'autenticacion/login.html', {'form': form, 'error': 'Cuenta inactiva.'})
            else:
                return render(request, 'autenticacion/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos.'})
    else:
        form = LoginForm()
        return render(request, "autenticacion/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == "POST":
        user_form = UserRegistroForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistroForm()
    return render(request, 'autenticacion/registro.html', {'form': user_form})


@login_required
def editar_usuario(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")

            if password:
                user.set_password(password)
                update_session_auth_hash(
                    request, user
                )  # Mantiene sesión activa tras cambiar contraseña

            user.save()
            return redirect("inventario")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "autenticacion/editar_usuario.html", {"form": form})