from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from django.core.paginator import Paginator

from django.core.files.storage import FileSystemStorage

from django.conf import settings


# Importar Modelos
from login.models import * 
from .models import Historial
from django.contrib.auth.models import User

# Importar Formularios
from .forms import *

# from .methods import update

from .utils import registrar_accion, validar_archivo

@login_required
def main_page(request):
    if 'user_token' not in request.session:
        return redirect('login:login') 

    # REFACTORIZAR, CAMBIAR REDIRECCIÓN A LA PÁGINA PRINCIPAL !!! Se quedó así :p
    return redirect(f"{reverse('main:content')}?item=Familias")



####################################### VISUALIZACIÓN DE CONTENIDO #######################################
@login_required
def content_view(request):
    item = request.GET.get('item')  # Obtiene el dato enviado
    searched = request.GET.get('searched') # Obtiene el elemento buscado
    recurso = request.GET.get('recurso') # Obtiene el recurso buscado
    page_number = request.GET.get('page') or 1  # Obtener el número de página de la solicitud
    idToEdit = request.GET.get('Id')  # Obtiene el ID del elemento

    # Lista vacía
    some = ""

    user = request.user
    # user_logged = str(user.username) if user.is_authenticated else "Invitado"
    
    ###############################################################
    # Seletor de contexto de Familia 
    if item == 'Familias':
        if idToEdit:
            # update(idToEdit, title):

            # Obtenerªª la instancia de Especies por su ID
            familia = get_object_or_404(Familias, id=idToEdit)

            # Obtener el nombre anterior
            nombre_anterior = familia.familia

            if request.method == 'POST':

                # Si el formulario se envía, procesar los datos
                form = FamiliaForm(request.POST, instance=familia)
                if form.is_valid():
                    # Guardar los cambios
                    form.save()  
                    # return render(request, 'content.html', context)
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
                    registrar_accion('Editar', 'Familias', familia.id, request.user, detalles='Se editó uno o más campos de una Familia.', datos_formulario=datos_formulario)
                    ############## REGISTRO EN EL HISTORIAL ##############

                    messages.success(request, "La Familia ha sido actualizada.")

                    # Verificar si el nombre ha cambiado
                    if nombre_anterior != familia.familia:
                        # Actualizar las tablas relacionadas AÑADIR MÁS!! Especimen, galeria, excluidas
                        Especies.objects.filter(familia=nombre_anterior).update(familia=familia.familia)
                        EspeciesFotosVivas.objects.filter(familiy=nombre_anterior).update(familiy=familia.familia)
                        EspecimenesFotos.objects.filter(familiy=nombre_anterior).update(familiy=familia.familia)
                        Generos.objects.filter(familiy=nombre_anterior).update(familiy=familia.familia)

            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = FamiliaForm(instance=familia)

            context = {
                'user': user,
                'form': form, 
                'familia': familia,
                'editar': True,
                'title': item,
                'id': idToEdit,
            }
            
            # Renderizar la plantilla con el formulario
            return render(request, 'content.html', context)

        else:

            if searched:
                # Cargar los datos filtrados
                familias = Familias.objects.filter(familia__startswith=searched).values('familia', 'division', 'comentario', 'id', 'foto').order_by('familia')

            else:
                # Cargar datos relacionados con 'familia'
                familias = Familias.objects.values('familia', 'division', 'comentario', 'id', 'foto').order_by('familia')

            especiesInFamily = Especies.objects.values('nombre_cientifico', 'familia').order_by('familia')

            familiyNameList = Familias.objects.values('familia').order_by('familia') # Esto es para el search
            
            # Crear una instancia del formulario
            formFamilia = FamiliaForm()

            paginator = Paginator(familias, 50) 
            page_obj = paginator.get_page(page_number) 

            # Contexto de la página
            context = {
                'user': user,
                'familias':  list(familiyNameList),
                'dependientes': list(especiesInFamily),
                'page_obj': page_obj,
                'form': formFamilia,
                'title': "Familias",
            }

            return render(request, 'content.html', context)  # Pasa el contexto a la plantilla
    ###############################################################


    ###############################################################
    # Seletor de contexto de Especie
    elif item == 'Especies':
        if idToEdit:
            # update(idToEdit, title):

            # Obtenerªª la instancia de Especies por su ID
            especies = get_object_or_404(Especies, id=idToEdit)

            nombre_anterior = especies.nombre_cientifico
            
            if request.method == 'POST':
                # Si el formulario se envía, procesar los datos
                form = EspecieForm(request.POST, instance=especies)

                if form.is_valid():
                    form.save()  # Guardar los cambios

                    ############## REGISTRO EN EL HISTORIAL ##############
                    datos_formulario = {
                        'nombre_cientifico': especies.nombre_cientifico,
                        'familia': especies.familia,
                        'codigo': especies.codigo,
                        'nombre_comun': especies.nombre_comun,
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
                    registrar_accion('Editar', 'Especies', especies.id, request.user, detalles='Se editó uno o más campos de una Especie.', datos_formulario=datos_formulario)
                    ############## REGISTRO EN EL HISTORIAL ##############
                    messages.success(request, "La Especie ha sido actualizada.")

                    # Verificar si el nombre ha cambiado
                    if nombre_anterior != especies.nombre_cientifico:
                        # Actualizar las tablas relacionadas AÑADIR MÁS!! Especimen, galeria, excluidas
                        EspeciesFotosVivas.objects.filter(species=nombre_anterior).update(species=especies.nombre_cientifico)
                        EspecimenesFotos.objects.filter(species=nombre_anterior).update(species=especies.nombre_cientifico)
                    
            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = EspecieForm(instance=especies)

            context = {
                'user': user,
                'form': form, 
                'especies': especies,
                'editar': True,
                'title': item,
                'id': idToEdit,
            }

            # Renderizar la plantilla con el formulario
            return render(request, 'content.html', context)

        else: 
            if searched:
                # Cargar los datos filtrados
                especies = Especies.objects.filter(nombre_cientifico__startswith=searched).values('nombre_cientifico', 'familia','codigo', 'nombre_comun', 'id', 'foto').order_by('nombre_cientifico')

            else:
                # Cargar datos relacionados con 'familia'
                especies = Especies.objects.values('nombre_cientifico', 'familia','codigo', 'nombre_comun', 'id', 'foto').order_by('nombre_cientifico')

            especiesNameList = Especies.objects.values('nombre_cientifico').order_by('nombre_cientifico')
            especimenInEspecies = EspecimenesFotos.objects.values('species', 'collector').order_by('species')

            formEspecie = EspecieForm()

            paginator = Paginator(especies, 100) 
            page_obj = paginator.get_page(page_number)  

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(especimenInEspecies), 
                'especies':  list(especiesNameList),
                'form': formEspecie,
                'page_obj': page_obj,
                'title': "Especies",
            }

            return render(request, 'content.html', context)  # Pasa el contexto a la plantilla
    ###############################################################


    ###############################################################
    # Seletor de contexto de Especimen
    elif item == 'Especímenes':
        if idToEdit:
            # update(idToEdit, title):

            # Obtenerªª la instancia de Especies por su ID
            especimenes = get_object_or_404(EspecimenesFotos, id=idToEdit)
            nombre_foto = especimenes.photoname
            if request.method == 'POST':
                # Si el formulario se envía, procesar los datos
                form = EspecimenForm(request.POST, request.FILES, instance=especimenes)
                if form.is_valid():

                    # Verificar que se haya enviado el archivo
                    if request.FILES.get('photoname'):
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
                        especimen = form.save(commit=False)
                        especimen.photoname = nombre_foto
                    
                    # Guardar la instancia del Especimen para obtener su ID
                    especimen.save()
                    messages.success(request, "El Espécimen ha sido actualizado.")

                    ############## REGISTRO EN EL HISTORIAL ##############
                    # Convertir los datos del formulario a un diccionario
                    datos_formulario = {
                        'familiy': especimenes.familiy,
                        'species': especimenes.species,
                        'photoname': especimenes.photoname,
                        'barcode': especimenes.barcode,
                        'accesion': especimenes.accesion,
                        'collector': especimenes.collector,
                        'number': especimenes.number,
                        'addcoll': especimenes.addcoll,
                        'herb': especimenes.herb,
                        'day': especimenes.day,
                        'month': especimenes.month,
                        'year': especimenes.year,
                        'division': especimenes.division,
                        'code': especimenes.code,
                        'species_authors': especimenes.species_authors,
                        'detby': especimenes.detby,
                        'detdate': especimenes.detdate,
                        'plantdesc': especimenes.plantdesc,
                        'habitat': especimenes.habitat,
                        'lat': float(especimenes.lat) if especimenes.lat else None,
                        'long': float(especimenes.long) if especimenes.long else None,
                        'altitude': especimenes.altitude,
                        'geodata': especimenes.geodata,
                        'notes': especimenes.notes,
                        'genus': especimenes.genus,
                        'sp1': especimenes.sp1,
                        'author1': especimenes.author1,
                        'rank1': especimenes.rank1,
                        'sp2': especimenes.sp2,
                        'author2': especimenes.author2,
                    }

                    # Registrar la acción en el historial
                    registrar_accion('Editar', 'Espécimen', especimenes.id, request.user, detalles='Se editó uno o más campos de un Espécimen.', datos_formulario=datos_formulario)
                    ############## REGISTRO EN EL HISTORIAL ##############
            
            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = EspecimenForm(instance=especimenes)

            context = {
                'user': user,
                'form': form, 
                'especimenes': especimenes,
                'editar': True,
                'title': item,
                'id': idToEdit,
            }

            # Renderizar la plantilla con el formulario
            return render(request, 'content.html', context)

        else:
            if searched:
                # Cargar los datos filtrados
                especimenes = EspecimenesFotos.objects.filter(species__startswith=searched).values('species', 'collected','collector', 'geodata', 'photoname', 'id').order_by('species')

            else:
                # Cargar datos relacionados con 'Especímenes'
                especimenes = EspecimenesFotos.objects.values('species', 'collected','collector', 'geodata', 'photoname', 'id').order_by('species')

            especiesNameList = Especies.objects.values('nombre_cientifico').order_by('nombre_cientifico')
            especimenesNameList = EspecimenesFotos.objects.values('species').order_by('species')

            formEspecimen = EspecimenForm()
            

            paginator = Paginator(especimenes, 50) 
            page_obj = paginator.get_page(page_number)  

            # Contexto de la página
            context = {
                'user': user,
                'especies':  list(especiesNameList),
                'especimenes':  list(especimenesNameList),
                'dependientes': list(some),
                'form': EspecimenForm,
                'page_obj': page_obj,
                'title': "Especímenes",
            }

            return render(request, 'content.html', context)  # Pasa el contexto a la plantilla
    ###############################################################


    ###############################################################
    # Seletor de contexto de Historial
    elif  item == 'Historial':
        historial = Historial.objects.values('accion', 'modelo_afectado', 'id_objeto', 'usuario', 'fecha', 'detalles', 'datos_formulario').order_by('-fecha')
        historialList = Historial.objects.values('accion')

        paginator = Paginator(historial, 100) 
        page_obj = paginator.get_page(page_number)  

        # Contexto de la página
        context = {
            'user': user,
            'historial':  list(historialList),
            'page_obj': page_obj,
            'dependientes': list(some),
            'title': "Historial",
        }

        return render(request, 'content.html', context)
    ###############################################################


    ###############################################################
    # Selector de contexto de usuario
    elif  item == 'Usuarios':
        if searched:
            usuarios = User.objects.filter(username__startswith=searched).values('username', 'email', 'password', 'id')
        else: 
            usuarios = User.objects.values('username', 'email', 'password', 'id')

        formUsuario = CustomUserCreationForm()

        # print(historial)
        paginator = Paginator(usuarios, 100) 
        page_obj = paginator.get_page(page_number)  

        # Contexto de la página
        context = {
            'user': user,
            'usuario':  list(usuarios),
            'dependientes': list(some),
            'form': formUsuario,
            'page_obj': page_obj,
            'title': "Usuarios",
        }

        return render(request, 'content.html', context)
    ###############################################################


    ###############################################################
    # Selector de contexto de Galería
    elif  item == 'Galería':
        if idToEdit:

            # Obtenerªª la instancia de Especies por su ID
            especiesImg = get_object_or_404(EspeciesFotosVivas, id=idToEdit)
            
            # Traer elementos que para relacionar, Familias y Especies
            familiaRelated = get_object_or_404(Familias, familia=especiesImg.familiy)
            especieRelated = get_object_or_404(Especies, nombre_cientifico=especiesImg.species)

            if request.method == 'POST':
                # Si el formulario se envía, procesar los datos
                form = EspeciesFotosVivasForm(request.POST, request.FILES, instance=especiesImg)

                if form.is_valid():
                    # for field in form:
                    #     print(f"{field.label}: {field.value()}")
                        
                    # Revisar que se haya pasado el archivo (No se sabe si es requerido completamente)
                    archivo = request.FILES.get('photo_name') 

                    # Validar el archivo
                    if not validar_archivo(archivo, request):
                        return redirect(f"{reverse('main:content')}?item=Galería")

                    # Guardar el archivo si es válido
                    if archivo:

                        # Configurar el almacenamiento de archivos
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
                            messages.success(request, "La información de la Imagen ha sido actualizada.")
                            ############## REGISTRO EN EL HISTORIAL ##############
                            # Convertir los datos del formulario a un diccionario
                            datos_formulario = {
                                'Familia': especiesImg.familiy,
                                'photo_name': especiesImg.photo_name,
                                'gallery': especiesImg.gallery,
                                'comment': especiesImg.comment,
                                'species': especiesImg.species,
                                'species_authors': especiesImg.species_authors,
                                'genus': especiesImg.genus,
                                'sp1': especiesImg.sp1,
                                'author1': especiesImg.author1,
                                'rank1': especiesImg.rank1,
                                'sp2': especiesImg.sp2,
                                'author2': especiesImg.author2,
                                'rank2': especiesImg.rank2,
                            }

                            # Registrar la acción en el historial
                            registrar_accion('Editar', 'Galería', especiesImg.id, request.user, detalles='Se editó uno o más campos de una imagen de la Galería.', datos_formulario=datos_formulario)
                            ############## REGISTRO EN EL HISTORIAL ##############
                            
                        else:
                            messages.success(request, "La imagen con ese nombre ya existe.")
                    else:
                        # Guardar sin archivo si no se subió ninguno
                        imagen = form.save(commit=False)
                        imagen = form.save()
                        messages.success(request, "La información de la Imagen ha sido actualizada.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'Familia': especiesImg.familiy,
                            'photo_name': especiesImg.photo_name,
                            'gallery': especiesImg.gallery,
                            'comment': especiesImg.comment,
                            'species': especiesImg.species,
                            'species_authors': especiesImg.species_authors,
                            'genus': especiesImg.genus,
                            'sp1': especiesImg.sp1,
                            'author1': especiesImg.author1,
                            'rank1': especiesImg.rank1,
                            'sp2': especiesImg.sp2,
                            'author2': especiesImg.author2,
                            'rank2': especiesImg.rank2,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Galería', especiesImg.id, request.user, detalles='Se editó uno o más campos de una imagen de la Galería.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############

                else:
                    print("Errores en el formulario:", form.errors) 

            else:
                # Si es una solicitud GET, mostrar el formulario con los datos actuales
                form = EspeciesFotosVivasForm(instance=especiesImg)

            context = {
                'user': user,
                'form': form, 
                'especiesImg': especiesImg,
                'editar': True,
                'title': item,
                'id': idToEdit,
                'especieRelated': especieRelated,
                'familiaRelated': familiaRelated,
            }

            # Renderizar la plantilla con el formulario
            return render(request, 'content.html', context)

        else:
            if searched:
                especiesFotosVivas = EspeciesFotosVivas.objects.filter(species__startswith=searched).values('species', 'author1', 'photo_name', 'id').order_by('species')
            else: 
                especiesFotosVivas = EspeciesFotosVivas.objects.values('species', 'author1', 'photo_name', 'id').order_by('species')
            especiesNameList = Especies.objects.values('nombre_cientifico').order_by('nombre_cientifico')

            formGalería = EspeciesFotosVivasForm()

            # print(historial)
            paginator = Paginator(especiesFotosVivas, 100) 
            page_obj = paginator.get_page(page_number)  

            # Contexto de la página
            context = {
                'user': user,
                'species_names': list(especiesNameList),
                'galeria':  list(especiesFotosVivas),
                'form': formGalería,
                'dependientes': list(some),
                'page_obj': page_obj,
                'title': "Galería",
            }

            return render(request, 'content.html', context)
    ###############################################################


    ###############################################################
    # Selector de contexto de Recursos
    elif  item == 'Recursos':

        ################ Glosario ################
        if recurso == 'Glosario':
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                glosario = get_object_or_404(Glosario, id=idToEdit)

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = GlosarioForm(request.POST, instance=glosario)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'termino': glosario.termino,
                            'definicion': glosario.definicion,
                            'c': glosario.c,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Glosario', glosario.id, request.user, detalles='Se editó uno o más campos de un recurso de Glosario.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############
                        
                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = GlosarioForm(instance=glosario)

                context = {
                    'user': user,
                    'form': form, 
                    'Glosario': glosario,
                    'editar': True,
                    'title': item,
                    'subtitle': "Glosario",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                glosario = Glosario.objects.filter(termino__startswith=searched).values('termino', 'definicion', 'c', 'id').order_by('termino')
            else: 
                glosario = Glosario.objects.values('termino', 'definicion', 'c', 'id').order_by('termino')

            paginator = Paginator(glosario, 100) 
            page_obj = paginator.get_page(page_number)  
            formGlosario = GlosarioForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(glosario),
                'form': formGlosario,
                'page_obj': page_obj,
                'title': "Recursos",
                'subtitle': "Glosario",
            }

            return render(request, 'content.html', context)

        ################ Literatura ################
        elif recurso == 'Literatura':
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                literatura = get_object_or_404(Literatura, id=idToEdit)

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = LiteraturaForm(request.POST, instance=literatura)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'citada': literatura.citada,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Literatura', literatura.id, request.user, detalles='Se editó uno o más campos de un recurso de Literatura.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############
                        # return render(request, 'content.html', context)
                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = LiteraturaForm(instance=literatura)

                context = {
                    'user': user,
                    'form': form, 
                    'literatura': literatura,
                    'editar': True,
                    'title': item,
                    'subtitle': "Literatura",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                literatura = Literatura.objects.filter(citada__startswith=searched).values('citada', 'id').order_by('citada')
            else: 
                literatura = Literatura.objects.values('citada', 'id').order_by('citada')

            paginator = Paginator(literatura, 100) 
            page_obj = paginator.get_page(page_number)  
            formLiteratura = LiteraturaForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(literatura),
                'form': formLiteratura,
                'page_obj': page_obj,
                'title': "Recursos",
                'subtitle': "Literatura",
            }

            return render(request, 'content.html', context)

        ################ Especies Excluidas ################
        elif recurso == "EspeciesExcluidas":
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                excluidas = get_object_or_404(EspeciesExcluidas, id=idToEdit)

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = EspeciesExcluidasForm(request.POST, instance=excluidas)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "La Especie ha sido actualizada.")

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
                        registrar_accion('Editar', 'Especies Excluidas', excluidas.id, request.user, detalles='Se editó uno o más campos de un recurso de Especies Excluidas.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############
                        
                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = EspeciesExcluidasForm(instance=excluidas)

                context = {
                    'user': user,
                    'form': form, 
                    'excluidas': excluidas,
                    'editar': True,
                    'title': item,
                    'subtitle': "Especies Excluidas",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                especiesExcluidas = EspeciesExcluidas.objects.filter(nombre_cientifico__startswith=searched).values('nombre_cientifico', 'species_authors', 'comentario', 'id').order_by('nombre_cientifico')
            else: 
                especiesExcluidas = EspeciesExcluidas.objects.values('nombre_cientifico', 'species_authors', 'comentario', 'id').order_by('nombre_cientifico')

            paginator = Paginator(especiesExcluidas, 100) 
            page_obj = paginator.get_page(page_number)  
            formExcluidas = EspeciesExcluidasForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(especiesExcluidas),
                'form': formExcluidas,
                'page_obj': page_obj,
                'title': "Recursos",
                'subtitle': "Especies Excluidas",
            }

            return render(request, 'content.html', context)
    ###############################################################


    ###############################################################
    # Selector de contexto de usuario
    elif  item == 'Manejo':

        ################ Colectores ################
        if recurso == 'Colectores':
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                colectores = get_object_or_404(Colectores, id=idToEdit)

                nombre_anterior = colectores.colector

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = ColectoresForm(request.POST, instance=colectores)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'colector': colectores.colector,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Colectores', colectores.id, request.user, detalles='Se editó uno o más campos de un recurso de Colectores.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############

                        if nombre_anterior != colectores.colector:
                            # Actualizar las tablas relacionadas
                            EspecimenesFotos.objects.filter(collector=nombre_anterior).update(collector=colectores.colector)
                        
                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = ColectoresForm(instance=colectores)

                context = {
                    'user': user,
                    'form': form, 
                    'colectores': colectores,
                    'editar': True,
                    'title': item,
                    'subtitle': "Colectores",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)
            
            if searched:
                colectores = Colectores.objects.filter(colector__startswith=searched).values('colector', 'id').order_by('colector')
            else: 
                colectores = Colectores.objects.values('colector', 'id').order_by('colector')

            paginator = Paginator(colectores, 100) 
            page_obj = paginator.get_page(page_number)
            formColectores = ColectoresForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(colectores),
                'form': formColectores,
                'page_obj': page_obj,
                'title': "Manejo",
                'subtitle': "Colectores",
            }

            return render(request, 'content.html', context)

        ################ Códigos ################
        elif recurso == 'Códigos':
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                codigo = get_object_or_404(Codigos, id=idToEdit)

                nombre_anterior = codigo.codigo

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = CodigosForm(request.POST, instance=codigo)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'codigo': codigo.codigo,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Códigos', codigo.id, request.user, detalles='Se editó uno o más campos de un recurso de Códigos.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############

                        if nombre_anterior != codigo.codigo:
                            # Actualizar las tablas relacionadas
                            EspecimenesFotos.objects.filter(code=nombre_anterior).update(code=codigo.codigo)
                            Especies.objects.filter(codigo=nombre_anterior).update(codigo=codigo.codigo)

                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = CodigosForm(instance=codigo)

                context = {
                    'user': user,
                    'form': form, 
                    'codigos': codigo,
                    'editar': True,
                    'title': item,
                    'subtitle': "Códigos",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                codigos = Codigos.objects.filter(codigo__startswith=searched).values('codigo', 'id').order_by('codigo')
            else: 
                codigos = Codigos.objects.values('codigo', 'id').order_by('codigo')

            paginator = Paginator(codigos, 100) 
            page_obj = paginator.get_page(page_number)  
            formCodigos = CodigosForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(codigos),
                'form': formCodigos,
                'page_obj': page_obj,
                'title': "Manejo",
                'subtitle': "Códigos",
            }

            return render(request, 'content.html', context)

        ################ Divisiones ################
        elif recurso == "Divisiones":
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                divisiones = get_object_or_404(Divisiones, id=idToEdit)

                nombre_anterior = divisiones.division

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = DivisionesForm(request.POST, instance=divisiones)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'division': divisiones.division,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Divisiones', divisiones.id, request.user, detalles='Se editó uno o más campos de un recurso de Divisiones.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############

                        if nombre_anterior != divisiones.division:
                            # Actualizar las tablas relacionadas
                            EspecimenesFotos.objects.filter(division=nombre_anterior).update(division=divisiones.division)
                            Familias.objects.filter(division=nombre_anterior).update(division=divisiones.division)

                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = DivisionesForm(instance=divisiones)

                context = {
                    'user': user,
                    'form': form, 
                    'divisiones': divisiones,
                    'editar': True,
                    'title': item,
                    'subtitle': "Divisiones",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                divisiones = Divisiones.objects.filter(division__startswith=searched).values('division', 'id').order_by('division')
            else: 
                divisiones = Divisiones.objects.values('division', 'id').order_by('division')

            paginator = Paginator(divisiones, 100) 
            page_obj = paginator.get_page(page_number)  
            formDivisiones = DivisionesForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(divisiones),
                'form': formDivisiones,
                'page_obj': page_obj,
                'title': "Manejo",
                'subtitle': "Divisiones",
            }

            return render(request, 'content.html', context)

        ################ Géneros ################
        elif recurso == "Géneros":
            if idToEdit:
                # update(idToEdit, title):

                # Obtenerªª la instancia de Especies por su ID
                generos = get_object_or_404(Generos, id=idToEdit)

                nombre_anterior = generos.genero

                if request.method == 'POST':
                    # Si el formulario se envía, procesar los datos
                    form = GenerosForm(request.POST, instance=generos)
                    if form.is_valid():
                        form.save()  # Guardar los cambios
                        messages.success(request, "El recurso ha sido actualizado.")

                        ############## REGISTRO EN EL HISTORIAL ##############
                        # Convertir los datos del formulario a un diccionario
                        datos_formulario = {
                            'genero': generos.genero,
                            'familiy': generos.familiy,
                        }

                        # Registrar la acción en el historial
                        registrar_accion('Editar', 'Géneros', generos.id, request.user, detalles='Se editó uno o más campos de un recurso de Géneros.', datos_formulario=datos_formulario)
                        ############## REGISTRO EN EL HISTORIAL ##############

                        if nombre_anterior != generos.genero:
                            # Actualizar las tablas relacionadas
                            EspecimenesFotos.objects.filter(genus=nombre_anterior).update(genus=generos.genero)
                            Especies.objects.filter(genus=nombre_anterior).update(genus=generos.genero)
                            EspeciesExcluidas.objects.filter(genus=nombre_anterior).update(genus=generos.genero)
                            EspeciesFotosVivas.objects.filter(genus=nombre_anterior).update(genus=generos.genero)

                else:
                    # Si es una solicitud GET, mostrar el formulario con los datos actuales
                    form = GenerosForm(instance=generos)

                context = {
                    'user': user,
                    'form': form, 
                    'generos': generos,
                    'editar': True,
                    'title': item,
                    'subtitle': "Géneros",
                    'id': idToEdit,
                }

                # Renderizar la plantilla con el formulario
                return render(request, 'content.html', context)

            if searched:
                generos = Generos.objects.filter(genero__startswith=searched).values('genero', 'familiy', 'id').order_by('genero')
            else: 
                generos = Generos.objects.values('genero', 'familiy', 'id').order_by('genero')

            paginator = Paginator(generos, 100) 
            page_obj = paginator.get_page(page_number)  
            formGeneros = GenerosForm()

            # Contexto de la página
            context = {
                'user': user,
                'dependientes': list(some),
                'recursos':  list(generos),
                'form': formGeneros,
                'page_obj': page_obj,
                'title': "Manejo",
                'subtitle': "Géneros",
            }

            return render(request, 'content.html', context)
    ###############################################################


    # Acción por defecto
    return render(request, '404.html')
####################################### VISUALIZACIÓN DE CONTENIDO #######################################