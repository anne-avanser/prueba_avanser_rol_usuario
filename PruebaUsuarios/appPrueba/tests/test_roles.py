
import os
import sys
import unittest
from datetime import datetime

# IMPORTAR el runner HTML 
try:
    from HtmlTestRunner import HTMLTestRunner
except Exception as e:
    print("ERROR: no se pudo importar HtmlTestRunner. Instálalo con:\n  pip install html-testRunner")
    raise

# Intentos para añadir la ruta del proyecto al PYTHONPATH
def ensure_project_path():
    this_file = os.path.abspath(__file__)
    tried = []
    # construimos candidatos: 2, 3, 4 niveles arriba — cubre estructuras comunes
    for up in (2, 3, 4):
        candidate = this_file
        for _ in range(up):
            candidate = os.path.dirname(candidate)
        tried.append(candidate)
        if os.path.exists(os.path.join(candidate, 'manage.py')) or os.path.exists(os.path.join(candidate, 'PruebaUsuarios', 'settings.py')):
            if candidate not in sys.path:
                sys.path.insert(0, candidate)
            return candidate, tried

    fallback = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if fallback not in sys.path:
        sys.path.insert(0, fallback)
    return fallback, tried

project_path, tried_paths = ensure_project_path()

# DIAGNÓSTICO rápido en caso de fallo posterior
print("DEBUG: cwd =", os.getcwd())
print("DEBUG: sys.path (primeros 5) =", sys.path[:5])
print("DEBUG: project_path used =", project_path)
print("DEBUG: tried paths =", tried_paths)

# -------------------------
# Configurar DJANGO_SETTINGS_MODULE y ejecutar django.setup()
# -------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PruebaUsuarios.settings')

try:
    import django
    django.setup()
except Exception as e:
    # Si hay error aquí, mostramos info útil y relanzamos
    print("\nERROR al inicializar Django. Información del error:")
    raise

# -------------------------
# Ahora que Django está inicializado, importar modelos
# -------------------------
try:
    from appPrueba.models import Rol
except Exception as e:
    print("\nERROR al importar appPrueba.models. Comprueba que:")
    print("- La app 'appPrueba' tiene __init__.py")
    print("- La estructura de carpetas es correcta (ver DEBUG arriba)")
    raise

class TestRol(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba: limpia tabla Rol"""
        Rol.objects.all().delete()

    def test_post_crear_rol(self):
        rol = Rol.objects.create(nombre_rol="Administrador")
        self.assertEqual(rol.nombre_rol, "Administrador")

    def test_get_listar_roles(self):
        Rol.objects.create(nombre_rol="Usuario")
        roles = Rol.objects.all()
        self.assertGreater(len(roles), 0)

    def test_get_obtener_rol_por_id(self):
        rol = Rol.objects.create(nombre_rol="Supervisor")
        rol_encontrado = Rol.objects.get(id_rol=rol.id_rol)
        self.assertEqual(rol_encontrado.nombre_rol, "Supervisor")

    def test_put_editar_rol(self):
        rol = Rol.objects.create(nombre_rol="Temporal")
        rol.nombre_rol = "Editado"
        rol.save()
        self.assertEqual(Rol.objects.get(id_rol=rol.id_rol).nombre_rol, "Editado")

    def test_delete_eliminar_rol(self):
        rol = Rol.objects.create(nombre_rol="Eliminar")
        rol_id = rol.id_rol
        rol.delete()
        self.assertFalse(Rol.objects.filter(id_rol=rol_id).exists())


# -------------------------
# Ejecución y reporte
# -------------------------
if __name__ == "__main__":
    # Directorio de reportes (dentro de la app/tests para evitar confusión)
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.join(tests_dir, "reports")
    os.makedirs(report_dir, exist_ok=True)

    report_file = os.path.join(report_dir, f"reporte_roles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

    # Cargar suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRol)

    # 1) Ejecutar y mostrar en consola (ok / FAIL / ERROR)
    runner_console = unittest.TextTestRunner(verbosity=2)
    result = runner_console.run(suite)

    # 2) Generar reporte HTML (HtmlTestRunner)
    # HtmlTestRunner quiere la suite sin haber sido alterada: recargamos la suite
    suite_for_html = unittest.TestLoader().loadTestsFromTestCase(TestRol)
    with open(report_file, "w", encoding="utf-8") as report:
        runner_html = HTMLTestRunner(stream=report, report_title="Reporte de Pruebas - Roles", descriptions=True)
        runner_html.run(suite_for_html)

    print(f"\n Reporte generado en: {report_file}")
