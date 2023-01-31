from django.urls import path
from . import views
from django.conf.urls import include
# from polls.dash_apps.finished_apps import testplot

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('demo/',  views.demo, name='demo'),
    path('japanese_salary/', views.japanese_salary, name='japanese_salary'),
    # path('japanese_salary/', include('django_plotly_dash.urls')),
    path('bar/',  views.yearly_avg_co2, name='bar-test'),
    path('demo_japanese_prefecture/', views.demo_japanese_prefecture, name="demo-prefecture"),
    # システムエンジニア（男性）の年収
    path('avg_system_man/', views.avg_system_man, name="dashboard-avg-system-man"),
    # 'bar= url のパス, views.関数, name=わかりやすい名前（パスを変えた時でもhtml 側で {% url 'name'%}を取ることができる）
]