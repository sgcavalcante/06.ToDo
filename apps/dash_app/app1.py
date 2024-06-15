# dash_app/app1.py

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder().query("continent=='Oceania'")
app = Dash(__name__, server=False)

app.layout = html.Div(
    [
        html.H4("Life expectancy plot with a selectable hover mode"),
        html.P("Select hovermode:"),
        dcc.RadioItems(
            id="hovermode",
            inline=True,
            options=["x", "x unified", "closest"],
            value="closest",
        ),
        dcc.Graph(id="graph"),
    ]
)

@app.callback(
    Output("graph", "figure"),
    Input("hovermode", "value"),
)
def update_hovermode(mode):
    fig = px.line(
        df,
        x="year",
        y="lifeExp",
        color="country",
        title="Hover over points to see the change",
    )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode=mode)
    return fig

dash_app = app
