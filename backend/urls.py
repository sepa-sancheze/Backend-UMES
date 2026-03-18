from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'UMES Administration'
admin.site.site_title = 'UMES Admin'
admin.site.index_title = 'University Management System'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.academics.urls')),
    path('api/v1/', include('apps.students.urls')),
    path('api/v1/', include('apps.staff.urls')),
    path('api/v1/', include('apps.classes.urls')),
    path('api/v1/', include('apps.enrollments.urls')),
]
