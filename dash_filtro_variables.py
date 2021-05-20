# -*- coding: utf-8 -*-
"""
Created on Tue May 18 14:20:14 2021

@author: scpgo
"""

import streamlit as st

st.title("Streamlit example")

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go # or 
import plotly.express as px

from datetime import date, timedelta
import datetime

from pygraphtec import  lee_fichero_sesion

#df = lee_fichero_sesion("201112-165432.csv", path_sesiones='/Users/scpgo/.spyder-py3/dataLogger')
df = lee_fichero_sesion("201112-180010.csv", path_sesiones='/Users/scpgo/.spyder-py3/dataLogger')

app = dash.Dash()

fig_names = df.columns #asigno fig_names a las columnas del Dataframe

cols_dropdown = html.Div([ #Div del filtro de variables
    dcc.Dropdown(
        id='cols_dropdown',
        options=[{'label': x, 'value': x} for x in fig_names], #creo el filtro de variables
        value=None, #ninguna opcion inicial preseleccionada    
        multi=True #permite selección de varias opciones
    ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=df.index.min()-timedelta(days=1),
        max_date_allowed=datetime.date.today(),
        initial_visible_month=df.index.min(),
        start_date=date(2020,11,12),
        end_date=date(2020, 11, 13))])

fig_plot = html.Div(id='fig_plot') #Div de la gráfica

app.layout = html.Div([cols_dropdown, fig_plot]) #permite construir la estructura el filtro
                                                 #de variables y la gráfica

@app.callback( #permite devolver la gráfica como Dash Core Component dcc.Graph (línea 44)
dash.dependencies.Output('fig_plot', 'children'),
[dash.dependencies.Input('cols_dropdown', 'value'),
 dash.dependencies.Input('my-date-picker-range', 'start_date'),
 dash.dependencies.Input('my-date-picker-range', 'end_date')])

def name_to_figure(value,start_date,end_date):
    if value is None or len(value)==0 or start_date not in df.index:
        figure = {}
    else:
        df_date_filter = df.loc[start_date:end_date]
        figure=px.line(df_date_filter[value]) #se crea figura que representa todas las variables
                                   #fig_names corresponde a la variable global (línea 25)
    return dcc.Graph(figure=figure)

app.run_server(debug=True, use_reloader=False) #arranca la aplicacion