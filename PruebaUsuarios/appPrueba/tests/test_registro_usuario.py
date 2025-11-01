import unittest
import os
import sys
import django
import io
from datetime import datetime

# CONFIGURAR RUTA DEL PROYECTO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# CONFIGURAR ENTORNO DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PruebaUsuarios.settings')
django.setup()

from appPrueba.models import Rol, Usuario


class TestRegistroUsuario(unittest.TestCase):
    """Pruebas unitarias del módulo de usuarios."""

    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        Usuario.objects.all().delete()
        self.rol, creado = Rol.objects.get_or_create(nombre_rol='Aprendiz')

    # PRUEBA 1: Registrar usuario  (POST)
    def test_registrar_usuario(self):
        usuario = Usuario.objects.create(
            nombre='Juan',
            apellido='Pérez',
            tipo_documento='CC',
            documento='123456',
            correo='juanperez@gmail.com',
            telefono='3123456789',
            id_rol=self.rol,
            estado=1,
            contrasenia='ClaveSegura123'
        )
        self.assertIsNotNone(usuario.id_usuario)
        self.assertEqual(usuario.id_rol, self.rol)

    # PRUEBA 2: No permitir usuario sin rol
    def test_no_permitir_usuario_sin_rol(self):
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nombre='Ana',
                apellido='Gómez',
                tipo_documento='CC',
                documento='654321',
                correo='ana@gmail.com',
                telefono='3000000000',
                id_rol=None,
                estado=1,
                contrasenia='ClaveSegura123'
            )


    # PRUEBA 3: Validar relación usuario-rol (GET)
    def test_relacion_usuario_rol(self):
        usuario = Usuario.objects.create(
            nombre='Carlos',
            apellido='Ruiz',
            tipo_documento='CC',
            documento='888888',
            correo='carlos@gmail.com',
            telefono='3110000000',
            id_rol=self.rol,
            estado=1,
            contrasenia='ClaveSegura123'
        )
        self.assertEqual(usuario.id_rol.nombre_rol, 'Aprendiz')

    # PRUEBA 4: Actualizar datos del usuario (PUT)
    def test_actualizar_usuario(self):
        usuario = Usuario.objects.create(
            nombre='Laura',
            apellido='Torres',
            tipo_documento='CC',
            documento='999999',
            correo='lauraemail.com',
            telefono='3001112233',
            id_rol=self.rol,
            estado=1,
            contrasenia='abc'
        )
        usuario.telefono = '3200000000'
        usuario.correo = 'laura@nuevo.com'
        usuario.save()

        actualizado = Usuario.objects.get(id_usuario=usuario.id_usuario)
        self.assertEqual(actualizado.telefono, '3200000000')
        self.assertEqual(actualizado.correo, 'laura@nuevo.com')


# ==============================================
# EJECUCIÓN INDIVIDUAL CON REPORTE HTML
# ==============================================
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRegistroUsuario)

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    total = result.testsRun
    errores = len(result.errors)
    fallos = len(result.failures)
    exitosos = total - errores - fallos
    porcentaje = (exitosos / total * 100) if total > 0 else 0

    # Crear reporte HTML manualmente
    html = f"""
    <html>
    <head><meta charset='utf-8'><title>Reporte de Pruebas - Usuarios</title></head>
    <body style="font-family:Arial;background:#f9f9f9;padding:20px;">
    <h1 style="color:#39A900;">Reporte de Pruebas - Módulo Usuarios</h1>
    <p><b>Fecha:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><b>Total pruebas:</b> {total}</p>
    <p><b>Aprobadas:</b> {exitosos}</p>
    <p><b>Fallidas:</b> {fallos}</p>
    <p><b>Errores:</b> {errores}</p>
    <p><b>Porcentaje éxito:</b> {porcentaje:.2f}%</p>
    <hr>
    <pre>{stream.getvalue()}</pre>
    </body></html>
    """

    # Guardar archivo HTML
    ruta_reporte = os.path.join(os.path.dirname(__file__), 'test_report_usuarios.html')
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write(html)

    print(stream.getvalue())
    print(f"Reporte HTML generado: {ruta_reporte}")
