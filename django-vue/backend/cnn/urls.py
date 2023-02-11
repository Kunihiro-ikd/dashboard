from django.urls import path
from cnn import views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

app_name = "cnn"
urlpatterns = [
    path('img_upload', views.img_upload, name='img_upload'),
    path('nueral_style', views.nueral_style, name='nueral_style'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




