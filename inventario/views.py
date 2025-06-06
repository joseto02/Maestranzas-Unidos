from django.shortcuts import render, redirect
from .models import Producto, Movimiento
from .forms import ProductoForm
# Create your views here.

def inicio(request):
    return render(request, 'inventario/inicio.html')

def inventario(request):
    productos = Producto.objects.all()
    return render(request, 'productos/index.html', {'productos': productos})

def crear_producto(request):
    
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('inventario')
    
    return render(request, 'productos/crear.html', {'formulario': formulario})

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('inventario')
    return render(request, 'productos/editar.html', {'formulario': formulario, 'producto': producto})

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('inventario')

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