from django.contrib import admin
from .models import Subject, ClassSection, Schedule


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = ('day_of_week', 'start_time', 'end_time', 'is_deleted')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'program', 'semester',
        'credits', 'is_mandatory', 'is_deleted', 'created_at',
    )
    list_filter = ('is_mandatory', 'is_deleted', 'semester', 'program__department__faculty')
    search_fields = ('name', 'code', 'program__name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('program',)
    ordering = ('program__name', 'semester', 'name')


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'subject', 'teacher', 'period',
        'classroom', 'max_capacity', 'enrolled_count', 'is_open', 'is_deleted',
    )
    list_filter = ('period', 'is_open', 'is_deleted', 'academic_year', 'semester')
    search_fields = ('section_code', 'subject__name', 'subject__code', 'teacher__last_name')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    autocomplete_fields = ('subject', 'teacher')
    inlines = [ScheduleInline]
    ordering = ('-academic_year', 'semester', 'subject__name')

    def enrolled_count(self, obj):
        return obj.enrolled_count
    enrolled_count.short_description = 'Enrolled'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'day_of_week', 'start_time', 'end_time', 'is_deleted')
    list_filter = ('day_of_week', 'is_deleted')
    search_fields = ('section__subject__name', 'section__section_code')
    readonly_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('section', 'day_of_week', 'start_time')
