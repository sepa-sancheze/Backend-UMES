from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'date_of_birth', 'address',
            'program', 'program_name', 'enrollment_date',
            'current_semester', 'status',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
