from django.contrib import admin
from django.urls import include, path
from polls import views as polls_views
from cnn import views as cnn_views
from django.conf import settings
from django.conf.urls.static import static
# py ファイルを import することで html で py ファイルが利用可能になる
from polls.dash_apps.finished_apps import testplot, simpleexample, japanese_prefecture, avg_system_man

urlpatterns = [
    # polls ディレクトリと紐付け
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('cnn/', include('cnn.urls')),
    # 理由は分からないが、 django_plotly_dash のパスは必要
    # https://github.com/GibbsConsulting/django-plotly-dash/issues/117
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)