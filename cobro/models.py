from django.db import models

# ==================== MODELO CLIENTE ====================
class Cliente(models.Model):
    # Atributos básicos
    id = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=15, unique=True, help_text="Cédula o RUC")
    apellido = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    correo = models.EmailField()
    telefono = models.CharField(max_length=15, default="")
    
    # Estado Civil (según registro civil de Ecuador)
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero/a'),
        ('CASADO', 'Casado/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('VIUDO', 'Viudo/a'),
        ('UNION_LIBRE', 'Unión Libre'),
    ]
    estado_civil = models.CharField(
        max_length=20,
        choices=ESTADO_CIVIL_CHOICES,
        default='SOLTERO'
    )
    
    # Etnia (según registro de Ecuador)
    ETNIA_CHOICES = [
        ('MESTIZO', 'Mestizo/a'),
        ('INDIGENA', 'Indígena'),
        ('AFROECUATORIANO', 'Afroecuatoriano/a'),
        ('MONTUBIO', 'Montubio/a'),
        ('BLANCO', 'Blanco/a'),
        ('OTRO', 'Otro'),
    ]
    etnia = models.CharField(
        max_length=20,
        choices=ETNIA_CHOICES,
        default='MESTIZO'
    )
    
    # Fecha de registro
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.apellido} {self.nombre} - {self.identificacion}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']


###############################################33
# ==================== MODELO VEHÍCULO ====================
class Vehiculo(models.Model):
    # Tipos de vehículo según clasificación ecuatoriana
    TIPO_VEHICULO_CHOICES = [
        ('AUTO', 'Automóvil'),
        ('CAMIONETA', 'Camioneta'),
        ('MOTO', 'Motocicleta'),
        ('CAMION', 'Camión'),
        ('BUS', 'Bus'),
        ('FURGON', 'Furgoneta'),
    ]
    
    # Combustible
    COMBUSTIBLE_CHOICES = [
        ('GASOLINA', 'Gasolina Súper'),
        ('GASOLINA_ECO', 'Gasolina Eco'),
        ('DIESEL', 'Diésel'),
        ('ELECTRICO', 'Eléctrico'),
        ('HIBRIDO', 'Híbrido'),
        ('GAS', 'Gas Licuado'),
    ]
    
    # Atributos principales
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True, help_text="Ej: ABC-1234")
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField(default=2020)
    color = models.CharField(max_length=30)
    tipo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES, default='AUTO')
    combustible = models.CharField(max_length=20, choices=COMBUSTIBLE_CHOICES, default='GASOLINA')
    
    # Relación con cliente (un cliente puede tener muchos vehículos)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='vehiculos'
    )
    
    # Campos adicionales
    observacion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.color})"
    
    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['placa']


###################
# ==================== MODELO ESPACIO ====================
class Espacio(models.Model):
    # Estado del espacio
    ESTADO_CHOICES = [
        ('DISPONIBLE', '✅ Disponible'),
        ('OCUPADO', '🔴 Ocupado'),
        ('MANTENIMIENTO', '🔧 Mantenimiento'),
        ('RESERVADO', '📅 Reservado'),
    ]
    
    # Tipo de vehículo que puede ocupar el espacio
    TIPO_ESPACIO_CHOICES = [
        ('AUTO', 'Automóvil'),
        ('MOTO', 'Motocicleta'),
        ('CAMIONETA', 'Camioneta'),
        ('DISCAPACITADO', 'Persona con Discapacidad'),
        ('MUJER', 'Mujer Embarazada/Con Niños'),
        ('CARGA', 'Vehículo de Carga'),
    ]
    
    # Zona del parqueadero
    ZONA_CHOICES = [
        ('NORTE', 'Zona Norte'),
        ('SUR', 'Zona Sur'),
        ('ESTE', 'Zona Este'),
        ('OESTE', 'Zona Oeste'),
        ('CENTRO', 'Zona Centro'),
        ('VIP', 'Zona VIP'),
    ]
    
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(unique=True, help_text="Número de espacio (1,2,3...)")
    zona = models.CharField(max_length=20, choices=ZONA_CHOICES, default='NORTE')
    tipo_espacio = models.CharField(max_length=20, choices=TIPO_ESPACIO_CHOICES, default='AUTO')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    
    # Tarifa por hora según tipo de espacio
    tarifa_hora = models.DecimalField(max_digits=6, decimal_places=2, default=1.50)
    tarifa_hora_extra = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    
    # Ubicación física
    piso = models.IntegerField(default=1, help_text="Número de piso")
    sector = models.CharField(max_length=50, blank=True, help_text="Ej: Sector A, cerca del ascensor")
    
    # Campos adicionales
    tiene_cargador_electrico = models.BooleanField(default=False)
    tiene_seguridad = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Espacio #{self.numero} - Zona {self.zona} - {self.get_estado_display()}"
    
    class Meta:
        verbose_name = "Espacio"
        verbose_name_plural = "Espacios"
        ordering = ['zona', 'piso', 'numero']

    ###########################
    # ==================== MODELO COBRO ====================
class Cobro(models.Model):
    # Métodos de pago
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', '💵 Efectivo'),
        ('TARJETA_CREDITO', '💳 Tarjeta de Crédito'),
        ('TARJETA_DEBITO', '💳 Tarjeta de Débito'),
        ('TRANSFERENCIA', '🏦 Transferencia Bancaria'),
        ('YAPE', '📱 Yape'),
        ('PLIN', '📱 Plin'),
        ('TRANSACCION', '🔄 Transacción'),
    ]
    
    # Estado del cobro
    ESTADO_COBRO_CHOICES = [
        ('ACTIVO', '🟢 Activo (Vehículo estacionado)'),
        ('PAGADO', '✅ Pagado'),
        ('ANULADO', '❌ Anulado'),
        ('PENDIENTE', '⏳ Pendiente de pago'),
    ]
    
    # Tipo de tarifa
    TARIFA_CHOICES = [
        ('HORA', 'Por Hora'),
        ('DIA', 'Por Día'),
        ('MES', 'Mensual'),
        ('SEMANA', 'Semanal'),
    ]
    
    # Campos principales
    id = models.AutoField(primary_key=True)
    numero_cobro = models.CharField(max_length=20, unique=True, blank=True, help_text="Número de ticket/factura")
    
    # Relaciones
    vehiculo = models.ForeignKey(
        Vehiculo, 
        on_delete=models.CASCADE, 
        related_name='cobros'
    )
    espacio = models.ForeignKey(
        Espacio, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='cobros'
    )
    
    # Fechas
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    
    # Cálculos de tiempo
    horas_estacionado = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    minutos_estacionado = models.IntegerField(default=0)
    
    # Valores económicos
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2, default=1.50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="IVA 15% o 12% según tarifa")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Pago
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODO_PAGO_CHOICES, 
        default='EFECTIVO'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_COBRO_CHOICES, 
        default='ACTIVO'
    )
    tipo_tarifa = models.CharField(
        max_length=10, 
        choices=TARIFA_CHOICES, 
        default='HORA'
    )
    
    # Información adicional
    observacion = models.TextField(blank=True, null=True)
    factura_electronica = models.BooleanField(default=False)
    factura_numero = models.CharField(max_length=50, blank=True, null=True)
    
    # Campos para registro
    creado_por = models.CharField(max_length=100, blank=True, help_text="Usuario que registró")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cobro #{self.numero_cobro} - {self.vehiculo.placa} - Total: ${self.total}"
    
    class Meta:
        verbose_name = "Cobro"
        verbose_name_plural = "Cobros"
        ordering = ['-fecha_ingreso']