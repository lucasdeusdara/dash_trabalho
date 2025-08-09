import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Dados básicos de vendas por cidade e mês
dados = pd.DataFrame({
    "Cidade": ["São Paulo", "Rio", "Fortaleza", "São Paulo", "Rio", "Fortaleza"],
    "Mês": ["Jan", "Jan", "Jan", "Fev", "Fev", "Fev"],
    "Vendas": [100, 80, 70, 120, 90, 160]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Interativo de Vendas", style={"textAlign": "center"}),

    html.Label("Escolha a cidade:"),
    dcc.Dropdown(
        id="cidade-dropdown",
        options=[{"label": c, "value": c} for c in dados["Cidade"].unique()],
        value="São Paulo"
    ),

    html.Br(),

    html.Div([
        html.Div([dcc.Graph(id="graf1")], style={"width": "48%", "display": "inline-block"}),
        html.Div([dcc.Graph(id="graf2")], style={"width": "48%", "display": "inline-block"}),
    ]),

    html.Div([
        dcc.Graph(id="graf3")
    ], style={"width": "50%", "margin": "auto"})
])

@app.callback(
    Output("graf1", "figure"),
    Output("graf2", "figure"),
    Output("graf3", "figure"),
    Input("cidade-dropdown", "value")
)
def atualizar_graficos(cidade):
    df_filtrado = dados[dados["Cidade"] == cidade]

    # gráfico de barras com vendas por mês
    graf1 = px.bar(df_filtrado, x="Mês", y="Vendas", color="Mês",
                   title=f"Vendas em {cidade}",
                   text="Vendas")
    graf1.update_traces(textposition='outside')

    # gráfico de linha mostrando evolução das vendas
    graf2 = px.line(df_filtrado, x="Mês", y="Vendas", markers=True,
                   title=f"Evolução das vendas - {cidade}")

    # gráfico de pizza mostrando participação das cidades nas vendas totais
    total_vendas = dados.groupby("Cidade")["Vendas"].sum().reset_index()
    graf3 = px.pie(total_vendas, names="Cidade", values="Vendas",
                  title="Participação nas vendas totais", hole=0.3)
    graf3.update_traces(textinfo='percent+label')

    return graf1, graf2, graf3
    
server = app.server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)

