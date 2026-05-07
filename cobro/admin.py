from django.contrib import admin


from .models import Cliente
from .models import Vehiculo

admin.site.register(Cliente)
admin.site.register(Vehiculo)