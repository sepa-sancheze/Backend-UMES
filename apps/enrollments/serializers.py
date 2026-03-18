from rest_framework import serializers
from .models import Enrollment, Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = [
            'id', 'enrollment', 'numeric_grade', 'letter_grade',
            'graded_at', 'graded_by', 'notes',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    section_str = serializers.CharField(source='section.__str__', read_only=True)
    grade = GradeSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'section', 'section_str',
            'enrolled_date', 'status', 'notes', 'grade',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'enrolled_date', 'created_at', 'updated_at']

    def get_student_name(self, obj):
        return obj.student.full_name
