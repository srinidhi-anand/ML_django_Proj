from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
     path('home/', views.class_view, name='home'),
     path('home/<value>', views.frames_display, name='view_images')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
