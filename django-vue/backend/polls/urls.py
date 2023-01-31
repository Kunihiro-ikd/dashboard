from django.urls import path
from . import views
from django.conf.urls import include

app_name = "polls"
urlpatterns = [
    # 引数について説明する
    # 'home'url のパス, views.関数名, name=わかりやすい名前（html 側で {% url 'name'%}を用いてurlを取得可能）
    # ホーム画面
    path('', views.home, name='home'),
    # システムエンジニア（男性）の年収
    path('avg_system_man/', views.avg_system_man, name="dashboard-avg-system-man"),
    # 本サイトについて説明
    path('about', views.about, name='about'),

    ###########################
    ####  demo ################
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # plotly のサンプル
    path('demo/',  views.demo, name='demo'),
    path('demo/japanese_salary/', views.japanese_salary, name='japanese_salary'),
    path('demo/bar/',  views.yearly_avg_co2, name='bar-test'),
    path('demo/demo_japanese_prefecture/', views.demo_japanese_prefecture, name="demo-prefecture"),
    ####  demo ################
    ###########################
]