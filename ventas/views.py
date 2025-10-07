from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Cliente, Pedido
from .forms import ClienteForm, PedidoForm

def home(request):
    total_clientes = Cliente.objects.count()
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='PENDIENTE').count()
    
    context = {
        'total_clientes': total_clientes,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
    }
    return render(request, 'home.html', context)

# Vistas para Clientes
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Nuevo Cliente'})

def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    pedidos = cliente.pedidos.all()
    return render(request, 'clientes/detalle_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos
    })

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form_cliente.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})

# Vistas para Pedidos
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/form_pedido.html', {'form': form, 'titulo': 'Nuevo Pedido'})

def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})

def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, request.FILES, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('detalle_pedido', pk=pedido.pk)
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/form_pedido.html', {
        'form': form,
        'titulo': 'Editar Pedido'
    })

def eliminar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'pedidos/confirmar_eliminar.html', {'pedido': pedido})