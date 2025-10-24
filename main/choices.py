from login.models import Codigos, Especies, Familias, Generos, Divisiones, EspeciesFotosVivas, Colectores

# Librerías de manejo de usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Opciones del seleccionador Familia
def get_family_choices():
    familias = Familias.objects.values_list('familia', flat=True).order_by('familia') 
    return [('', 'Seleccionar Familia... *')] + [(familia, familia) for familia in familias]

# Opciones del seleccionador Especie
def get_species_choices():
    especies = Especies.objects.values_list('nombre_cientifico', flat=True).order_by('nombre_cientifico')
    return [('', 'Seleccionar Especie... *')] + [(especie, especie) for especie in especies]

# Opciones del seleccionador Códigos
def get_code_choices():
    codigos = Codigos.objects.values_list('codigo', flat=True).order_by('codigo')
    return [('', 'Seleccionar Código...')] + [(codigo, codigo) for codigo in codigos]

# Opciones del seleccionador de Divisiones
def get_division_choices():
    divisiones = Divisiones.objects.values_list('division', flat=True).order_by('division')
    return [('', 'Seleccionar División...')] + [(division, division) for division in divisiones]

# Opciones del seleccionador de Colectores
def get_collector_choices():
    colectores = Colectores.objects.values_list('colector', flat=True).order_by('colector')
    return [('', 'Seleccionar Colector... *')] + [(colector, colector) for colector in colectores]

# Opciones del seleccionador de Géneros
def get_genus_choices():
    generos = Generos.objects.values_list('genero', flat=True).order_by('genero')
    return [('', 'Seleccionar Género...')] + [(genero, genero) for genero in generos]

# Opciones del seleccionador de Fotos - No me acuerdo dónde se usa y si se usa, realmente podría tener una mejor implementación :p
def get_photo_choices():
    photo_names = EspeciesFotosVivas.objects.values_list('photo_name', flat=True).order_by('photo_name')
    return [('', 'Seleccionar Foto...')] + [(photo_name, photo_name) for photo_name in photo_names]


###########################################################################################################
# Hay ciertos problemas, pues no se cargan dinámicamente estos valores, cuando hay una actualización, no
# se recalculan


# Opciones del seleccionador Familia
# familias = Familias.objects.values_list('familia', flat=True).order_by('familia') 
# FAMILY_CHOICES = [('', 'Seleccionar Familia... *')] + [(familia, familia) for familia in familias]
# # Opciones del seleccionador Especie
# especies = Especies.objects.values_list('nombre_cientifico', flat=True).order_by('nombre_cientifico') 
# ESPECIES_CHOICES = [('', 'Seleccionar Especie... *')] + [(especie, especie) for especie in especies]
# # Opciones del seleccionador Codigos
# codigos = Codigos.objects.values_list('codigo', flat=True).order_by('codigo')
# CODE_CHOICES = [('', 'Seleccionar Código...')] + [(codigo, codigo) for codigo in codigos]
# # Opciones del seleccionador de divisiones
# divisiones = Divisiones.objects.values_list('division', flat=True).order_by('division')
# DIVISION_CHOICES = [('', 'Seleccionar División...')] + [(division, division) for division in divisiones]
# # Opciones del seleccionador de colectores
# colectores = Colectores.objects.values_list('colector', flat=True).order_by('colector')
# COLECTOR_CHOICES = [('', 'Seleccionar Colector... *')] + [(colector, colector) for colector in colectores]
# # Opciones del seleccionador de generos
# generos = Generos.objects.values_list('genero', flat=True).order_by('genero')
# GENERO_CHOICES = [('', 'Seleccionar Genero...')] + [(genero, genero) for genero in generos]
# # Opciones del seleccionador de Fotos
# photo_names = EspeciesFotosVivas.objects.values_list('photo_name', flat=True).order_by('photo_name')
# PHOTO_CHOICES = [('', 'Seleccionar Foto...')] + [(photo_name, photo_name) for photo_name in photo_names]

###########################################################################################################