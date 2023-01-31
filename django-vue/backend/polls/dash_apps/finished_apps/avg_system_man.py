# -*- coding: utf-8 -*-
from dash import dcc
from dash import html
from dash.dependencies import ALL, MATCH, Input, Output, State
from django_plotly_dash import DjangoDash
from django.conf import settings

import numpy as np
import pandas as pd
import plotly.express as px
import json
import geopandas as gpd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

data_path = settings.BASE_DIR / 'backend' / 'data' 

# データの読み込み
df_all = pd.read_csv(data_path / 'avg_system_man.csv')

# 転値 dataframe の作成 都道府県ごとの推移
df_transpose = df_all.set_index("都道府県").T
df_transpose = df_transpose.reset_index().rename(columns={"index": "年度"})

# 地理データの読み込み
jsonfile = gpd.read_file(data_path / 'japan.geojson')

df = df_all.dropna()
dfjson = json.loads(jsonfile.to_json())

app = DjangoDash(
    'AvgSystemMan',
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([
    html.Div(
        html.H1(
            '都道府県別 システムエンジニアの年収（男性）',
            style={
                'textAlign': 'center',
                'margin':'3% auto'
                # 'color': '#2e8b57'
            })),
    dcc.Markdown(
                '''    
                表示したい年度を選んでください。※データがない場合、0として計算しています。
                ''',
             style={
                 'textAlign': 'center',
                 'margin': '1% auto'
             }),
    html.Div(
        dcc.Dropdown(
            id='selectplace',
            options=[{
                'label': i,
                'value': i
            } for i in df.columns.drop('都道府県')],
            value=df.columns[35],
            style={
                'width': 800,
                'margin': '1% auto',
                'textAlign':'center',
            })),
    html.Div(
        dcc.Loading(children=dcc.Graph(
            id='japanmap',
            style={
                'width': 1000,
                'height': 400,
                'margin': '1% auto'
            }))),
    html.Div(
        dcc.Loading(
            children=dcc.Graph(
                id='hist',
                style={
                    'width': 1100,
                    'height': 300,
                    'margin': '1% auto'
                }))),
    html.Div(
        html.H1(
            'システムエンジニアの年収（男性）の推移',
            style={
                'textAlign': 'center',
                'margin':'3% auto'
            })),
    html.Div(
        dcc.Dropdown(
            id='select_prefecture_year',
            options=[
                {
                'label': i,
                'value': i
                } for i in df_transpose.columns.drop('年度')
            ],
            value=df_transpose.columns[13],
            multi=True,
            style={
                'width': 800,
                'margin': '1% auto',
                'textAlign':'center',
            })),
    html.Div(
        dcc.Loading(
            children=dcc.Graph(
                id='year_transition',
                style={
                    'width': 1100,
                    'height': 500,
                    'margin': '1% auto'
                },
            ))),
    # TODO Slider の実装
])


@app.callback(
    Output('japanmap', 'figure'),
    [Input('selectplace', 'value')]
)
def update_map(selected_value):
    selectdf = df[selected_value]
    fig = px.choropleth_mapbox(
        selectdf,
        geojson=dfjson,
        locations=df['都道府県'],
        color=selectdf,
        featureidkey='properties.nam_ja',
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=3.6,
        center={"lat": 36,"lon": 138},
        opacity=0.7,
        labels={"2015年": "2015年"}
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output('hist', 'figure'),
    [Input('selectplace', 'value')]
)
def draw_graph(selected_value):
    df_sort = df.sort_values(by=selected_value)
    df_sort['順位'] = np.arange(47, 0, -1)
    fig = px.bar(
        df_sort,
        x='都道府県',
        y=selected_value,
        color=selected_value,
        color_continuous_scale="Viridis",
        hover_data=['順位'],
        title=f'{selected_value} 都道府県の平均年収の比較',
    )
    fig.update(layout_coloraxis_showscale=False)
    fig.update_layout(
        xaxis=dict(title='都道府県'),
        yaxis=dict(title='平均年収(千円)'),
    )
    return fig


@app.callback(Output('year_transition', 'figure'), [Input('select_prefecture_year', 'value')])
def draw_graph_year_transition(selected_value):
    fig = px.line(
        df_transpose,
        x='年度',
        y=selected_value,
        title=f'{selected_value}  ※データが無い年は 0 としてプロット',
        markers=True,
    )
    fig.update_layout(
        xaxis=dict(title='年度'),
        yaxis=dict(title='平均年収(千円)'),
    )
    fig.update(layout_coloraxis_showscale=False)
    return fig
