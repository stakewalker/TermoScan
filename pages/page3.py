from dash import Dash, dcc, html, Input, Output, State, callback
from pages import relatorio

# Gerar relatório no formato de lista/planilha,
# permitindo que o usuário escolha data de início e fim

layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Gerar Relatório', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Digite o nome do arquivo')
])

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)

def update_output(n_clicks, value):
    return relatorio.gerar_relatorio(
        "relatorio_temperaturas.pdf",
        relatorio.imagens,
        relatorio.descricoes
)