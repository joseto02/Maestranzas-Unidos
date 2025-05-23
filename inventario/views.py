from django.shortcuts import render, redirect
from .models import Producto
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