from django.apps import AppConfig # Clase base que permite configurar las aplicaciones en Django

class ApppruebaConfig(AppConfig):
    # Define el tipo de campo automático por defecto para los modelos
    # 'BigAutoField' crea identificadores primarios (id) tipo BIGINT en la base de datos.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appPrueba' # Debe coincidir con el nombre del directorio donde está ubicada la app.
    
