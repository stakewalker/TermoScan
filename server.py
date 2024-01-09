from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from pages import page1, page2, page3, cfg_salas, cfg_clp, cfg_geral
import json
import os
import dash_auth

# Carregar configurações ou criar um dicionário vazio
with open('assets/configs.json', 'r') as file:
    configs = json.load(file)

# Inicializar app e configurar
termoscan = Dash(__name__, 
        external_stylesheets=[getattr(dbc.themes,configs['tema'], dbc.themes.BOOTSTRAP)], 
        suppress_callback_exceptions=True
        )
termoscan.title = "TermoScan"
termoscan.head = [
    html.Link(
        rel='icon',
        href='assets/termoscan_icon.png',
        type='image/x-icon'
    )
]

# Autenticação
usuarios = {
    'programador': 'programador',
    'engenheiro': 'engenheiro'
}
auth = dash_auth.BasicAuth(
    termoscan,
    usuarios
)

navbar = dbc.Navbar([  # Barra de menus do topo
    dbc.Container(
        [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src='assets/termoscan_icon.png', height="30px")),
                    dbc.Col(dbc.NavbarBrand("TermoScan", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            href="/",
            style={"textDecoration": "none"},
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            id="navbar-collapse",
            is_open=False,
            navbar=True
        ),
        ]
    ),
    
    dbc.Container(
        dbc.Nav(
            [
                dbc.NavLink("Temperatura das Salas", href="/page-1", id="page-1-link"),
                dbc.NavLink("Visualizar Tudo", href="/page-2", id="page-2-link"),
                dbc.NavLink("Gerar Relatório", href="/page-3", id="page-3-link"),
                dbc.DropdownMenu(  # Sub-menu de configurações
                    children=[
                        dbc.DropdownMenuItem("Programação", header=True),
                        dbc.DropdownMenuItem("Add/Remover Salas", href="/cfg_salas"),
                        dbc.DropdownMenuItem("Programação de CLPs", href="/cfg_clp"),
                        dbc.DropdownMenuItem("Outros", header=True),
                        dbc.DropdownMenuItem("Definições Gerais", href="/cfg_geral"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Configurações",
                ),
                # Truque para deslogar o usuário...
                dbc.NavLink("Sair", href="http://log:out@127.0.0.1:8050", id="logout-link")
            ],
            pills=True,
            className="ml-auto", 
        )
    )],
    color="dark",
    dark=True,
    sticky="top"
)


# Área do conteúdo
content = dbc.Col(id="conteudo", 
    style={"align":"center"})

# Layout do App
termoscan.layout = html.Div([dcc.Location(id="url"), navbar, content])

# Callback principal
@termoscan.callback(
    Output("conteudo", "children"), 
    Input("url", "pathname"))

def display_page(pathname):
    if pathname == "/page-1":
        return page1.layout
    elif pathname == "/page-2":
        return page2.layout
    elif pathname == "/page-3":
        return page3.layout
    elif pathname == "/cfg_salas":
        return cfg_salas.layout
    elif pathname == "/cfg_clp":
        return cfg_clp.layout
    elif pathname == "/cfg_geral":
        return cfg_geral.layout
    else:  # Página de abertura, com imagem, logo, etc...
        return html.Div([
            dbc.Container([
                html.H1("TermoScan", className="big-title", style={
                    "color": "white",
                    "textShadow": "2px 2px 4px rgba(0, 0, 0, 0.8)",
                    "fontSize": "10rem",  
                    "marginBottom": "0", 
                }),
                html.P("by Stakewalker", style={
                    "color": "white",
                    "position": "center",
                    "fontSize": "1.5rem", 
                    "textShadow": "2px 2px 4px rgba(0, 0, 0, 0.6)"
                }),
            ], fluid=True, style={
                "height": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "backgroundImage": "url('assets/background.jpg')",
                "backgroundSize": "cover",
            }),

        ])

# Callback que indica qual página está selecionada
@termoscan.callback(
    [
        Output(f"{page}-link", "active") for page in ["page-1", "page-2", "page-3"]
    ],
    [Input("url", "pathname")]
)
def atualizar_tema(tema):
    with open('assets/configs.json', 'r') as file:
        configs = json.load(file)

    # Atualizar o external_stylesheets no layout
    termoscan.external_stylesheets = [getattr(dbc.themes,configs['tema'], dbc.themes.BOOTSTRAP)]
    # Retorna a lista de estados para os links
    return toggle_active_links(tema)


def toggle_active_links(pathname):
    return [pathname == f"/{page}" for page in ["page-1", "page-2", "page-3"]]


if __name__ == "__main__":
    termoscan.run_server(debug=True)