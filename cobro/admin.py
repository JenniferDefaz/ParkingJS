from django.contrib import admin


from .models import Cliente
from .models import Vehiculo
from .models import Espacio
from .models import Tarifa
from .models import Cobro


admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Espacio)
admin.site.register(Tarifa)
admin.site.register(Cobro)