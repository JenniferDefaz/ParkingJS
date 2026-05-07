from django.contrib import admin


from .models import Cliente
from .models import Vehiculo
from .models import Espacio

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Espacio)