"""Stores admin - LEGACY, desativado.

Os modelos de stores foram consolidados no app 'commerce'.
Use commerce/admin.py para gerenciar Store, Product, Order, etc.
"""
from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Versão legada - mantido apenas para compatibilidade.
    Use commerce.StoreAdmin para o novo painel.
    """
    list_display = ['name', 'slug', 'phone', 'email', 'owner']
    list_filter = ['created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    def get_model_perms(self, request):
        """Não mostrar no índice do admin para evitar confusão."""
        return {}
