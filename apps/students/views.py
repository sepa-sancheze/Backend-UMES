from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer


class StudentListView(APIView):
    def get(self, request):
        students = Student.objects.filter(is_deleted=False).select_related('program')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = StudentSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = StudentSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = StudentSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
