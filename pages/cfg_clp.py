from dash import html, dcc, Input, Output, State, Dash, callback
import dash_bootstrap_components as dbc
import json


def carregar_clps():
    try:
        with open('assets/clps.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salvar_clps(clps):
    with open('assets/clps.json', 'w') as file:
        json.dump(clps, file)

clps = carregar_clps()

# Gerar layout com dropdowns e campos de edição
layout = dbc.Container([
    html.H3("Definições de CLP", className="header"),

    # Dropdowns e campos de edição para cada clp
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-clps',
                options=[{'label': clp['modelo'], 'value': key} for key, clp in clps.items()] + [{'label': 'Adicionar Novo CLP', 'value': 'Novo CLP'}],
                placeholder="Escolha o CLP",
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Label("Modelo do CLP:"), html.Br(),
                    dcc.Input(id='input-clp-modelo', type='text', size="40"),
                    html.Label("Versão do Firmware do CLP:"), html.Br(),
                    dcc.Input(id='input-clp-firmware', type='text', size="40"),
                    html.Label("Endereço IP:"), html.Br(),
                    dcc.Input(id='input-clp-ip', type='text', size="40"),
                    html.Label("Online?"), html.Br(),
                    dcc.Input(id='input-clp-status', type='text', size="40"),
                    html.Label("Sensores Disponíveis:"), html.Br(),
                    dcc.Dropdown(id='dropdown-clp-sensores', options=[], multi=True),
                    html.Br(),
                    dbc.Button("Salvar Alterações", id='save-button', style={'margin-right': '50px'}),
                    dbc.Button("Adicionar", color="success", id='add-button'),
                    dbc.Button("Remover", color="danger", id='remove-button'),
                    html.Div(id='output-clp-message', className='mt-3')
                ])
            ),
            width=6
        )
    ], className="mb-3")
])

# Callback para atualizar campos de edição quando clp é selecionada
@callback(
    [Output('input-clp-modelo', 'value'),
     Output('input-clp-ip', 'value'),
     Output('input-clp-firmware', 'value'),
     Output('input-clp-status', 'value'),
     Output('dropdown-clp-sensores', 'options')],
    [Input('dropdown-clps', 'value')],
    prevent_initial_call=True
)
def atualizar_campos_edicao(selected_clp_modelo):
    if selected_clp_modelo and selected_clp_modelo != 'Novo CLP':
        selected_clp = clps.get(selected_clp_modelo, {})
        clp_info = selected_clp
        sensor_options = [{'label': sensor, 'value': sensor} for sensor in selected_clp.get('sensores', [])]
        return clp_info.get('modelo', ''), clp_info.get('ip', ''), clp_info.get('versao_firmware', ''), clp_info.get('online', ''), sensor_options
    else:
        return '', '', '', '', []


# Callback para salvar as mudanças quando clicar no botão
@callback(
    [Output('output-clp-message', 'children'),
     Output('dropdown-clps', 'options')],
    [Input('save-button', 'n_clicks'),
     Input('add-button', 'n_clicks'),
     Input('remove-button', 'n_clicks')],
    [State('dropdown-clps', 'value'),
     State('input-clp-modelo', 'value'),
     State('input-clp-ip', 'value'),
     State('input-clp-firmware', 'value'),
     State('input-clp-status', 'value')],
    prevent_initial_call=True
)
def salvar_alteracoes(save_clicks, add_clicks, remove_clicks, selected_clp_modelo, modelo_clp, ip_clp, firmware_clp, status_clp):
    if save_clicks:
        if selected_clp_modelo and selected_clp_modelo != 'Novo CLP':
            selected_clp = clps.get(selected_clp_modelo, {})
            selected_clp['modelo'] = modelo_clp
            selected_clp['ip'] = ip_clp
            selected_clp['versao_firmware'] = firmware_clp
            selected_clp['online'] = status_clp
            salvar_clps(clps)
            return "Alterações salvas com sucesso!", [{'label': key, 'value': key} for key in clps.keys()] + [{'label': 'Adicionar Novo CLP', 'value': 'Novo CLP'}]
        else:
            return "", []

    elif add_clicks:
        if modelo_clp and ip_clp and firmware_clp and status_clp:
            new_clp_key = f"clp_{len(clps) + 1}"
            new_clp = {
                'modelo': modelo_clp,
                'ip': ip_clp,
                'versao_firmware': firmware_clp,
                'online': status_clp,
                'sensores': []
            }
            clps[new_clp_key] = new_clp
            salvar_clps(clps)
            return "Novo CLP adicionado com sucesso!", [{'label': key, 'value': key} for key in clps.keys()] + [{'label': 'Adicionar Novo CLP', 'value': 'Novo CLP'}]
        else:
            return "Preencha todos os campos para adicionar um novo CLP.", []

    elif remove_clicks:
        if selected_clp_modelo and selected_clp_modelo != 'Novo CLP':
            clps.pop(selected_clp_modelo, None)
            salvar_clps(clps)
            return "CLP removido com sucesso!", [{'label': key, 'value': key} for key in clps.keys()] + [{'label': 'Adicionar Novo CLP', 'value': 'Novo CLP'}]
        else:
            return "Selecione um CLP para remover.", []

    raise PreventUpdate


