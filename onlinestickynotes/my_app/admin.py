from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'content')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)