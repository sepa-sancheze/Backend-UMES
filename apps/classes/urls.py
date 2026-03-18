from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<uuid:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('sections/', views.ClassSectionListView.as_view(), name='section-list'),
    path('sections/<uuid:pk>/', views.ClassSectionDetailView.as_view(), name='section-detail'),
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/<uuid:pk>/', views.ScheduleDetailView.as_view(), name='schedule-detail'),
]
