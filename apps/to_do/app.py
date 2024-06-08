# app.py
from dash import dcc, html
import plotly.express as px
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

df = px.data.iris()
x=[0,1,2,3,4,5,6,7,8,9,10]
y=[-5,-8,1,2,3,4,10,-5,6,9,9]
#fig = px.line(df, x='sepal_width', y='sepal_length')
fig = px.scatter(df, x='sepal_width', y='sepal_length')

# Ajustar o layout da figura
fig.update_layout(
    autosize=True,
    #width=800,  # Largura em pixels
    #height=600,  # Altura em pixels
    margin=dict(l=20, r=20, b=20, t=20)
)

app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=fig,
        style={'width': '50vw', 'height': '50vh'}  # Ajustar o gráfico ao contêiner
    )
], style={'width': '50vw', 'height': '50vh', 'overflow': 'hidden'})  # Ajustar o contêiner


