# app.py
from dash import dcc, html
import plotly.express as px
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length')

# Ajustar o layout da figura
fig.update_layout(
    autosize=False,
    width=800,  # Largura em pixels
    height=600,  # Altura em pixels
    margin=dict(l=50, r=50, b=100, t=100, pad=4)
)

app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=fig,
        style={'width': '100%', 'height': '100%'}  # Ajustar o gráfico ao contêiner
    )
], style={'width': '80vw', 'height': '80vh', 'margin': 'auto'})  # Ajustar o contêiner
