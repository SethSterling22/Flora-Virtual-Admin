from django.contrib import admin

# Register your models here.
from .models import Codigos, Colectores, Divisiones, Especies
from .models import EspeciesExcluidas, EspeciesFotosVivas, EspecimenesFotos, Familias, Generos, Glosario, Literatura

# Registrar los modelos
admin.site.register(Codigos)
admin.site.register(Colectores)
admin.site.register(Divisiones)
admin.site.register(Especies)
admin.site.register(EspeciesExcluidas)
admin.site.register(EspeciesFotosVivas)
admin.site.register(EspecimenesFotos)
admin.site.register(Familias)
admin.site.register(Generos)
admin.site.register(Glosario)
admin.site.register(Literatura)
