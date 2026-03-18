from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'employee_id', 'full_name', 'email', 'department',
        'contract_type', 'academic_degree', 'is_active', 'is_deleted', 'hire_date',
    )
    list_filter = ('contract_type', 'is_active', 'is_deleted', 'department__faculty')
    search_fields = ('first_name', 'last_name', 'email', 'employee_id', 'department__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('department',)
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'hire_date'
