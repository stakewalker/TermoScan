from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from server import termoscan
import json
import os

temas = ["BOOTSTRAP", "CERULEAN", "COSMO", "CYBORG", "DARKLY", "FLATLY",
         "JOURNAL", "LITERA", "LUMEN", "LUX", "MATERIA", "MINTY", "MORPH", "PULSE",
         "QUARTZ", "SANDSTONE", "SIMPLEX", "SKETCHY", "SLATE", "SOLAR", "SPACELAB",
         "SUPERHERO", "UNITED", "VAPOR", "YETI", "ZEPHYR"
         ]

# Carregar configurações existentes ou criar um dicionário vazio
configs_file = 'assets/configs.json'
if os.path.exists(configs_file):
    with open(configs_file, 'r') as file:
        configs = json.load(file)
else:
    configs = {}

layout = dbc.Container([
    html.H3("Configurações", className="header"),

    # Configurar CLP
    dbc.Row([
        dbc.Card([
            dbc.CardHeader(html.H5("Detalhes da Empresa")),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Label("Nome da Empresa", className="form-label"),
                        dbc.Input(id='nome-empresa', type='text', value=configs.get('nome_empresa', ''), className="form-control"),
                    ])
                ], className="mb-3")
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Label("Responsável Técnico", className="form-label"),
                        dbc.Input(id='nome-resp', type='text', value=configs.get('nome_resp', ''), className="form-control"),
                    ])
                ], className="mb-3")
            ),
            dcc.Upload(  # Alterar logo da empresa
                id='upload-logo',
                children=html.Button('Alterar Logo', className='button button-primary'),
                multiple=False
            ),
        ], className="mb-3"),
    ]),

    # Configurar Tema do Sistema
    dbc.Card([
        dbc.CardHeader(html.H3("Cores do Sistema")),
        dbc.CardBody([
            dcc.Dropdown(
                id='temas-dropdown',
                options=[{'label': tema.title(), 'value': tema.lower()} for tema in temas],
                value=configs.get('tema', ''),
                persistence=True
            )
        ])
    ], className="mb-3"),

    # Botão "Salvar"
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Button('Salvar Alterações', id='save-button'), width=12)
            ])
        ])
    ]),

    # Exibir Mensagens
    html.Div(id='output-message', className='mt-3')],
    className="mt-5"
)

# Callback do Botão Salvar
@callback(
    [Output('output-message', 'value')],
    [Input('save-button', 'n_clicks')],
    [
        State('nome-empresa', 'value'),
        State('nome-resp', 'value'),
        State('temas-dropdown', 'value'),
        State('upload-logo', 'contents')
    ]
)
def save_changes(n_clicks, nome_empresa, nome_resp, tema, upload_logo_contents):
    if n_clicks is None or n_clicks == 0:
        return [None]

    # Salvar as configurações em configs.json
    configs['nome_empresa'] = nome_empresa
    configs['nome_resp'] = nome_resp
    configs['tema'] = tema.upper()

    with open(configs_file, 'w') as file:
        json.dump(configs, file, indent=2)

    # Atualizar o external_stylesheets no layout
    termoscan.external_stylesheets = [getattr(dbc.themes,configs['tema'], dbc.themes.BOOTSTRAP)]
    
    return [dbc.Alert('Suas alterações foram salvas!', color='success')]
