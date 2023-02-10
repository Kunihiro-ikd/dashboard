from django.urls import path
from cnn import views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

app_name = "cnn"
urlpatterns = [
    path('img_upload', views.upload_img, name='img_upload'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)