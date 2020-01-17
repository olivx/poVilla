from django.contrib import admin

# Register your models here.
from .models import Disciplina , Local, Mailbag, Request, PO, Servico

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin): 

    list_filter =('name',)
    search_fields =('__all__',)

@admin.register(Servico)
class ServicolinaAdmin(admin.ModelAdmin): 

    list_filter =('nome',)
    search_fields =('__all__',)

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):

    list_filter = ('name',)
    search_fields =('name',)

@admin.register(Mailbag)
class MailbagAdmin(admin.ModelAdmin):

    list_display = ('alias', 'local', 'entrega',)
    list_filter = ('entrega',)
    search_fields =('alias','user__first_name', 'user__last_name', )

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):

    search_fields =('name',)


@admin.register(PO)
class POAdmin(admin.ModelAdmin):

    search_fields =('__all__',)
    list_display = ('po', 'servico', 'request',)

 




    