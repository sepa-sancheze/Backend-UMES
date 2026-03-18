from django.contrib import admin
from .models import Faculty, Department, Program


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'dean_name', 'department_count', 'is_deleted', 'created_at')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'code', 'dean_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('name',)

    def department_count(self, obj):
        return obj.departments.filter(is_deleted=False).count()
    department_count.short_description = 'Departments'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty', 'head_name', 'program_count', 'is_deleted', 'created_at')  # noqa: E501
    list_filter = ('faculty', 'is_deleted')
    search_fields = ('name', 'code', 'head_name', 'faculty__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('faculty',)
    ordering = ('faculty__name', 'name')

    def program_count(self, obj):
        return obj.programs.filter(is_deleted=False).count()
    program_count.short_description = 'Programs'


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'department', 'level',
        'duration_semesters', 'total_credits', 'is_active', 'is_deleted', 'created_at',
    )
    list_filter = ('level', 'is_active', 'is_deleted', 'department__faculty')
    search_fields = ('name', 'code', 'department__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('department',)
    ordering = ('department__name', 'name')
