import unittest
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PruebaUsuarios.settings')
django.setup()

from appPrueba.models import Rol, Usuario

# PRUEBA 1: Crear un rol correctamente
class TestRol(unittest.TestCase):
    """Pruebas unitarias para la tabla Rol y su relación con Usuario"""

    def setUp(self):
        Rol.objects.all().delete()
        Usuario.objects.all().delete()

    def test_crear_rol(self):
        """Debe crear un rol correctamente"""
        rol = Rol.objects.create(nombre_rol='instructor')
        self.assertEqual(rol.nombre_rol, 'instructor')
        self.assertIsNotNone(rol.id_rol)

    # PRUEBA 2: No permitir roles duplicados
    def test_no_permitir_rol_duplicado(self):
        """No debe permitir roles con nombres duplicados"""
        Rol.objects.create(nombre_rol='admin')
        with self.assertRaises(Exception):
            Rol.objects.create(nombre_rol='admin')
            
    # PRUEBA 3: Verificar relación Rol - Usuario
    def test_relacion_usuario_rol(self):
        """Debe poder asociar un usuario a un rol existente"""
        rol_aprendiz = Rol.objects.create(nombre_rol='aprendiz')
        usuario = Usuario.objects.create(
            nombre='Laura',
            apellido='Mendoza',
            tipo_documento='CC',
            documento='789654123',
            correo='laura@example.com',
            contrasenia='Abc12345',
            id_rol=rol_aprendiz
        )
        self.assertEqual(usuario.id_rol.nombre_rol, 'aprendiz')

    # PRUEBA 4: Eliminación en cascada
    def test_eliminar_rol_elimina_usuarios(self):
        """Al eliminar un rol, también deben eliminarse los usuarios relacionados (CASCADE)"""
        rol = Rol.objects.create(nombre_rol='temporal')
        Usuario.objects.create(
            nombre='Juan',
            apellido='Pérez',
            tipo_documento='CC',
            documento='111222999',
            correo='juan@example.com',
            contrasenia='Abc12345',
            id_rol=rol
        )

        rol.delete()
        self.assertEqual(Usuario.objects.count(), 0)

    # MÉTODO tearDown(): Se ejecuta después de cada prueba
    def tearDown(self):
        Usuario.objects.all().delete()
        Rol.objects.all().delete()


if __name__ == '__main__':
    unittest.main()
