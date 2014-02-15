from django.contrib import admin
from .models import Board

class BoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'public')

    def public(self, b):
        return not b.is_hidden
    public.boolean = True

admin.site.register(Board, BoardAdmin)
