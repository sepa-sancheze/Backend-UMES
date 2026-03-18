from django.contrib import admin
from .models import Enrollment, Grade


class GradeInline(admin.StackedInline):
    model = Grade
    extra = 0
    fields = ('numeric_grade', 'letter_grade', 'graded_at', 'graded_by', 'notes', 'is_deleted')
    readonly_fields = ('id', 'created_at', 'updated_at')
    autocomplete_fields = ('graded_by',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student', 'section', 'status', 'enrolled_date',
        'has_grade', 'is_deleted', 'created_at',
    )
    list_filter = ('status', 'is_deleted', 'section__subject__program__department__faculty')
    search_fields = (
        'student__first_name', 'student__last_name', 'student__student_id',
        'section__subject__name', 'section__subject__code',
    )
    readonly_fields = ('id', 'enrolled_date', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('student', 'section')
    inlines = [GradeInline]
    ordering = ('-enrolled_date',)
    date_hierarchy = 'enrolled_date'

    def has_grade(self, obj):
        return hasattr(obj, 'grade')
    has_grade.boolean = True
    has_grade.short_description = 'Graded'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment', 'numeric_grade', 'letter_grade',
        'graded_by', 'graded_at', 'is_deleted',
    )
    list_filter = ('letter_grade', 'is_deleted')
    search_fields = (
        'enrollment__student__first_name', 'enrollment__student__last_name',
        'enrollment__section__subject__name',
    )
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('graded_by',)
    ordering = ('-graded_at',)
