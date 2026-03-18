from rest_framework import serializers
from .models import Subject, ClassSection, Schedule


class SubjectSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'code', 'name', 'program', 'program_name',
            'credits', 'semester', 'description', 'is_mandatory',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'section', 'day_of_week', 'day_of_week_display',
            'start_time', 'end_time',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClassSectionSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    enrolled_count = serializers.IntegerField(read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = ClassSection
        fields = [
            'id', 'section_code', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'academic_year', 'semester',
            'period', 'classroom', 'max_capacity', 'enrolled_count', 'is_open',
            'schedules',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_teacher_name(self, obj):
        return obj.teacher.full_name
