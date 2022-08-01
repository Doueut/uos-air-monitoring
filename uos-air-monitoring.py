import dash
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import os
import pandas as pd
from urllib import response
import requests, bs4
from bs4 import BeautifulSoup
import dash_bootstrap_components as dbc

# 1. 데이터 불러오기
# 1-1. 서울시 측정소별 데이터
url_sido = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?sidoName=서울&pageNo=1&numOfRows=100&returnType=xml&serviceKey=oWT24qOJcMA4Q2zt9d7iA2vpKXjFCsqZ6fiNJQRBYrp9NOq4yu8rhRkAhIKEwxbeeSVy%2FCK0dAZQi%2BchzGjwJA%3D%3D&ver=1.0'
# 현재시각 서울의 측정소 데이터들 모임
# serviceKey=~~ -> 공공데이터포털에서 받은 인증키
response=requests.get(url_sido).text.encode('utf-8')
xmlobj_sido=bs4.BeautifulSoup(response, 'lxml-xml')



# 2. API 데이터 dataframe에 넣기
# 2-1. 서울시 측정소별 데이터
rows_sido=xmlobj_sido.find_all('item')

rowList_sido=[]
nameList_sido=[]
columnList_sido=[]

rowsLen_sido=len(rows_sido)
for i in range(0,rowsLen_sido):
    columns_sido=rows_sido[i].find_all()

    columnsLen_sido=len(columns_sido)
    for j in range(0, columnsLen_sido):
        if i==0:
            nameList_sido.append(columns_sido[j].name)
        eachColumn_sido=columns_sido[j].text
        columnList_sido.append(eachColumn_sido)
    rowList_sido.append(columnList_sido)
    columnList_sido=[]


df_sido=pd.DataFrame(rowList_sido, columns=nameList_sido)
# print(df_sido['stationName']) # -> 데이터 확인



# 1-2. 동대문구 측정소 데이터
url_station = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName='+'동대문구'+'&dataTerm=month&pageNo=1&numOfRows=100&returnType=xml&serviceKey=oWT24qOJcMA4Q2zt9d7iA2vpKXjFCsqZ6fiNJQRBYrp9NOq4yu8rhRkAhIKEwxbeeSVy%2FCK0dAZQi%2BchzGjwJA%3D%3D&ver=1.0'
response=requests.get(url_station).text.encode('utf-8')
xmlobj_station=bs4.BeautifulSoup(response, 'lxml-xml')

# 2-2. 특정 측정소 데이터
rows_station=xmlobj_station.find_all('item')

rowList_station=[]
nameList_station=[]
columnList_station=[]

rowsLen_station=len(rows_station)
for i in range(0,rowsLen_station):
    columns_station=rows_station[i].find_all()

    columnsLen_station=len(columns_station)
    for j in range(0, columnsLen_station):
        if i==0:
            nameList_station.append(columns_station[j].name)
        eachColumn_station=columns_station[j].text
        columnList_station.append(eachColumn_station)
    rowList_station.append(columnList_station)
    columnList_station=[]


df_station=pd.DataFrame(rowList_station, columns=nameList_station)
# print(df_station) # -> 데이터 확인


fig_khai=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['khaiValue'])) 
fig_so2=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['so2Value']))
fig_co=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['coValue']))
fig_pm10=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['pm10Value']))
fig_pm25=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['pm25Value']))
fig_no2=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['no2Value']))
fig_o3=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['o3Value']))



# 5. dash를 이용한 웹사이트 구축
app=dash.Dash(__name__, title="Air Quality", external_stylesheets=[dbc.themes.COSMO])
server=app.server

app.layout=html.Div([
    html.Div([
        dbc.Button([html.H1('서울시 대기오염물질 현황')],style={"width":"100%"} ), # 화면에 100% 비율을 차지하게 해줌
        html.A(html.P('by AEM LAB'),className='text-end') # 오른쪽 정렬
    ]),
    html.Div([
        html.Div([
            dbc.Button([html.H4('측정소별 농도 현황')],className="border"),
            dcc.Dropdown(id='stationName', # Dropdown이라는 기능을 사용하여 측정소를 선택할 수 있게함 # 아직 반영이 안되었음
            multi=False,
            searchable=True,
            value='홍릉로',
            placeholder='Select 측정소',
            options=[{'label':c, 'value': c} for c in (df_sido.loc[:,'stationName'])],className='dropdown',)
        ],className='creat_container six'),
    ], id='third-container'),

 dbc.Container([ # 그래프가 한 행에 3개씩 표시되게 함
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='figpm10')]),
        dbc.Col([dcc.Graph(id='figpm25')])
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='figkhai')]),
        dbc.Col([dcc.Graph(id='figso2')]),
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='figno2')]),
        dbc.Col([dcc.Graph(id='figo3')])
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='figco')])
        ]),

        html.Br(),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='currentpm10')]),
        dbc.Col([dcc.Graph(id='currentpm25')])
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='currentkhai')]),
        dbc.Col([dcc.Graph(id='currentso2')]),
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='currentno2')]),
        dbc.Col([dcc.Graph(id='currento3')])
        ]),
        html.Br(),
        dbc.Row([
        dbc.Col([dcc.Graph(id='currentco')])
        ])

    ])
])


@app.callback(
    Output('figkhai','figure'),
    Output('figno2','figure'),
    Output('figso2','figure'),
    Output('figco','figure'),
    Output('figo3','figure'),
    Output('figpm10','figure'),
    Output('figpm25','figure'),

    Output('currentkhai','figure'),
    Output('currentno2','figure'),
    Output('currentso2','figure'),
    Output('currentco','figure'),
    Output('currento3','figure'),
    Output('currentpm10','figure'),
    Output('currentpm25','figure'),

    Input('stationName','value')
    )



# 3. 측정소별 dataframe 만들기
def update_station(stationName):
    url_station = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?stationName='+stationName+'&dataTerm=month&pageNo=1&numOfRows=500&returnType=xml&serviceKey=oWT24qOJcMA4Q2zt9d7iA2vpKXjFCsqZ6fiNJQRBYrp9NOq4yu8rhRkAhIKEwxbeeSVy%2FCK0dAZQi%2BchzGjwJA%3D%3D&ver=1.0'
    response=requests.get(url_station).text.encode('utf-8')
    xmlobj_station=bs4.BeautifulSoup(response, 'lxml-xml')

    rows_station=xmlobj_station.find_all('item')

    rowList_station=[]
    nameList_station=[]
    columnList_station=[]

    rowsLen_station=len(rows_station)
    for i in range(0,rowsLen_station):
        columns_station=rows_station[i].find_all()

        columnsLen_station=len(columns_station)
        for j in range(0, columnsLen_station):
            if i==0:
                nameList_station.append(columns_station[j].name)
            eachColumn_station=columns_station[j].text
            columnList_station.append(eachColumn_station)
        rowList_station.append(columnList_station)
        columnList_station=[]


    df_station=pd.DataFrame(rowList_station, columns=nameList_station)


    fig_khai=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['khaiValue']))
    fig_so2=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['so2Value']))
    fig_no2=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['no2Value']))
    fig_co=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['coValue']))
    fig_o3=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['o3Value']))
    fig_pm10=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['pm10Value']))
    fig_pm25=go.Figure(go.Scatter(x=df_station['dataTime'],y=df_station['pm25Value']))

    current_khai=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,18]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "no2Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,0.5]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,0.03],'color':'#0000FF'}, # 좋음
            {'range':[0.03,0.06],'color':'#00FF00'}, # 보통
            {'range':[0.06,0.2],'color':'#FFFF00'}, # 나쁨
            {'range':[0.2,0.5],'color':'#FF0000'}]})) # 매우나쁨

    current_so2=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,3]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "so2Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,0.3]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,0.02],'color':'#0000FF'}, # 좋음
            {'range':[0.02,0.05],'color':'#00FF00'}, # 보통
            {'range':[0.05,0.15],'color':'#FFFF00'}, # 나쁨
            {'range':[0.15,0.3],'color':'#FF0000'}]})) # 매우나쁨

    current_no2=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,18]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "no2Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,0.5]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,0.03],'color':'#0000FF'}, # 좋음
            {'range':[0.03,0.06],'color':'#00FF00'}, # 보통
            {'range':[0.06,0.2],'color':'#FFFF00'}, # 나쁨
            {'range':[0.2,0.5],'color':'#FF0000'}]})) # 매우나쁨

    current_co=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,4]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "coValue", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,30]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,2],'color':'#0000FF'}, # 좋음
            {'range':[2,9],'color':'#00FF00'}, # 보통
            {'range':[9,15],'color':'#FFFF00'}, # 나쁨
            {'range':[15,30],'color':'#FF0000'}]})) # 매우나쁨

    current_o3=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,20]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "o3Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,0.3]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,0.03],'color':'#0000FF'}, # 좋음
            {'range':[0.03,0.09],'color':'#00FF00'}, # 보통
            {'range':[0.09,0.15],'color':'#FFFF00'}, # 나쁨
            {'range':[0.15,0.3],'color':'#FF0000'}]})) # 매우나쁨

    current_pm10=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,7]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "pm10Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,300]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,30],'color':'#0000FF'}, # 좋음
            {'range':[30,80],'color':'#00FF00'}, # 보통
            {'range':[80,150],'color':'#FFFF00'}, # 나쁨
            {'range':[150,300],'color':'#FF0000'}]})) # 매우나쁨
            
    current_pm25=go.Figure(go.Indicator( # graph object의 indicator plot 사용
    mode = "gauge+number",
    value = float(df_station.iat[0,10]), # iat -> result의 1행 3열을 값으로 추출 # 현재 khai value
    title = {'text': "pm25Value", 'font': {'size': 20}}, # 제목 지정
    gauge = {
        'axis':{'range':[0,150]}, # 범위 지정
        'bar':{'color':'black'}, # 바 색깔
        'steps':[ # 범위별로 색깔지정
            {'range':[0,15],'color':'#0000FF'}, # 좋음
            {'range':[15,35],'color':'#00FF00'}, # 보통
            {'range':[35,75],'color':'#FFFF00'}, # 나쁨
            {'range':[75,150],'color':'#FF0000'}]})) # 매우나쁨


    return fig_khai, fig_so2, fig_no2, fig_co, fig_o3, fig_pm10, fig_pm25, current_khai, current_so2, current_no2, current_co, current_o3, current_pm10, current_pm25 

if __name__ == '__main__':
    app.run_server(debug=True)