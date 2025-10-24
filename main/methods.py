from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from django.db import transaction

# Importar modelos
from login.models import *

from .forms import *

from .utils import registrar_accion, validar_archivo, comprimir_imagen

import json

# Módulos de manejo de imágenes comprimidas
import os

from .forms import CustomUserCreationForm



from .choices import *


####################################### MÉTODO POST #######################################
@login_required
@csrf_protect
def add(request):
    if request.method == 'POST':
        go_to = request.POST.get('go_to') # Diferenciar a dónde van los POST

        ###############################################################
        # Agregar a Familia
        if go_to == 'Familias':
            form = FamiliaForm(request.POST)

            if form.is_valid():
                familia = form.save(commit=False)
                # Guardar la instancia de Familia para obtener su ID
                familia = form.save()
                ############## REGISTRO EN EL HISTORIAL ##############
                # Convertir los datos del formulario a un diccionario
                datos_formulario = {
                    'nombre': form.cleaned_data.get('familia'),
                    'division': form.cleaned_data.get('division'),
                    'descripcion': form.cleaned_data.get('descripcion'),
                    'comentario': form.cleaned_data.get('comentario'),
                    'foto': form.cleaned_data.get('foto'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Familias', familia.id, request.user, detalles='Se agregó una nueva Familia.', datos_formulario=datos_formulario)
                ############## REGISTRO EN EL HISTORIAL ##############

                # Redirigir a la página de familias
                messages.success(request, "Familia agregada exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Familias")
            else:
                # Envío de error si el formulario no es válido
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
        ###############################################################


        ###############################################################
        # Agregar Especie
        if go_to == 'Especies':
            form = EspecieForm(request.POST)

            if form.is_valid():
                especie = form.save(commit=False)
                # Guardar la instancia de Especie para obtener su ID
                especie.save()

                ############## REGISTRO EN EL HISTORIAL ##############
                # Convertir los datos del formulario a un diccionario
                datos_formulario = {
                    'nombre_cientifico': form.cleaned_data.get('nombre_cientifico'),
                    'familia': form.cleaned_data.get('familia'),
                    'codigo': form.cleaned_data.get('codigo'),
                    'nombre_comun': form.cleaned_data.get('nombre_comun'),
                    'foto': form.cleaned_data.get('foto'),
                    'sinonimos': form.cleaned_data.get('sinonimos'),
                    'species_authors': form.cleaned_data.get('species_authors'),
                    'genus': form.cleaned_data.get('genus'),
                    'rank1': form.cleaned_data.get('rank1'),
                    'sp1': form.cleaned_data.get('sp1'),
                    'author1': form.cleaned_data.get('author1'),
                    'sp2': form.cleaned_data.get('sp2'),
                    'author2': form.cleaned_data.get('author2'),
                    'habito': form.cleaned_data.get('habito'),
                    'tallos': form.cleaned_data.get('tallos'),
                    'hojas': form.cleaned_data.get('hojas'),
                    'inflorescencia': form.cleaned_data.get('inflorescencia'),
                    'frutos': form.cleaned_data.get('frutos'),
                    'soros': form.cleaned_data.get('soros'),
                    'distribucion': form.cleaned_data.get('distribucion'),
                    'nota': form.cleaned_data.get('nota'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Especie', especie.id, request.user, detalles='Se agregó una nueva Especie.', datos_formulario=datos_formulario)
                ############## REGISTRO EN EL HISTORIAL ##############

                # Redirigir a la página de Especie
                messages.success(request, "Especie agregada exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Especies")

            else:
                # Envío de error si el formulario no es válido
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
        ###############################################################


        ###############################################################
        # Agregar Especimen
        if go_to == 'Especímenes':
            # form = EspecieForm(request.POST)
            form = EspecimenForm(request.POST, request.FILES)
            
            # print(form.foto)
            if form.is_valid():
                # Revisar que se haya pasado el archivo (No se sabe si es requerido completamente)
                archivo = request.FILES.get('photoname') 

                # Validar el archivo
                if not validar_archivo(archivo, request):
                    return redirect(f"{reverse('main:content')}?item=Especímenes")

                try:
                    # Guardar imágenes al 100% ESPÉCIMEN
                    # fs_original = FileSystemStorage(location='staticfiles/fotos_vivas')
                    fs_original = FileSystemStorage(location='staticfiles/Images_elverde')
                    nombre_archivo = fs_original.save(archivo.name, archivo)
                    
                    # Guardar imágenes al 60% de compresión ESPÉCIMEN
                    medium_compressed = comprimir_imagen(archivo, 60)
                    if medium_compressed:
                        # fs_medium = FileSystemStorage(location='staticfiles/fotos_comp')
                        fs_medium = FileSystemStorage(location='staticfiles/Images_comp')
                        medium_filename = fs_medium.save(archivo.name, medium_compressed)
                    
                    # Guardar imágenes al 95% de compresión - thumbnail ESPÉCIMEN
                    thumb_compressed = comprimir_imagen(archivo, 95)
                    if thumb_compressed:
                        # fs_thumb = FileSystemStorage(location='staticfiles/fotos_vivas/thumb')
                        fs_thumb = FileSystemStorage(location='staticfiles/Images_elverde/thumb/JPEG')
                        thumb_filename = fs_thumb.save(archivo.name, thumb_compressed)
                    
                    # Guardar en la base de datos
                    especimen = form.save(commit=False)
                    especimen.photoname = nombre_archivo
                
                except Exception as e:
                    # Clean up if something fails
                    for path in [archivo]:
                        if path and os.path.exists(path):
                            os.remove(path)
                    messages.error(request, f'Error procesando imagen: {str(e)}')
                    return redirect(f"{reverse('main:content')}?item=Especímenes")

                else:
                    # Guardar sin archivo si no se subió ninguno
                    especimen = form.save(commit=False)

                # Guardar la instancia del Especimen para obtener su ID
                especimen.save()

                ############## REGISTRO EN EL HISTORIAL ##############
                # Convertir los datos del formulario a un diccionario
                datos_formulario = {
                    'familiy': form.cleaned_data.get('familiy'),
                    'species': form.cleaned_data.get('species'),
                    'photoname': nombre_archivo if archivo else None,
                    'barcode': form.cleaned_data.get('barcode'),
                    'accesion': form.cleaned_data.get('accesion'),
                    'collector': form.cleaned_data.get('collector'),
                    'number': form.cleaned_data.get('number'),
                    'addcoll': form.cleaned_data.get('addcoll'),
                    'herb': form.cleaned_data.get('herb'),
                    'day': form.cleaned_data.get('day'),
                    'month': form.cleaned_data.get('month'),
                    'year': form.cleaned_data.get('year'),
                    'division': form.cleaned_data.get('division'),
                    'code': form.cleaned_data.get('code'),
                    'species_authors': form.cleaned_data.get('species_authors'),
                    'detby': form.cleaned_data.get('detby'),
                    'dethdate': form.cleaned_data.get('dethdate'),
                    'plantdesc': form.cleaned_data.get('plantdesc'),
                    'habitat': form.cleaned_data.get('habitat'),
                    'lat': form.cleaned_data.get('lat'),
                    'long': form.cleaned_data.get('long'),
                    'altitude': form.cleaned_data.get('altitude'),
                    'geodata': form.cleaned_data.get('geodata'),
                    'notes': form.cleaned_data.get('notes'),
                    'genus': form.cleaned_data.get('genus'),
                    'sp1': form.cleaned_data.get('sp1'),
                    'author1': form.cleaned_data.get('author1'),
                    'rank1': form.cleaned_data.get('rank1'),
                    'sp2': form.cleaned_data.get('sp2'),
                    'author2': form.cleaned_data.get('author2'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Espécimen', especimen.id, request.user, detalles='Se agregó un nuevo Espécimen.', datos_formulario=datos_formulario)
                ############## REGISTRO EN EL HISTORIAL ##############

                # Redirigir a la página de Espécimen
                messages.success(request, "Espécimen agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Especímenes")

            else:
                # Envío de error si el formulario no es válido
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
        ###############################################################


        ###############################################################
        # Agregar Usuario
        if go_to == 'Usuarios':

            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()  # Esto guarda el usuario y encripta la contraseña

                ############## REGISTRO EN EL HISTORIAL ##############
                datos_formulario = {
                    'username': form.cleaned_data.get('username'),
                    'email': form.cleaned_data.get('email'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Usuario', user.id, request.user, detalles='Se agregó un nuevo Usuario.', datos_formulario=datos_formulario)
                ############## REGISTRO EN EL HISTORIAL ##############

                messages.success(request, "Usuario agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Usuarios")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = CustomUserCreationForm()
        ###############################################################


        ###############################################################
        # Agregar Imagen
        if go_to == 'Galería':
            form = EspeciesFotosVivasForm(request.POST, request.FILES)

            # Verificar si el forulario es válido y si tiene imagen
            if form.is_valid():
                # Revisar que se haya pasado el archivo (No se sabe si es requerido completamente)
                archivo = request.FILES.get('photo_name') 

                # Validar el archivo
                if not validar_archivo(archivo, request):
                    return redirect(f"{reverse('main:content')}?item=Galería")

                # Guardar el archivo si es válido
                if archivo:

                    # Guarda el archivo en el directorio de volumen "Carpeta quizás presta a cambios"
                    fs = FileSystemStorage(location='staticfiles/fotos_vivas')
                    nombre_archivo = archivo.name

                    # Verificar si el archivo ya existe en el directorio
                    if not fs.exists(nombre_archivo):
                        # Guarda el archivo en el directorio
                        nombre_archivo = fs.save(nombre_archivo, archivo)

                        # Guardar solo el nombre del archivo en la base de datos
                        imagen = form.save(commit=False)
                        imagen.foto_nombre = nombre_archivo
                        imagen.save()
                        # print("Archivo guardado.")
                    else:
                        messages.success(request, "La imagen con ese nombre ya existe.")
                        return redirect(f"{reverse('main:content')}?item=Galería")

                else:
                    # Guardar sin archivo si no se subió ninguno
                    imagen = form.save(commit=False)
                    imagen = form.save()

                ############## REGISTRO EN EL HISTORIAL ##############
                # Convertir los datos del formulario a un diccionario
                datos_formulario = {
                    'Familia': form.cleaned_data.get('familiy'),
                    'photo_name': form.cleaned_data.get('photo_name'),
                    'gallery': form.cleaned_data.get('gallery'),
                    'comment': form.cleaned_data.get('comment'),
                    'species': form.cleaned_data.get('species'),
                    'species_authors': form.cleaned_data.get('species_authors'),
                    'genus': form.cleaned_data.get('genus'),
                    'sp1': form.cleaned_data.get('sp1'),
                    'author1': form.cleaned_data.get('author1'),
                    'rank1': form.cleaned_data.get('rank1'),
                    'sp2': form.cleaned_data.get('sp2'),
                    'author2': form.cleaned_data.get('author2'),
                    'rank2': form.cleaned_data.get('rank2'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Galería', imagen.id, request.user, detalles='Se agregó una nueva Imagen a la galería.', datos_formulario=datos_formulario)
                ############## REGISTRO EN EL HISTORIAL ##############

                # Redirigir a la página de Galería
                messages.success(request, "Imagen agregada exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Galería")
            else:
                # Envío de error si el formulario no es válido
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
        ###############################################################


        ###############################################################
        # Agregar Glosario
        if go_to == 'Glosario':

            form = GlosarioForm(request.POST)
            if form.is_valid():
                glosario = form.save()

                datos_formulario = {
                    'termino': form.cleaned_data.get('termino'),
                    'definicion': form.cleaned_data.get('definicion'),
                    'c': form.cleaned_data.get('c'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Glosario', glosario.id, request.user, detalles='Se agregó un nuevo recurso al Glosario.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Recursos&recurso=Glosario")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = CustomUserCreationForm()
        ###############################################################


        ###############################################################
        # Agregar Especie Excluida
        if go_to == 'Especies Excluidas':

            form = EspeciesExcluidasForm(request.POST)
            if form.is_valid():
                excluidas = form.save()

                datos_formulario = {
                    'nombre_cientifico': form.cleaned_data.get('nombre_cientifico'),
                    'species_authors': form.cleaned_data.get('species_authors'),
                    'genus': form.cleaned_data.get('genus'),
                    'sp1': form.cleaned_data.get('sp1'),
                    'autor1': form.cleaned_data.get('autor1'),
                    'rank1': form.cleaned_data.get('rank1'),
                    'sp2': form.cleaned_data.get('sp2'),
                    'autor2': form.cleaned_data.get('autor2'),
                    'comentario': form.cleaned_data.get('comentario'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Especies Excluidas', excluidas.id, request.user, detalles='Se agregó un nuevo recurso a las Especies Excluidas.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Recursos&recurso=EspeciesExcluidas")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = EspeciesExcluidasForm()
        ###############################################################


        ###############################################################
        # Agregar Literatura
        if go_to == 'Literatura':

            form = LiteraturaForm(request.POST)
            if form.is_valid():
                literatura = form.save()

                datos_formulario = {
                    'citada': form.cleaned_data.get('citada'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Literatura', literatura.id, request.user, detalles='Se agregó un nuevo recurso a la Literatura.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Recursos&recurso=Literatura")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = LiteraturaForm()
        ###############################################################


        ###############################################################
        # Agregar Colectores
        if go_to == 'Colectores':

            form = ColectoresForm(request.POST)
            if form.is_valid():
                colectores = form.save()

                datos_formulario = {
                    'colector': form.cleaned_data.get('colector'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Colectores', colectores.id, request.user, detalles='Se agregó un nuevo recurso a los Colectores.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Manejo&recurso=Colectores")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = ColectoresForm()
        ###############################################################


        ###############################################################
        # Agregar Códigos
        if go_to == 'Códigos':

            form = CodigosForm(request.POST)
            if form.is_valid():
                codigos = form.save()

                datos_formulario = {
                    'codigo': form.cleaned_data.get('codigo'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Códigos', codigos.id, request.user, detalles='Se agregó un nuevo recurso a los Códigos.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Manejo&recurso=Códigos")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = CodigosForm()
        ###############################################################


        ###############################################################
        # Agregar Divisiones
        if go_to == 'Divisiones':

            form = DivisionesForm(request.POST)
            if form.is_valid():
                division = form.save()

                datos_formulario = {
                    'division': form.cleaned_data.get('division'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Divisiones', division.id, request.user, detalles='Se agregó un nuevo recurso a Divisiones.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Manejo&recurso=Divisiones")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = DivisionesForm()
        ###############################################################


        ###############################################################
        # Agregar Géneros
        if go_to == 'Géneros':

            form = GenerosForm(request.POST)
            if form.is_valid():
                genero = form.save()

                datos_formulario = {
                    'genero': form.cleaned_data.get('genero'),
                    'familiy': form.cleaned_data.get('familiy'),
                }

                # Registrar la acción en el historial
                registrar_accion('Crear', 'Géneros', genero.id, request.user, detalles='Se agregó un nuevo recurso a Géneros.', datos_formulario=datos_formulario)

                messages.success(request, "Recurso agregado exitosamente.")
                return redirect(f"{reverse('main:content')}?item=Manejo&recurso=Géneros")

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.success(request, f"Error en '{form.fields[field].label}': {error}")
            
            form = GenerosForm()
        ###############################################################

    # Devuelta a la página de la que se viene
    if go_to == 'Glosario' or go_to == 'Literatura':
        return redirect(f"{reverse('main:content')}?item=Recursos&recurso={go_to}", {'form': form})
    elif go_to == 'Especies Excluidas':
        return redirect(f"{reverse('main:content')}?item=Recursos&recurso=EspeciesExcluidas", {'form': form})
    elif go_to == 'Colectores' or go_to == 'Códigos' or go_to == 'Divisiones' or go_to == 'Géneros':
        return redirect(f"{reverse('main:content')}?item=Manejo&recurso={go_to}", {'form': form})
    else:
        return redirect(f"{reverse('main:content')}?item={go_to}", {'form': form})
####################################### MÉTODO POST #######################################



####################################### MÉTODO DELETE #######################################
@login_required
@csrf_protect
def delete(request, id, title):
    if request.method == 'POST':
        go_to = request.POST.get('go_to') # Diferenciar a dónde van los POST

        ###############################################################
        if title == 'Familias':

            familia = get_object_or_404(Familias, id=id)

            # Verificar la existencia de la foto en el campo de la base de datos
            especies_relacionadas = Especies.objects.filter(familia=familia.familia).exists()

            # print(especies_relacionadas)
            
            # print('#######################################################')
            if especies_relacionadas:
                messages.error(request, "No se puede eliminar la Familia porque está relacionada con una o más especies.")
                return redirect(f"{reverse('main:content')}?item={title}")

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'nombre': familia.familia,
                'division': familia.division, 
                'descripcion': familia.descripcion, 
                'comentario': familia.comentario,
                'foto': familia.foto,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Familias', familia.id, request.user, detalles='Se elimninó una Familia.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            familia.delete()
            messages.success(request, "La familia fue movida a la papelera.")
        ###############################################################


        ###############################################################
        elif title == 'Especies':
            especies = get_object_or_404(Especies, id=id)

            colectores_relacionados = EspecimenesFotos.objects.filter(species=especies.nombre_cientifico).exists()

            if colectores_relacionados:
                messages.error(request, "No se puede eliminar la Especie porque está relacionada con uno o más Especímenes.")
                return redirect(f"{reverse('main:content')}?item={title}")

            ############## REGISTRO EN EL HISTORIAL ##############
            datos_formulario = {
                'nombre_cientifico': especies.nombre_cientifico,
                'familia': especies.familia,
                'codigo': especies.codigo,
                'nombre_comun': especies.nombre_comun,
                # 'foto': nombre_archivo if archivo else None,
                'foto': especies.foto,
                'sinonimos': especies.sinonimos,
                'species_authors': especies.species_authors,
                'genus':  especies.genus,
                'rank1': especies.rank1,
                'sp1': especies.sp1,
                'author1': especies.author1,
                'sp2': especies.sp2,
                'author2': especies.author2,
                'habito': especies.habito,
                'tallos': especies.tallos,
                'hojas': especies.hojas,
                'inflorescencia': especies.inflorescencia,
                'frutos': especies.frutos,
                'soros': especies.soros,
                'distribucion': especies.distribucion,
                'nota': especies.nota,
            }

                    # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Especies', especies.id, request.user, detalles='Se elimninó una Especie.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            especies.delete()
            messages.success(request, "La Especie fue movida a la papelera.")
        ###############################################################


        ###############################################################
        elif title == 'Especímenes':

            especimen = get_object_or_404(EspecimenesFotos, id=id)

            # Eliminar la imagen del espécimen
            if especimen.photoname:
                fs = FileSystemStorage(location='staticfiles/Images_elverde')
                fs_comp = FileSystemStorage(location='staticfiles/Images_comp')
                fs_thumb = FileSystemStorage(location='staticfiles/Images_elverde/thumb/JPEG')
                foto_path = especimen.photoname

                # Elimina el archivo en la ubicación principal
                if fs.exists(foto_path):
                    fs.delete(foto_path)  # Elimina el archivo
                
                # Elimina el archivo comprimido
                if fs_comp.exists(foto_path):
                    fs_comp.delete(foto_path)  

                # Elimina el archivo thumb
                if fs_thumb.exists(foto_path):
                    fs_thumb.delete(foto_path)  

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'familiy': especimen.familiy,
                'species': especimen.species,
                'photoname': especimen.photoname,
                'barcode': especimen.barcode,
                'accesion': especimen.accesion,
                'collector': especimen.collector,
                'number': especimen.number,
                'addcoll': especimen.addcoll,
                'herb': especimen.herb,
                'day': especimen.day,
                'month': especimen.month,
                'year': especimen.year,
                'division': especimen.division,
                'code': especimen.code,
                'species_authors': especimen.species_authors,
                'detby': especimen.detby,
                'detdate': especimen.detdate,
                'plantdesc': especimen.plantdesc,
                'habitat': especimen.habitat,
                'lat': especimen.lat,
                'long': especimen.long,
                'altitude': especimen.altitude,
                'geodata': especimen.geodata,
                'notes': especimen.notes,
                'genus': especimen.genus,
                'sp1': especimen.sp1,
                'author1': especimen.author1,
                'rank1': especimen.rank1,
                'sp2': especimen.sp2,
                'author2': especimen.author2,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Espécimen', especimen.id, request.user, detalles='Se eliminó un Espécimen.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            especimen.delete()
            messages.success(request, "El Espécimen fue movida a la papelera.")
        ###############################################################


        ###############################################################
        elif title == 'Galería':

            imagen = get_object_or_404(EspeciesFotosVivas, id=id)

            if imagen.photo_name:
                fs = FileSystemStorage(location='staticfiles/fotos_vivas')
                # Asegúrate de que foto_path sea solo el nombre del archivo
                foto_path = imagen.photo_name # Obtén solo el nombre del archivo
                
                # Construir la ruta completa
                full_path = fs.path(foto_path)
                
                if fs.exists(full_path):
                    print("Foto eliminada")
                    fs.delete(full_path)  # Elimina el archivo
                else:
                    print("El archivo no existe.")

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'Familia': imagen.familiy,
                'photo_name': imagen.photo_name,
                'gallery': imagen.gallery,
                'comment': imagen.comment,
                'species': imagen.species,
                'species_authors': imagen.species_authors,
                'genus': imagen.genus,
                'sp1': imagen.sp1,
                'author1': imagen.author1,
                'rank1': imagen.rank1,
                'sp2': imagen.sp2,
                'author2': imagen.author2,
                'rank2': imagen.rank2,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Galería', imagen.id, request.user, detalles='Se elimninó una imagen de la Galería.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            imagen.delete()
            messages.success(request, "La Imagen fue movida a la papelera.")
        ###############################################################


        ##############################################################
        elif title == 'Usuarios':

            # Busca el usuario por ID
            usuario = get_object_or_404(User, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del usuario a un diccionario
            datos_formulario = {
                'username': usuario.username,
                'email': usuario.email,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Usuario', usuario.id, request.user, detalles='Se eliminó un usuario.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            # Eliminar el usuario
            usuario.delete()
            messages.success(request, "El usuario fue eliminado correctamente.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Glosario':

            glosario = get_object_or_404(Glosario, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'termino': glosario.termino,
                'definicion': glosario.definicion,
                'c': glosario.c,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Glosario', glosario.id, request.user, detalles='Se elimninó un recurso de Glosario.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            glosario.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Literatura':

            literatura = get_object_or_404(Literatura, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'citada': literatura.citada,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Literatura', literatura.id, request.user, detalles='Se elimninó un recurso de Literatura.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            literatura.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Especies Excluidas':

            excluidas = get_object_or_404(EspeciesExcluidas, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'nombre_cientifico': excluidas.nombre_cientifico,
                'species_authors': excluidas.species_authors,
                'genus': excluidas.genus,
                'sp1': excluidas.sp1,
                'autor1': excluidas.autor1,
                'rank1': excluidas.rank1,
                'sp2': excluidas.sp2,
                'autor2': excluidas.autor2,
                'comentario': excluidas.comentario,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Especies Excluidas', excluidas.id, request.user, detalles='Se elimninó un recurso de Especies Excluidas.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            excluidas.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Colectores':

            colectores = get_object_or_404(Colectores, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'colector': colectores.colector,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Colectores', colectores.id, request.user, detalles='Se elimninó un recurso de Colectores.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            colectores.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Códigos':

            codigo = get_object_or_404(Codigos, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'codigo': codigo.codigo,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Códigos', codigo.id, request.user, detalles='Se elimninó un recurso de Códigos.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            codigo.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Divisiones':

            division = get_object_or_404(Divisiones, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'division': division.division,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Divisiones', division.id, request.user, detalles='Se elimninó un recurso de Divisiones.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            division.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################


        ##################################################ª#############
        elif title == 'Géneros':

            genero = get_object_or_404(Generos, id=id)

            ############## REGISTRO EN EL HISTORIAL ##############
            # Convertir los datos del formulario a un diccionario
            datos_formulario = {
                'genero': genero.genero,
                'familiy': genero.familiy,
            }

            # Registrar la acción en el historial
            registrar_accion('Eliminar', 'Géneros', genero.id, request.user, detalles='Se elimninó un recurso de Géneros.', datos_formulario=datos_formulario)
            ############## REGISTRO EN EL HISTORIAL ##############

            genero.delete()
            messages.success(request, "El recurso fue movido a la papelera.")
        ###############################################################

        # Devuelta a la página de la que se viene :D
        if go_to == 'Glosario' or go_to == 'Literatura':
            return redirect(f"{reverse('main:content')}?item=Recursos&recurso={go_to}")
        elif go_to == 'Especies Excluidas':
            return redirect(f"{reverse('main:content')}?item=Recursos&recurso=EspeciesExcluidas")
        elif go_to == 'Colectores' or go_to == 'Códigos' or go_to == 'Divisiones' or go_to == 'Géneros':
            return redirect(f"{reverse('main:content')}?item=Manejo&recurso={go_to}")
        else:
            return redirect(f"{reverse('main:content')}?item={go_to}")
####################################### MÉTODO DELETE #######################################



# Se utiliza para ligar las fotos con las familias y especies
####################################### MÉTODO UPDATE #######################################
@login_required
@csrf_protect
def update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        title = request.POST.get('go_to')
        photo_name = request.POST.get('photo_name')

        user = request.user
        ###############################################################
        if title == 'Familias':
            # Obtenerªª la instancia de Especies por su ID
            familia = get_object_or_404(Familias, familia=name)
            
            if request.method == 'POST':
                # Si el formulario se envía, procesar los datos
                form = FamiliaForm(request.POST, request.FILES, instance=familia)

                if not form.is_valid():
                    print(form.errors) 
                else:
                    # Obtener la instancia sin guardar
                    familia_instance = form.save(commit=False)
                    if form.is_valid():
                        familia_instance = form.save(commit=False)
                        # Cambiar el campo 'foto' de la familia
                        # familia.foto = photo_name
                        familia_instance.foto = photo_name
                        # form.save()  # Guardar los cambios
                        familia_instance.save()
                        familia_data = form.cleaned_data.get('familia')
                        messages.success(request, f"La Imagen ha sido ligada a la Familia: {familia_data}")
            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = FamiliaForm(instance=familia)
        ###############################################################


        ###############################################################
        if title == 'Especies':
            # Obtenerªª la instancia de Especies por su ID
            especies = get_object_or_404(Especies, nombre_cientifico=name)

            if request.method == 'POST':
                # Si el formulario se envía, procesar los datos
                form = EspecieForm(request.POST,  request.FILES, instance=especies)

                if not form.is_valid():
                    print(form.errors) 

                if form.is_valid():
                    especies.foto = photo_name
                    form.save()  # Guardar los cambios
                    especie_data = form.cleaned_data.get('nombre_cientifico')
                    messages.success(request, f"La Imagen ha sido ligada a la Especie: {especie_data}")
            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = EspecieForm(instance=especies)
        ###############################################################



    return redirect(f"{reverse('main:content')}?item={title}")
####################################### MÉTODO UPDATE #######################################
