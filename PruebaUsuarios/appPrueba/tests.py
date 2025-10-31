import re  # Módulo para trabajar con expresiones regulares (validaciones de texto)
from django.shortcuts import render  # Permite renderizar plantillas HTML
from appPrueba.models import Rol, Usuario


def registrar_usuario(request):
    """
    Vista principal que muestra el formulario de registro y procesa el envío.
    Incluye validaciones tanto de formato como de lógica de negocio.
    """

    errores = []  # Lista de errores a mostrar en el frontend

    if request.method == 'POST':
        #Captura de datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        tipo_documento = request.POST.get('tipo_documento', '').strip()
        documento = request.POST.get('documento', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        contrasenia = request.POST.get('contrasenia', '').strip()
        rol_id = request.POST.get('rol')

        #VALIDACIONES BACKEND

        # 1. Validar nombre y apellido (solo letras y espacios)
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            errores.append("El nombre solo puede contener letras y espacios.")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellido):
            errores.append("El apellido solo puede contener letras y espacios.")

        # 2. Validar tipo de documento
        if tipo_documento not in ['CC', 'TI', 'CE']:
            errores.append("El tipo de documento no es válido.")

        # 3. Documento solo números
        if not documento.isdigit():
            errores.append("El documento solo debe contener números.")
        elif len(documento) < 5:
            errores.append("El documento debe tener al menos 5 dígitos.")

        # 4. Correo válido
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append("El correo electrónico no es válido. Debe incluir '@' y un dominio válido (ej: .com, .edu, .co).")

        # 5. Teléfono (si lo envía)
        if telefono:
            if not telefono.isdigit():
                errores.append("El teléfono solo debe contener números.")
            elif len(telefono) < 7 or len(telefono) > 15:
                errores.append("El teléfono debe tener entre 7 y 15 dígitos.")

        # 6. Contraseña segura
        # Debe tener al menos una mayúscula, una minúscula, un número y 8 caracteres.
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', contrasenia):
            errores.append("La contraseña debe tener mínimo 8 caracteres, incluir mayúsculas, minúsculas y números.")

        # 7. Rol válido
        try:
            rol = Rol.objects.get(id_rol=rol_id)
        except Rol.DoesNotExist:
            errores.append("Debe seleccionar un rol válido.")
            rol = None

        # 8. Verificar duplicados en BD
        if Usuario.objects.filter(documento=documento).exists():
            errores.append("Ya existe un usuario con ese documento.")
        if Usuario.objects.filter(correo=correo).exists():
            errores.append("Ya existe un usuario con ese correo.")

        # Si hay errores, volver a mostrar el formulario
        if errores:
            roles = Rol.objects.all()
            return render(request, 'registro_usuario.html', {
                'roles': roles,
                'errores': errores,
                'nombre': nombre,
                'apellido': apellido,
                'correo': correo,
                'documento': documento,
                'telefono': telefono
            })

        # Si todo está correcto, registrar el usuario 
        Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            tipo_documento=tipo_documento,
            documento=documento,
            correo=correo,
            telefono=telefono,
            contrasenia=contrasenia,
            id_rol=rol
        )

        # Renderizar página de éxito con el nombre del usuario
        return render(request, 'registro_exitoso.html', {'nombre': nombre})

    # Si es GET (mostrar formulario por primera vez)
    roles = Rol.objects.all()
    return render(request, 'registro_usuario.html', {'roles': roles})
