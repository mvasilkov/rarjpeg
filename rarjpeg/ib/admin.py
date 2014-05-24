from django.contrib import admin
from .models import Board, Message


class BoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'public')

    def public(self, b):
        return not b.is_hidden
    public.boolean = True


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'board', 'pubdate')
    readonly_fields = ('parent', 'reply_to')

admin.site.register(Board, BoardAdmin)
admin.site.register(Message, MessageAdmin)
