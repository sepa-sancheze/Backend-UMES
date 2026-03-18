from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Teacher
from .serializers import TeacherSerializer


class TeacherListView(APIView):
    def get(self, request):
        teachers = Teacher.objects.filter(is_deleted=False).select_related('department')
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = TeacherSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = TeacherSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = TeacherSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
