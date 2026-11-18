from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Role, User


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'status', 'created')
    exclude = ('created_id', 'modified_id')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_id = request.user.id or 1
        obj.modified_id = request.user.id or 1
        super().save_model(request, obj, form, change)


class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'status')
    list_filter = ('role', 'is_staff', 'is_superuser', 'status')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'username')}),
        ('Rol y permisos', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'status'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.username:
            obj.username = obj.email
        if not obj.pk:
            obj.created_id = request.user.id or 1
        obj.modified_id = request.user.id or 1
        super().save_model(request, obj, form, change)


admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)