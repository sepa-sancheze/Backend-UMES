from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Faculty, Department, Program
from .serializers import FacultySerializer, DepartmentSerializer, ProgramSerializer


# --- Faculty ---

class FacultyListView(APIView):
    def get(self, request):
        faculties = Faculty.objects.filter(is_deleted=False)
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Faculty, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = FacultySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = FacultySerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = FacultySerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Department ---

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.filter(is_deleted=False).select_related('faculty')
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Department, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = DepartmentSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = DepartmentSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = DepartmentSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Program ---

class ProgramListView(APIView):
    def get(self, request):
        programs = Program.objects.filter(is_deleted=False).select_related('department')
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgramDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Program, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = ProgramSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = ProgramSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = ProgramSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
