from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'UMES Administration'
admin.site.site_title = 'UMES Admin'
admin.site.index_title = 'University Management System'

API_PATH='api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PATH, include('apps.academics.urls')),
    path(API_PATH, include('apps.students.urls')),
    path(API_PATH, include('apps.staff.urls')),
    path(API_PATH, include('apps.classes.urls')),
    path(API_PATH, include('apps.enrollments.urls')),
]
