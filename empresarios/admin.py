from django.contrib import admin
from .models import Empresa, Documento, Metrica
# Register your models here.

admin.site.register(Empresa)
admin.site.register(Documento)
admin.site.register(Metrica)