from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Enrollment, Grade
from .serializers import EnrollmentSerializer, GradeSerializer


# --- Enrollment ---

class EnrollmentListView(APIView):
    def get(self, request):
        enrollments = Enrollment.objects.filter(is_deleted=False).select_related(
            'student', 'section__subject'
        ).prefetch_related('grade')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Enrollment, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = EnrollmentSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = EnrollmentSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = EnrollmentSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Grade ---

class GradeListView(APIView):
    def get(self, request):
        grades = Grade.objects.filter(is_deleted=False).select_related(
            'enrollment__student', 'enrollment__section', 'graded_by'
        )
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Grade, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = GradeSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = GradeSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = GradeSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
