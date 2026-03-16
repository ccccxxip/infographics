from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# загружаем данные
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

metrics = ["pop", "lifeExp", "gdpPercap"]
years = sorted(df["year"].unique())

app = Dash(__name__)
server = app.server

# layout
app.layout = html.Div([

    html.H1("Gapminder Dashboard", style={"textAlign": "center"}),

    # блок с контролами
    html.Div([

        html.Div([
            html.Label("Countries"),  # выбор стран
            dcc.Dropdown(
                options=[{"label": c, "value": c} for c in sorted(df.country.unique())],
                value=["Germany", "Canada"],
                multi=True,
                id="country-dropdown"
            ),

            html.Label("Line chart metric"),  # выбор метрики для линейного графика
            dcc.Dropdown(
                options=[{"label": m, "value": m} for m in metrics],
                value="pop",
                id="y-axis"
            ),
        ], style={"width": "30%", "display": "inline-block"}),

        html.Div([
            html.Label("Bubble X"),  # ось X пузырька
            dcc.Dropdown(
                options=[{"label": m, "value": m} for m in metrics],
                value="gdpPercap",
                id="bubble-x"
            ),

            html.Label("Bubble Y"),  # ось Y пузырька
            dcc.Dropdown(
                options=[{"label": m, "value": m} for m in metrics],
                value="lifeExp",
                id="bubble-y"
            ),
        ], style={"width": "30%", "display": "inline-block"}),

        html.Div([
            html.Label("Bubble size"),  # размер пузырька
            dcc.Dropdown(
                options=[{"label": m, "value": m} for m in metrics],
                value="pop",
                id="bubble-size"
            ),

            html.Label("Year"),  # выбор года
            dcc.Slider(
                min=min(years),
                max=max(years),
                step=5,
                value=max(years),
                marks={str(y): str(y) for y in years},
                id="year-slider"
            ),
        ], style={"width": "35%", "display": "inline-block"}),

    ], style={"padding": "20px"}),  # паддинги для блока контролов

    # первый ряд графиков
    html.Div([

        html.Div([
            dcc.Graph(id="line-chart", style={"height": "35vh"})  # линейный график
        ], style={"width": "50%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="bubble-chart", style={"height": "35vh"})  # пузырьковая диаграмма
        ], style={"width": "50%", "display": "inline-block"}),

    ]),

    # второй ряд графиков
    html.Div([

        html.Div([
            dcc.Graph(id="top15-chart", style={"height": "35vh"})  # топ-15 стран по популяции
        ], style={"width": "50%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="pie-chart", style={"height": "35vh"})  # круговая диаграмма по континентам
        ], style={"width": "50%", "display": "inline-block"}),

    ])

])

# коллбэк для линейного графика
@app.callback(
    Output("line-chart", "figure"),
    Input("country-dropdown", "value"),
    Input("y-axis", "value")
)
def update_line(countries, metric):
    filtered = df[df.country.isin(countries)]
    fig = px.line(filtered, x="year", y=metric, color="country")
    return fig

# коллбэк для пузырьковой диаграммы
@app.callback(
    Output("bubble-chart", "figure"),
    Input("bubble-x", "value"),
    Input("bubble-y", "value"),
    Input("bubble-size", "value"),
    Input("year-slider", "value")
)
def update_bubble(x, y, size, year):
    filtered = df[df.year == year]
    fig = px.scatter(filtered, x=x, y=y, size=size, color="continent",
                     hover_name="country", size_max=60)
    return fig

# коллбэк для топ-15 стран
@app.callback(
    Output("top15-chart", "figure"),
    Input("year-slider", "value")
)
def update_top15(year):
    filtered = df[df.year == year]
    top15 = filtered.sort_values("pop", ascending=False).head(15)
    fig = px.bar(top15, x="country", y="pop")
    return fig

# коллбэк для круговой диаграммы
@app.callback(
    Output("pie-chart", "figure"),
    Input("year-slider", "value")
)
def update_pie(year):
    filtered = df[df.year == year]
    continent_pop = filtered.groupby("continent")["pop"].sum().reset_index()
    fig = px.pie(continent_pop, values="pop", names="continent")
    return fig

# запуск приложения
# if __name__ == "__main__":
#     app.run(debug=True)