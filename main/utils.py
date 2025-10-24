from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage
from .models import Historial
from django.contrib import messages

from django.contrib.auth.models import User
import json

from PIL import Image
import os
from io import BytesIO


# def comprimir_imagen(image, quality):
#     """Comprimir la imagen a una escala determinada"""
#     img = Image.open(image)
#     if img.mode != 'RGB':
#         img = img.convert('RGB')
        
#     output = BytesIO()
#     img.save(output, format='JPEG', quality=quality, optimize=True)
#     output.seek(0)
#     return output
def comprimir_imagen(image, quality):
    """Comprimir la imagen a una escala determinada"""
    try:
        # Verificar si es un objeto InMemoryUploadedFile
        if hasattr(image, 'file'):
            img = Image.open(image.file)
        else:
            # Si es un path o archivo directo
            img = Image.open(image)
            
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        return output
        
    except Exception as e:
        print(f"Error al comprimir imagen: {str(e)}")
        return None


def registrar_accion(accion, modelo_afectado, id_objeto, usuario=None, detalles=None, datos_formulario=None):
    """
    Registra una acción en el historial.
    :param accion: Tipo de acción ('crear', 'editar', 'eliminar').
    :param modelo_afectado: Nombre del modelo afectado (ej. 'Familias', 'Especies').
    :param id_objeto: ID del objeto afectado.
    :param usuario: Usuario que realizó la acción (opcional).
    :param detalles: Información adicional (opcional).
    :param datos_formulario: Diccionario con los datos del formulario (opcional).
    """

    # Extraer el nombre del usuario
    nombre_usuario = usuario.username if hasattr(usuario, 'username') else str(usuario)

    # Convertir el diccionario a JSON string
    datos_formulario_json = json.dumps(datos_formulario, ensure_ascii=False) if datos_formulario else None

    Historial.objects.create(
        accion=accion,
        modelo_afectado=modelo_afectado,
        id_objeto=id_objeto,
        usuario=nombre_usuario,
        detalles=detalles,
        datos_formulario=datos_formulario_json,  # Guardar como JSON string
    )


def validar_archivo(archivo, request):
    """
    Valida el archivo subido.
    :param archivo: Archivo subido (InMemoryUploadedFile).
    :param request: Objeto HttpRequest para agregar mensajes de error.
    :return: True si el archivo es válido, False si no lo es.
    """
    if not archivo:
        return True  # No hay archivo, pero es opcional

    # Validar el tamaño del archivo (límite de 20 MB)
    if archivo.size > 20 * 1024 * 1024: 
        messages.error(request, "El archivo es demasiado grande. El tamaño máximo permitido es 20 MB.")
        return False

    # Validar el tipo de archivo (solo imágenes JPG, JPEG o PNG)
    extensiones_permitidas = ['.jpg', '.jpeg', '.png']
    if not archivo.name.lower().endswith(tuple(extensiones_permitidas)):
        messages.error(request, "Solo se permiten archivos JPG, JPEG o PNG.")
        return False

    return True  # El archivo es válido