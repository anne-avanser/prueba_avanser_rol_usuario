import unittest
import io
import os
import sys
import django
from datetime import datetime

# Configurar ruta base del proyecto 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Cargar configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PruebaUsuarios.settings')
django.setup()

# Se crea un "loader" de unittest que buscará todos los archivos de pruebas
# que comiencen con "test_" dentro de la carpeta appPrueba/tests
loader = unittest.TestLoader()
# discover() busca recursivamente todos los archivos test_*.py y los agrupa en un "suite" de pruebas
suite = loader.discover(start_dir='appPrueba/tests', pattern='test_*.py')

# Se crea un flujo de texto en memoria para capturar el resultado de las pruebas
stream = io.StringIO()
# Se configura el "runner" que ejecutará las pruebas con un nivel de detalle (verbosity) = 2
runner = unittest.TextTestRunner(stream=stream, verbosity=2)
result = runner.run(suite)

# Se crea o sobrescribe un archivo en la carpeta de pruebas con la salida completa del test
with open('appPrueba/tests/test_output.txt', 'w', encoding='utf-8') as f:
    f.write(stream.getvalue())

# Crear reporte HTML
html = f"""
<html>
<head>
<meta charset='utf-8'>
<title>Reporte de Pruebas Automatizadas</title>
<style>
body {{ font-family: Arial; background-color: #f9f9f9; padding: 20px; }}
h1 {{ color: #39A900; }}
pre {{ background: #eee; padding: 15px; border-radius: 6px; }}
</style>
</head>
<body>
<h1>Reporte de Pruebas Automatizadas (Unittest)</h1>
<p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<hr>
<pre>{stream.getvalue()}</pre>
</body>
</html>
"""

with open('appPrueba/tests/test_report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(stream.getvalue())  # para mostrar los tests en pantalla

print(" Pruebas ejecutadas correctamente.")
print(" Reporte HTML generado en: appPrueba/tests/test_report.html")
print(" Resultado en texto: appPrueba/tests/test_output.txt")
