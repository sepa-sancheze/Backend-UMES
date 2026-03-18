from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Subject, ClassSection, Schedule
from .serializers import SubjectSerializer, ClassSectionSerializer, ScheduleSerializer


# --- Subject ---

class SubjectListView(APIView):
    def get(self, request):
        subjects = Subject.objects.filter(is_deleted=False).select_related('program')
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Subject, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = SubjectSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = SubjectSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = SubjectSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- ClassSection ---

class ClassSectionListView(APIView):
    def get(self, request):
        sections = ClassSection.objects.filter(is_deleted=False).select_related(
            'subject', 'teacher'
        ).prefetch_related('schedules')
        serializer = ClassSectionSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClassSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassSectionDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ClassSection, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = ClassSectionSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = ClassSectionSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = ClassSectionSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- Schedule ---

class ScheduleListView(APIView):
    def get(self, request):
        schedules = Schedule.objects.filter(is_deleted=False).select_related('section__subject')
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Schedule, pk=pk, is_deleted=False)

    def get(self, request, pk):
        serializer = ScheduleSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = ScheduleSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        serializer = ScheduleSerializer(self.get_object(pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.get_object(pk).soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
