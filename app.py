import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import json

#from plotly.subplots import make_subplots
#import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

df2 = pd.read_csv('transferencias_entidades_fed.csv', sep=',', encoding = 'latin1')
mexico_path = 'C:/Users/Homar/Documents/Jupyter Notebooks/Mapeando/mexican_states.geojson'
with open(mexico_path) as f:
    geo_mexico = json.load(f)
    
dt_entidad = df2.groupby(['ENTIDAD']).agg({'MONTOOK': 'sum'}).reset_index()
fig7 = px.choropleth(dt_entidad, 
                     geojson=geo_mexico, 
                     locations="ENTIDAD", 
                     featureidkey="properties.admin_name",
                     color='MONTOOK',
                     color_continuous_scale="Viridis",
                     fitbounds='locations', height=400
                     )
fig7.update_layout(title_text='Por Entidad', 
                   margin={"r":0,"t":0,"l":0,"b":0})
    
dt_fecha = df2.groupby(['CICLO', 'MesN']).agg({'MONTOOK': 'sum'}).reset_index()
fig3 = px.line(dt_fecha, 
             x="MesN", 
             y="MONTOOK",
             color='CICLO', 
            # color_discrete_map='blue',
             height=400)
#fig3.update_layout(title_text='Por Mes y Año')

dt_subtema_concepto = df2.groupby(['SUBTEMA', 'CONCEPTO']).agg({'MONTOOK': 'sum'}).reset_index()
fig5 = px.sunburst(dt_subtema_concepto, path=['SUBTEMA', 'CONCEPTO'], values='MONTOOK', height=400)
#fig5.update_layout(title_text='Por Subtema y Fondo')

dt_ciclo_subtema = df2.groupby(['CICLO', 'SUBTEMA']).agg({'MONTOOK': 'sum'}).reset_index()
fig2 = px.bar(dt_ciclo_subtema, x="CICLO", y="MONTOOK",
             color='SUBTEMA', #barmode='group',
             height=400)
#fig2.update_layout(title_text='Por Año y Subtema')

#fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")
#fig.add_trace(fig7, row=1, col=1)
#fig.add_trace(fig3, row=1, col=2)
#fig.add_trace(fig5, row=2, col=1)
#fig.add_trace(fig2, row=2, col=2)
#app.layout = html.Div(children=[
#    html.H1(children='Transferencias Federales'),
#
#    html.Div(children='''
#        Tablero hecho con dash.
#    '''),
#
#    dcc.Graph(
#        id='example-graph',
#        figure=fig
#    )
#])

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.Div([
            html.H1(children='Transferencias Federales'),
            html.Div(children='''
                Por Entidad
            '''),
            dcc.Graph(
                id='graph1',
                figure=fig7
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children='por Omar Humberto González Ávila'),
            html.Div(children='''
                Por Mes y Año
            '''),
            dcc.Graph(
                id='graph2',
                figure=fig3
            ),  
        ], className='six columns'),
        ], className='row'),
    html.Div([
        html.Div([
            html.H1(children=''),
            html.Div(children='''
                Por Subtema y Fondo
            '''),
            dcc.Graph(
                id='graph3',
                figure=fig5
            ),  
        ], className='six columns'),
        html.Div([
            html.H1(children=''),
            html.Div(children='''
                Por Año y Subtema
            '''),
            dcc.Graph(
                id='graph4',
                figure=fig2
            ),  
        ], className='six columns'),
    ], className='row'),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)