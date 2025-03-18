from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page_app.urls')),
    path('student/', include('student_portal.urls')),
    path('instructor/', include('instructor_portal.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
