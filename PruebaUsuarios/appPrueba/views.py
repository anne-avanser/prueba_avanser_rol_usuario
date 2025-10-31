import re
from django.shortcuts import render
from appPrueba.models import Rol, Usuario

def registrar_rol(request):
    errores = []
    exito = None

    if request.method == 'POST':
        nombre_rol = request.POST['nombre_rol'].strip()

        # Validaciones
        if not nombre_rol:
            errores.append("El nombre del rol no puede estar vacío.")
        elif not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre_rol):
            errores.append("El nombre del rol solo puede contener letras.")
        elif Rol.objects.filter(nombre_rol__iexact=nombre_rol).exists():
            errores.append("Ya existe un rol con ese nombre.")

        if not errores:
            Rol.objects.create(nombre_rol=nombre_rol)
            exito = f"Rol '{nombre_rol}' creado correctamente."

    roles = Rol.objects.all().order_by('nombre_rol')
    return render(request, 'registro_rol.html', {
        'roles': roles,
        'errores': errores,
        'exito': exito
    })

def registrar_usuario(request):
    errores = []

    if request.method == 'POST':
        nombre = request.POST['nombre'].strip()
        apellido = request.POST['apellido'].strip()
        tipo_documento = request.POST['tipo_documento']
        documento = request.POST['documento'].strip()
        correo = request.POST['correo'].strip()
        telefono = request.POST['telefono'].strip()
        contrasenia = request.POST['contrasenia']
        rol_id = request.POST['rol']

        # VALIDACIONES
        # Campos vacíos
        if not all([nombre, apellido, tipo_documento, documento, correo, contrasenia, rol_id]):
            errores.append("Todos los campos obligatorios deben estar completos.")

        # Validar solo letras en nombre/apellido
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", nombre):
            errores.append("El nombre solo puede contener letras.")
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", apellido):
            errores.append("El apellido solo puede contener letras.")

        # Correo válido
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            errores.append("El correo electrónico no es válido. Debe incluir '@' y un dominio válido (ej: .com, .edu, .co).")

        # Contraseña segura
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', contrasenia):
            errores.append("La contraseña debe tener mínimo 8 caracteres, incluir mayúsculas, minúsculas y números.")

        # Documento solo números
        if not documento.isdigit():
            errores.append("El documento solo debe contener números.")

        # Teléfono solo números (opcional)
        if telefono and not telefono.isdigit():
            errores.append("El teléfono solo debe contener números.")

        # Rol válido
        try:
            rol = Rol.objects.get(id_rol=rol_id)
        except Rol.DoesNotExist:
            errores.append("Debe seleccionar un rol válido.")
            rol = None

        # Correo o documento duplicado
        if Usuario.objects.filter(correo=correo).exists():
            errores.append("El correo ya está registrado.")
        if Usuario.objects.filter(documento=documento).exists():
            errores.append("El documento ya está registrado.")

        # Si hay errores, devolverlos al formulario
        if errores:
            roles = Rol.objects.all()
            return render(request, 'registro_usuario.html', {'roles': roles, 'errores': errores})

        # Guardar usuario si todo es válido
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

        return render(request, 'registro_exitoso.html', {'nombre': nombre})

    # GET
    roles = Rol.objects.all()
    return render(request, 'registro_usuario.html', {'roles': roles})
