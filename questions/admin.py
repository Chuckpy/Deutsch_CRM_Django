from django.contrib import admin
from .models import Questao, Resposta


class RespostasSet(admin.TabularInline):
    model = Resposta

class QuestoesAdmin(admin.ModelAdmin):
    inlines = [RespostasSet]


admin.site.register(Questao, QuestoesAdmin)
admin.site.register(Resposta)