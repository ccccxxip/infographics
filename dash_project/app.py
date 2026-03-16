from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# данные
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

# доступные метрики
metrics = ["pop", "lifeExp", "gdpPercap"]
years = sorted(df["year"].unique())

app = Dash(__name__)

# интерфейс
app.layout = html.Div([

    html.H1("Gapminder Dashboard", style={"textAlign": "center"}),

    html.Label("Выберите страны"),
    dcc.Dropdown(
        options=[{"label": c, "value": c} for c in sorted(df.country.unique())],
        value=["Germany", "Canada"],
        multi=True,
        id="country-dropdown"
    ),

    html.Label("Метрика для линейного графика"),
    dcc.Dropdown(
        options=[{"label": m, "value": m} for m in metrics],
        value="pop",
        id="y-axis"
    ),

    html.Br(),

    html.Label("X axis"),
    dcc.Dropdown(
        options=[{"label": m, "value": m} for m in metrics],
        value="gdpPercap",
        id="bubble-x"
    ),

    html.Label("Y axis"),
    dcc.Dropdown(
        options=[{"label": m, "value": m} for m in metrics],
        value="lifeExp",
        id="bubble-y"
    ),

    html.Label("Bubble size"),
    dcc.Dropdown(
        options=[{"label": m, "value": m} for m in metrics],
        value="pop",
        id="bubble-size"
    ),

    html.Label("Выберите год"),
    dcc.Slider(
        min=min(years),
        max=max(years),
        step=5,
        value=max(years),
        marks={str(y): str(y) for y in years},
        id="year-slider"
    ),

    html.Hr(),

    dcc.Graph(id="line-chart"),
    dcc.Graph(id="bubble-chart"),
    dcc.Graph(id="top15-chart"),
    dcc.Graph(id="pie-chart")

])


# линейный график
@app.callback(
    Output("line-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("y-axis", "value")
)
def update_line(countries, metric):

    dff = df[df.country.isin(countries)]

    fig = px.line(
        dff,
        x="year",
        y=metric,
        color="country",
        title="Сравнение стран"
    )

    return fig


# пузырьковая диаграмма
@app.callback(
    Output("bubble-chart", "figure"),
    Input("bubble-x", "value"),
    Input("bubble-y", "value"),
    Input("bubble-size", "value"),
    Input("year-slider", "value")
)
def update_bubble(x, y, size, year):

    dff = df[df.year == year]

    fig = px.scatter(
        dff,
        x=x,
        y=y,
        size=size,
        color="continent",
        hover_name="country",
        size_max=60,
        title="Bubble chart"
    )

    return fig


# топ стран по населению
@app.callback(
    Output("top15-chart", "figure"),
    Input("year-slider", "value")
)
def update_bar(year):

    dff = df[df.year == year]

    top15 = dff.sort_values("pop", ascending=False).head(15)

    fig = px.bar(
        top15,
        x="country",
        y="pop",
        title="Топ-15 стран по населению"
    )

    return fig


# круговая диаграмма
@app.callback(
    Output("pie-chart", "figure"),
    Input("year-slider", "value")
)
def update_pie(year):

    dff = df[df.year == year]

    cont = dff.groupby("continent")["pop"].sum().reset_index()

    fig = px.pie(
        cont,
        values="pop",
        names="continent",
        title="Популяция по континентам"
    )

    return fig


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)