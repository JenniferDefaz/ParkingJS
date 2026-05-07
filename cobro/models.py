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

