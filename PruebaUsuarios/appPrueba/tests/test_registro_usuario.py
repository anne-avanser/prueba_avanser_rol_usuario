import unittest # Permite crear y ejecutar pruebas unitarias en Python
import os         # Sirve para manipular rutas y archivos del sistema operativo
import sys        # Permite modificar la ruta de búsqueda de módulos (sys.path)
import django     # Se utiliza para configurar e inicializar el entorno Django

#CONFIGURAR RUTA DEL PROYECTO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

#CONFIGURAR ENTORNO DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PruebaUsuarios.settings')
django.setup() # Se inicializa Django para poder usar sus modelos dentro de este archivo

from appPrueba.models import Rol, Usuario

class TestRegistroUsuario(unittest.TestCase):

    def setUp(self):  # Método setUp(): se ejecuta antes de cada test
        Rol.objects.all().delete()  # Se eliminan todos los registros existentes para evitar interferencias
        Usuario.objects.all().delete()

        self.rol_admin = Rol.objects.create(nombre_rol='admin')
        self.rol_aprendiz = Rol.objects.create(nombre_rol='aprendiz')
        self.rol_funcionario = Rol.objects.create(nombre_rol='funcionario')

     # PRUEBA 1: Registro correcto de usuario
    def test_registrar_usuario_correctamente(self):
        """Registrar un usuario con un rol existente"""
        usuario = Usuario.objects.create(
            nombre='Salome',
            apellido='Gironza',
            tipo_documento='CC',
            documento='12345678',
            correo='salo12@gmail.com',
            telefono='3124567890',
            id_rol=self.rol_funcionario,
            contrasenia='Abc12345'
        )
        self.assertEqual(usuario.id_rol.nombre_rol, 'funcionario')
        self.assertEqual(usuario.nombre, 'Salome')

    # PRUEBA 2: No permitir usuario sin rol
    def test_no_permitir_usuario_sin_rol(self):
        """Verifica que no se puede crear un usuario sin rol"""
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nombre='Carlos',
                apellido='Torres',
                tipo_documento='CC',
                documento='98765432',
                correo='carlos@gmail.com',
                contrasenia='Abc12345',
                id_rol=None
            )

    # PRUEBA 3: Documento único
    def test_documento_unico(self):
        """Verifica que el documento sea único"""
        Usuario.objects.create(
            nombre='Luis',
            apellido='Gomez',
            tipo_documento='CC',
            documento='111222333',
            correo='luis@gmail.com',
            id_rol=self.rol_admin,
            contrasenia='Abc12345'
        )
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nombre='Luis',
                apellido='Gomez',
                tipo_documento='CC',
                documento='111222333',  # repetido
                correo='luis2@gmail.com',
                id_rol=self.rol_admin,
                contrasenia='Abc12345'
            )

     # Método tearDown(): se ejecuta después de cada test
    def tearDown(self):
        Usuario.objects.all().delete()
        Rol.objects.all().delete()

# Permite ejecutar las pruebas desde la terminal con:
#   python nombre_del_archivo.py
if __name__ == '__main__':
    unittest.main()
