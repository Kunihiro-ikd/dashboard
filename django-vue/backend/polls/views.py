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
from django.db.models import Avg
import plotly.express as px
from polls.forms import DateForm
from plotly.offline import plot
import plotly.graph_objects as go

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # ここに原因がありそう。チュートリアルのコードではエラーが出る。
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


def demo(request):
    template_name = "demo.html"
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
    averages = CO2.objects.values('date__year').annotate(avg=Avg('average'))
    x = averages.values_list('date__year', flat=True)
    y = averages.values_list('avg', flat=True)

    fig = px.bar(x=x, y=y)
    fig.update_layout(title_text= 'Average CO2 ')

    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'demo.html', context)



def japanese_salary(request):
    template_name = "japanese_salary.html"
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

# 
def django_plotly_dash(request):
    context = {}
    return render(request, 'django_plotly_dash.html',context)