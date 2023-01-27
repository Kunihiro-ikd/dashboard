from django.urls import path

from . import views

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
    path('japanese_salary/',  views.japanese_salary, name='japanese_salary'),
    # dashboard_japanese_salary.html で開いた方がよさそう
    path('bar/',  views.yearly_avg_co2, name='bar-test'),
    # 'bar= url のパス, views.関数, name=わかりやすい名前（パスを変えた時でもhtml 側で {% url 'name'%}を取ることができる）
]