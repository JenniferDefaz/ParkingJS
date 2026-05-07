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