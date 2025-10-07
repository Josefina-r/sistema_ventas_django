from django.db import models

# Create your models here.
import os

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='clientes/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    def delete(self, *args, **kwargs):
        if self.foto:
            if os.path.isfile(self.foto.path):
                os.remove(self.foto.path)
        super().delete(*args, **kwargs)

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    producto = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    imagen_producto = models.ImageField(upload_to='pedidos/', blank=True, null=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"
    
    @property
    def total(self):
        return self.cantidad * self.precio_unitario
    
    def delete(self, *args, **kwargs):
        if self.imagen_producto:
            if os.path.isfile(self.imagen_producto.path):
                os.remove(self.imagen_producto.path)
        super().delete(*args, **kwargs)