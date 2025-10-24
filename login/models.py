# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Codigos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'codigos'


class Colectores(models.Model):
    id = models.AutoField(primary_key=True)
    colector = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'colectores'


class Divisiones(models.Model):
    id = models.AutoField(primary_key=True)
    division = models.TextField()

    class Meta:
        #managed = True
        db_table = 'divisiones'


class Especies(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_cientifico = models.TextField(blank=True, null=True)
    foto = models.TextField(blank=True, null=True)
    familia = models.TextField(blank=True, null=True)
    codigo = models.TextField(blank=True, null=True)
    nombre_comun = models.TextField(blank=True, null=True)
    sinonimos = models.TextField(blank=True, null=True)
    species_authors = models.TextField(blank=True, null=True)
    genus = models.TextField(blank=True, null=True)
    sp1 = models.TextField(blank=True, null=True)
    author1 = models.TextField(blank=True, null=True)
    rank1 = models.TextField(blank=True, null=True)
    sp2 = models.TextField(blank=True, null=True)
    author2 = models.TextField(blank=True, null=True)
    rank2 = models.TextField(blank=True, null=True)
    sp3 = models.TextField(blank=True, null=True)
    author3 = models.TextField(blank=True, null=True)
    habito = models.TextField(blank=True, null=True)
    tallos = models.TextField(blank=True, null=True)
    hojas = models.TextField(blank=True, null=True)
    inflorescencia = models.TextField(blank=True, null=True)
    frutos = models.TextField(blank=True, null=True)
    soros = models.TextField(blank=True, null=True)
    distribucion = models.TextField(blank=True, null=True)
    nota = models.TextField(blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'especies'


class EspeciesExcluidas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_cientifico = models.CharField(max_length=39, blank=True, null=True)
    species_authors = models.CharField(max_length=69, blank=True, null=True)
    genus = models.CharField(max_length=13, blank=True, null=True)
    sp1 = models.CharField(max_length=15, blank=True, null=True)
    autor1 = models.CharField(max_length=36, blank=True, null=True)
    rank1 = models.CharField(max_length=4, blank=True, null=True)
    sp2 = models.CharField(max_length=13, blank=True, null=True)
    autor2 = models.CharField(max_length=18, blank=True, null=True)
    comentario = models.CharField(max_length=582, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'especies_excluidas'


class EspeciesFotosVivas(models.Model):
    id = models.AutoField(primary_key=True)
    familiy = models.CharField(max_length=25, blank=True, null=True)
    photo_name = models.TextField(blank=True, null=True)
    gallery = models.CharField(max_length=6, blank=True, null=True)
    comment = models.CharField(max_length=20, blank=True, null=True)
    species = models.CharField(max_length=54, blank=True, null=True)
    species_authors = models.CharField(max_length=128, blank=True, null=True)
    genus = models.CharField(max_length=17, blank=True, null=True)
    sp1 = models.CharField(max_length=18, blank=True, null=True)
    author1 = models.CharField(max_length=51, blank=True, null=True)
    rank1 = models.CharField(max_length=6, blank=True, null=True)
    sp2 = models.CharField(max_length=13, blank=True, null=True)
    author2 = models.CharField(max_length=40, blank=True, null=True)
    rank2 = models.CharField(max_length=4, blank=True, null=True)
    sp3 = models.CharField(max_length=8, blank=True, null=True)
    author3 = models.CharField(max_length=33, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'especies_fotos_vivas'


class EspecimenesFotos(models.Model):
    id = models.AutoField(primary_key=True)
    photo1 = models.IntegerField(blank=True, null=True)
    photoname = models.TextField(blank=True, null=True)
    barcode = models.CharField(max_length=10, blank=True, null=True)
    accesion = models.IntegerField(blank=True, null=True)
    collector = models.CharField(max_length=30, blank=True, null=True)
    number = models.CharField(max_length=13, blank=True, null=True)
    addcoll = models.CharField(max_length=93, blank=True, null=True)
    herb = models.CharField(max_length=5, blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    collected = models.TextField(blank=True, null=True)
    monthname = models.CharField(max_length=9, blank=True, null=True)
    division = models.TextField(blank=True, null=True)
    familiy = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)
    species = models.TextField(blank=True, null=True)
    species_authors = models.TextField(blank=True, null=True)
    detby = models.CharField(max_length=47, blank=True, null=True)
    detdate = models.CharField(max_length=16, blank=True, null=True)
    plantdesc = models.TextField(blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    ns = models.CharField(max_length=1, blank=True, null=True)
    long = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    ew = models.CharField(max_length=1, blank=True, null=True)
    llunit = models.CharField(max_length=3, blank=True, null=True)
    latlong = models.TextField(blank=True, null=True)
    altitude = models.TextField(blank=True, null=True)
    geodata = models.TextField(blank=True, null=True)
    notes = models.CharField(max_length=123, blank=True, null=True)
    genus = models.CharField(max_length=17, blank=True, null=True)
    sp1 = models.CharField(max_length=28, blank=True, null=True)
    author1 = models.CharField(max_length=51, blank=True, null=True)
    rank1 = models.CharField(max_length=6, blank=True, null=True)
    sp2 = models.CharField(max_length=13, blank=True, null=True)
    author2 = models.CharField(max_length=40, blank=True, null=True)
    rank2 = models.CharField(max_length=4, blank=True, null=True)
    sp3 = models.CharField(max_length=8, blank=True, null=True)
    author3 = models.CharField(max_length=33, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'especimenes_fotos'


class Familias(models.Model):
    id = models.AutoField(primary_key=True)
    familia = models.TextField(blank=True, null=True)
    redirigir = models.TextField(blank=True, null=True)
    division = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    foto = models.TextField(blank=True, null=True)
    clave_int = models.TextField(blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'familias'


class Generos(models.Model):
    id = models.AutoField(primary_key=True)
    genero = models.CharField(max_length=17, blank=True, null=True)
    familiy = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'generos'


class Glosario(models.Model):
    id = models.AutoField(primary_key=True)
    termino = models.CharField(max_length=39, blank=True, null=True)
    definicion = models.CharField(max_length=337, blank=True, null=True)
    c = models.CharField(db_column='C', max_length=39, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = True
        db_table = 'glosario'


class Literatura(models.Model):
    id = models.AutoField(primary_key=True)
    citada = models.CharField(max_length=357, blank=True, null=True)

    class Meta:
        #managed = True
        db_table = 'literatura'
