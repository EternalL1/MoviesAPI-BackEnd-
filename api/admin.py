from django.contrib import admin
from .models import Movie
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'average_rating')
    search_fields = ('title', 'genre')

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'phoneNumber', 'fullName', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'phoneNumber', 'fullName')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'phoneNumber', 'fullName', 'password')}),
        ('Permissions', {'fields': ('role', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phoneNumber', 'fullName', 'password', 'role', 'is_active'),
        }),
    )

    filter_horizontal = ()
    list_display_links = ('email',)

admin.site.register(User, CustomUserAdmin)