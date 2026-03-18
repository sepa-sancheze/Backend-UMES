from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<uuid:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
]
