from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'full_name', 'email', 'program',
        'current_semester', 'status', 'is_deleted', 'enrollment_date',
    )
    list_filter = ('status', 'is_deleted', 'program__department__faculty', 'current_semester')
    search_fields = ('first_name', 'last_name', 'email', 'student_id', 'program__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('program',)
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'enrollment_date'
