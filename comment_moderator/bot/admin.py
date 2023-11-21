from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'status', 'created_at')
    list_filter = ('status',)  
    search_fields = ('text',)  
    ordering = ('-created_at',)
