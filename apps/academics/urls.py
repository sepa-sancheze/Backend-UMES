from django.urls import path
from . import views

urlpatterns = [
    path('faculties/', views.FacultyListView.as_view(), name='faculty-list'),
    path('faculties/<uuid:pk>/', views.FacultyDetailView.as_view(), name='faculty-detail'),
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<uuid:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('programs/', views.ProgramListView.as_view(), name='program-list'),
    path('programs/<uuid:pk>/', views.ProgramDetailView.as_view(), name='program-detail'),
]
