from rest_framework import serializers
from .models import Faculty, Department, Program


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = [
            'id', 'name', 'code', 'description', 'dean_name',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)

    class Meta:
        model = Department
        fields = [
            'id', 'faculty', 'faculty_name', 'name', 'code',
            'description', 'head_name',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProgramSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Program
        fields = [
            'id', 'department', 'department_name', 'name', 'code', 'level',
            'duration_semesters', 'total_credits', 'description', 'is_active',
            'created_at', 'updated_at', 'is_deleted', 'deleted_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
