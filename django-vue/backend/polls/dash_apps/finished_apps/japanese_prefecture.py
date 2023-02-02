import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import ALL, MATCH, Input, Output, State
# import dash_bootstrap_components as dbc # bootstrap

import json
from django_plotly_dash import DjangoDash
import geopandas as gpd
from django.conf import settings

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_path = settings.BASE_DIR / 'backend' / 'data' 
# load data
df_all = pd.read_csv(data_path /'all_data.csv') # 統計で見る都道府県のすがた
# csv の都道府県のセルのデータ名と、geojson の properties.nam_ja を対応づける。対応づけられていなかった場合、地図へ色の反映はされない。
jsonfile = gpd.read_file(data_path / 'japan.geojson') # geodata

df = df_all.dropna()
dfjson = json.loads(jsonfile.to_json())

app = DjangoDash(
    'JapanesePrefecture',
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([
    html.Div(
        html.H1('都道府県データマップ',
                style={
                    'textAlign': 'center',
                    'margin':'3% auto'
                    # 'color': '#2e8b57'
                })),
    dcc.Markdown('''    
    表示したい項目を選んでください。
    ''',
             style={
                 'textAlign': 'center',
                 'margin': '1% auto'
             }),
    html.Div(
        dcc.Dropdown(id='selectplace',
                     options=[{
                         'label': i,
                         'value': i
                     } for i in df.columns.drop('都道府県')],
                     value=df.columns[1],
                     style={
                         'width': 800,
                         'margin': '1% auto',
                         'textAlign':'center',
                     })),
    html.Div(
        dcc.Loading(children=dcc.Graph(id='japanmap',
                                       style={
                                           'width': 1000,
                                           'height': 400,
                                           'margin': '1% auto'
                                       }))),
    html.Div(
        dcc.Loading(children=dcc.Graph(id='hist',
                                       style={
                                           'width': 1100,
                                           'height': 300,
                                           'margin': '1% auto'
                                       }))),
    
    html.Div(html.A(href="https://www.stat.go.jp/data/k-sugata/index.html",
                    target="_blank",
                    children='データ：統計でみる都道府県のすがた(総務省統計局)'),
             style={
                 'textAlign': 'center',
                 'margin': '3% auto'
             }),

])


@app.callback(Output('japanmap', 'figure'), [Input('selectplace', 'value')])
def update_map(selected_value):
    selectdf = df[selected_value]
    df_sort = df.sort_values(by=selected_value)
    df_sort['順位'] = np.arange(47, 0, -1)
    fig = px.choropleth_mapbox(
        selectdf,
        geojson=dfjson,
        locations=df['都道府県'],
        color=['順位'],
        hover_data=['順位'],
        featureidkey='properties.nam_ja',
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=3.6,
        center={"lat": 36,"lon": 138},
        opacity=0.7,
        labels={"総人口 (万人)": "総人口 (万人)"}
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(Output('hist', 'figure'), [Input('selectplace', 'value')])
def draw_graph(selected_value):
    df_sort = df.sort_values(by=selected_value)
    df_sort['順位'] = np.arange(47, 0, -1)
    fig = px.bar(df_sort,
                 x='都道府県',
                 y=selected_value,
                #  color=selected_value,
                 color_continuous_scale="Viridis",
                 hover_data=['順位'],
                 title=f'{selected_value}年度 平均年収')
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(yaxis_title='value')
    return fig
