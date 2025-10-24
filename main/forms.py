from django import forms
from login.models import *

# Librerías de manejo de usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .choices import *



class FamiliaForm(forms.ModelForm):

    # Opciones del seleccionador de Divisiones
    division = forms.ChoiceField(
    choices=get_division_choices,
    label="División",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Familias
        
        fields = ['familia', 'division', 'descripcion', 'comentario']

        # Atributos adicionales de los campos
        widgets = {
            'familia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la familia *'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'comentario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comentario'}),
        }
            # Labels personalizados
        labels = {
            'familia': 'Familia (Obligatorio)',
        }

    # Añadir campos requeridos
    def __init__(self, *args, **kwargs):
        super(FamiliaForm, self).__init__(*args, **kwargs)
        self.fields['familia'].required = True

        # Campos para actualización de dropdown
        self.fields['division'].choices = get_division_choices()



class EspecieForm(forms.ModelForm):

    # Opciones del seleccionador de Familias
    familia = forms.ChoiceField(
    choices=get_family_choices,
    label="Familia (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Códigos
    codigo = forms.ChoiceField(
    choices=get_code_choices,
    label="Código de la especie utilizado en la estación",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Géneros
    genus = forms.ChoiceField(
    choices=get_genus_choices,
    label="Género",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Especies

        fields = ['nombre_cientifico','familia','codigo', 'nombre_comun', 
        'sinonimos', 'species_authors', 'genus', 'sp1', 'author1', 'rank1', 'sp2', 
        'author2', 'habito', 'tallos', 'hojas', 'inflorescencia', 'frutos', 'soros',
        'distribucion', 'nota']

        # Atributos adicionales de los campos
        widgets = {
            'nombre_cientifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre científico de la Especie *'}),
            'nombre_comun': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre común de la especie en Puerto Rico'}),
            'sinonimos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre alternativo de la Especie'}),
            'species_authors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores de la especie'}),
            'sp1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Epíteto Específico'}),
            'author1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores extra'}),
            'rank1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subespecie o variedad'}),
            'sp2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Subespecie'}),
            'author2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores de la subespecie'}),
            'habito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hábito de la planta'}),
            'tallos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del tallo/tronco'}),
            'hojas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de las hojas'}),
            'inflorescencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la inflorescencia'}),
            'frutos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de los frutos'}),
            'soros': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de los soros'}),
            'distribucion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Distribución geográfica'}),
            'nota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notas adicionales'}),
        }
            
        # Labels personalizados
        labels = {
            'nombre_cientifico': 'Nombre Científico (Obligatorio)',
            'nombre_comun': 'Nombre Común',
            'sinonimos': 'Sinónimos',
            'species_authors': 'Autores de la Especie',
            'rank1': 'Subespecie o variedad',
            'sp1': 'Epíteto Específico',
            'author1': 'Autores Extra',
            'sp2': 'Subespecie', 
            'author2': 'Autores de la Subespecie',
            'habito': 'Hábito',
            'tallos': 'Tallos',
            'hojas': 'Hojas',
            'inflorescencia': 'Inflorescencia y Flores',
            'frutos': 'Frutos',
            'soros': 'Soros',
            'distribucion': 'Distribución de la Especie',
            'nota': 'Notas Adicionales',
        }

    def __init__(self, *args, **kwargs):
        super(EspecieForm, self).__init__(*args, **kwargs)
        self.fields['nombre_cientifico'].required = True
        self.fields['familia'].required = True

        # Campos para actualización de dropdown
        self.fields['familia'].choices = get_family_choices()
        self.fields['genus'].choices = get_genus_choices()
        self.fields['codigo'].choices = get_code_choices()



class EspecimenForm(forms.ModelForm):

    # Opciones del seleccionador de Divisiones
    division = forms.ChoiceField(
    choices=get_division_choices,
    label="División",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Especie
    species = forms.ChoiceField(
    choices=get_species_choices,
    label="Nombre Científico (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Familias
    familiy = forms.ChoiceField(
    choices=get_family_choices,
    label="Familia (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Códigos
    code = forms.ChoiceField(
    choices=get_code_choices,
    label="Código de la especie utilizado en la estación",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Géneros
    genus = forms.ChoiceField(
    choices=get_genus_choices,
    label="Género",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Géneros
    collector = forms.ChoiceField(
    choices=get_collector_choices,
    label="Colector (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = EspecimenesFotos

        fields = ['familiy', 'species', 'photoname', 'barcode', 'accesion', 'collector', 'number', 
        'addcoll', 'herb', 'day', 'month', 'year', 'division',  
        'code', 'species_authors', 'detby', 'detdate', 'plantdesc', 'habitat',
        'lat', 'long', 'altitude', 'geodata', 'notes', 'genus', 'sp1', 'author1', 'rank1', 'sp2', 'author2']

        # Opciones para el día
        DAY_CHOICES = [(str(i), str(i)) for i in range(1, 32)]
        
        # Opciones para el mes
        MONTH_CHOICES = [
            ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'),
            ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
            ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'),
            ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
        ]
        
        # Opciones para el año
        YEAR_CHOICES = [(str(i), str(i)) for i in range(1950, 2100)]

        # Atributos adicionales de los campos
        widgets = {
            'photoname': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número del código de barra del especímen'}),
            'accesion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de entrada al herbario'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de colección del colector'}),
            'addcoll': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colectores adicionales (apellido, iniciales)'}),
            'herb': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Herbario donde se encuentra el especímen'}),
            'day': forms.Select(choices=DAY_CHOICES, attrs={'class': 'form-control'}),
            'month': forms.Select(choices=MONTH_CHOICES, attrs={'class': 'form-control'}),
            'year': forms.Select(choices=YEAR_CHOICES, attrs={'class': 'form-control'}),
            'species_authors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores de la especie'}),
            'detby': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido, iniciales'}),
            'detdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha (YYYY-MM-DD)', 'type': 'date'}),
            'plantdesc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la inflorescencia'}),
            'habitat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rocky wet ravine on E side of road.'}),
            'lat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "17.7"}),
            'long': forms.TextInput(attrs={'class': 'form-control',  'placeholder': "67.85"}),
            'altitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "100m"}),
            'geodata': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Luquillo, research forest near the El Verde Station.'}),
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notas adicionales'}),
            'sp1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Epíteto Específico'}),
            'author1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores de la especie'}),
            'rank1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subespecie (subsp.) o variedad (var.)'}),
            'sp2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subespecie o variedad'}),
            'author2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores de la subespecie o variedad'}),
        }
            

        # Labels personalizados
        labels = {
            'photoname': 'Foto',
            'division': 'División',
            'species_authors': 'Autores de la Especie',
            'rank1': 'Subespecie o variedad',
            'sp1': 'Epíteto Específico',
            'author1': 'Autores Extra',
            'sp2': 'Subespecie', 
            'author2': 'Autores de la Subespecie',
            'detby': 'Persona que hizo la identificación del espécimen',
            'lat': 'Latitud',
            'long': 'Longitud',
            'altitude': 'Altitud',
            'geodata': 'Localidad geográfica donde se colectó el espécimen',
            'addcoll': 'Colectores adicionales',
            'number': 'Número de colector',
            'accesion': 'Número de entrada al herbario',
            'detdate': 'Fecha en que se hizo la identificación',
            'plantdesc': 'Descripción de la inflorescencia',
            'herb': 'Herbario donde se encuentra depositado el especímen',
            'notes': 'Notas Adicionales',
        }

    def __init__(self, *args, **kwargs):
        super(EspecimenForm, self).__init__(*args, **kwargs)

        self.fields['species'].required = True
        self.fields['familiy'].required = True
        self.fields['collector'].required = True

        # Campos para actualización de dropdown
        self.fields['species'].choices = get_species_choices()
        self.fields['familiy'].choices = get_family_choices()
        self.fields['genus'].choices = get_genus_choices()
        self.fields['code'].choices = get_code_choices()
        self.fields['collector'].choices = get_collector_choices()
        self.fields['division'].choices = get_division_choices()

        # Si ya hay un archivo subido, muestra su nombre
        if self.instance and self.instance.photoname:
            self.fields['photoname'].label = f"Foto (actual: {self.instance.photoname})"



class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@ejemplo.com'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre.Apellido'}),
        }

        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de error
        self.fields['username'].error_messages = {'required': 'Este campo es obligatorio.'}
        self.fields['email'].error_messages = {'required': 'Este campo es obligatorio.', 'invalid': 'Ingrese un correo electrónico válido.'}
        self.fields['password1'].error_messages = {'required': 'Este campo es obligatorio.'}
        self.fields['password2'].error_messages = {'required': 'Este campo es obligatorio.'}



class EspeciesFotosVivasForm(forms.ModelForm):

    # Opciones del seleccionador de Especie
    species = forms.ChoiceField(
    choices=get_species_choices,
    label="Nombre Científico (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Familias
    familiy = forms.ChoiceField(
    choices=get_family_choices,
    label="Familia (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Opciones del seleccionador de Géneros
    genus = forms.ChoiceField(
    choices=get_genus_choices,
    label="Género",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = EspeciesFotosVivas
        fields = [
            'familiy', 'photo_name', 'gallery', 'comment', 'species', 
            'species_authors', 'genus', 'sp1', 'author1', 'rank1', 
            'sp2', 'author2', 'rank2']

        # Estos valores son importantes, créanme :^)
        GALLERY_CHOICES = [
            ('', 'Seleccionar Grupo'),
            ('fru', 'Frutos'),
            ('floama', 'Flores Amarillas y Anaranjadas'),
            ('floazu', 'Flores Azules y Púrpuras'),
            ('flobla', 'Flores Blancas y Verdosas'),
            ('floro', 'Flores Rosadas y Rojas'),
            ('cor', 'Cortezas'),
            ('hel', 'Helechos'),
            ('gram', 'Gramíneas y Ciperáceas'),
        ]

        widgets = {
            'photo_name': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gallery': forms.Select(choices=GALLERY_CHOICES, attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Comentario breve'}),
            'species_authors': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Autores del nombre'}),
            'sp1': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Epíteto específico'}),
            'author1': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Autor 1'}),
            'rank1': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Rango 1 (sp., var., etc.)'}),
            'sp2': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Subespecie/variedad'}),
            'author2': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Autor 2'}),
            'rank2': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Rango 2'}),
        }

        # Labels personalizados
        labels = {
            'photo_name': 'Foto',
            'division': 'División',
            'gallery': 'Grupo',
            'species_authors': 'Autores de la Especie',
            'rank1': 'Subespecie o variedad',
            'sp1': 'Epíteto Específico',
            'author1': 'Autores Extra',
            'sp2': 'Subespecie', 
            'author2': 'Autores de la Subespecie',
            'comment': 'Notas Adicionales',
        }

    def __init__(self, *args, **kwargs):
        super(EspeciesFotosVivasForm, self).__init__(*args, **kwargs)

        self.fields['species'].required = True
        self.fields['familiy'].required = True

        # Campos para actualización de dropdown
        self.fields['species'].choices = get_species_choices()
        self.fields['familiy'].choices = get_family_choices()
        self.fields['genus'].choices = get_genus_choices()

        # Si ya hay un archivo subido, muestra su nombre
        if self.instance and self.instance.photo_name:
            self.fields['photo_name'].label = f"Foto (actual: {self.instance.photo_name})"



################################################ Manejo y Recursos ################################################
class GenerosForm(forms.ModelForm):

    # Opciones del seleccionador de Familias
    familiy = forms.ChoiceField(
    choices=get_family_choices,
    label="Familia (Obligatorio)",
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Generos
        fields = ['genero', 'familiy']
        widgets = {
            'genero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Quercus'}),
            'familiy': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Fagaceae'}),
        }

    def __init__(self, *args, **kwargs):
        super(GenerosForm, self).__init__(*args, **kwargs)
        self.fields['genero'].required = True

        # Campos para actualización de dropdown
        self.fields['familiy'].choices = get_family_choices()



class GlosarioForm(forms.ModelForm):
    class Meta:
        model = Glosario
        fields = ['termino', 'definicion', 'c']
        widgets = {
            'termino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Hábito'}),
            'definicion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del término...'}),
            'c': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: (opcional)'}),
        }



class LiteraturaForm(forms.ModelForm):
    class Meta:
        model = Literatura
        fields = ['citada']
        widgets = {
            'citada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Author, A. (2023). Title...'}),
        }



class EspeciesExcluidasForm(forms.ModelForm):

    # Opciones del seleccionador de Géneros
    genus = forms.ChoiceField(
    choices=get_genus_choices,
    label="Género",
    required = False,
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = EspeciesExcluidas
        fields = [
            'nombre_cientifico', 'species_authors', 'genus',
            'sp1', 'autor1', 'rank1', 'sp2', 'autor2', 'comentario'
        ]
        widgets = {
            'nombre_cientifico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la especie'}),
            'species_authors': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autores del nombre'}),
            'sp1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ilex'}),
            'autor1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: L.'}),
            'rank1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: sp.'}),
            'sp2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ballota'}),
            'autor2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Desf.'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Razón de exclusión...'}),
        }

        labels = {
            'nombre_cientifico': 'Nombre de la Especie',
            'species_authors': 'Autores de la Especie',
            'rank1': 'Subespecie o variedad',
            'sp1': 'Epíteto Específico',
            'author1': 'Autores Extra',
            'sp2': 'Subespecie', 
            'author2': 'Autores de la Subespecie',
            'comentario': 'Notas Adicionales',
        }
    
    def __init__(self, *args, **kwargs):
        super(EspeciesExcluidasForm, self).__init__(*args, **kwargs)
        self.fields['nombre_cientifico'].required = True

        # Campos para actualización de dropdown
        self.fields['genus'].choices = get_genus_choices()



class CodigosForm(forms.ModelForm):
    class Meta:
        model = Codigos
        fields = ['codigo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC123'}),
        }



class ColectoresForm(forms.ModelForm):
    class Meta:
        model = Colectores
        fields = ['colector']
        widgets = {
            'colector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: John Doe'}),
        }



class DivisionesForm(forms.ModelForm):
    class Meta:
        model = Divisiones
        fields = ['division']
        widgets = {
            'division': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej: Magnoliophyta'}),
        }
################################################ Manejo y Recursos ################################################