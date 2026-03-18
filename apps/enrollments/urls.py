from django.urls import path
from . import views

urlpatterns = [
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<uuid:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('grades/', views.GradeListView.as_view(), name='grade-list'),
    path('grades/<uuid:pk>/', views.GradeDetailView.as_view(), name='grade-detail'),
]
