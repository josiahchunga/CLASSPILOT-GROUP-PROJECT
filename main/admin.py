from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Announcement, Note, Assignment

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional info', {'fields': ('role', 'phone_number')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'message', 'author__username')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'description', 'author__username')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'description', 'author__username')
