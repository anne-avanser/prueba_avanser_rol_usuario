from django.db import models

# TABLA ROL
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_rol


# TABLA USUARIO
TIPO_DOCUMENTO = (
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('CE', 'Cédula de Extranjería'),
)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=20, unique=True)
    correo = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    estado = models.SmallIntegerField(default=1)
    contrasenia = models.CharField(max_length=100)

    def __str__(self):
        """Representación legible del usuario (nombre completo y rol)."""
        return f"{self.nombre} {self.apellido} - {self.id_rol.nombre_rol}"
