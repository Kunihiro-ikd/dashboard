from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.views.generic import TemplateView 
# import plotly.graph_objects as go
from polls.models import CO2
from django.db.models import Avg
import plotly.express as px
from polls.forms import DateForm
from plotly.offline import plot
import plotly.graph_objects as go

def home(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('home.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def about(request):
    template_name = "about.html"
    return render(request, template_name)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'demo/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'demo/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def demo(request):
    template_name = "demo/demo.html"
    start = request.GET.get('start')
    end = request.GET.get('end')

    co2 = CO2.objects.all()
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)
    print('views.py ---- make px.line')
    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )


    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'right',
            'x': 0.5
    })

    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, template_name, context)


def yearly_avg_co2(request):
    template_name = 'demo/demo.html'
    averages = CO2.objects.values('date__year').annotate(avg=Avg('average'))
    x = averages.values_list('date__year', flat=True)
    y = averages.values_list('avg', flat=True)

    fig = px.bar(x=x, y=y)
    fig.update_layout(title_text= 'Average CO2 ')

    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, template_name, context)



def japanese_salary(request):
    template_name = "demo/japanese_salary.html"
    start = request.GET.get('start')
    end = request.GET.get('end')
    co2 = CO2.objects.all()
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            # title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)]),
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return fig, plot_div

    plot1, plot2 =scatter()

    context ={
        'plot1': plot1.to_html(),
        'plot2': plot2,
        'form': DateForm()
    }

    return render(request, template_name, context)


def demo_japanese_prefecture(request):
    template_name = 'demo/japanese_prefecture.html'
    context = {}
    return render(request, template_name, context)

def avg_system_man(request):
    template_name = 'avg_system_man.html'
    context = {}
    return render(request, template_name, context)