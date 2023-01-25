from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView 
# import plotly.graph_objects as go
from polls.models import CO2
import plotly.express as px
from polls.forms import DateForm

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # ここに原因がありそう
    # template = loader.get_template('polls/index.html')
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})
    return render(request, 'detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})
    return render(request, 'results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# def line_charts():
    # fig = go.Figure(
    #     go.Scatter(x=[1, 2, 3], y=[3, 5, 2]), layout=go.Layout(width=400, height=400)
    # )
    # return fig.to_html(include_plotlyjs=False) 


def dashboard_japanese_salary(request):
    template_name = "dashboard_japanese_salary.html"
    start = request.GET.get('start')
    end = request.GET.get('end')
    print('----------')

    co2 = CO2.objects.all()
    print(co2, '\n------')
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
    })

    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, template_name, context)

 