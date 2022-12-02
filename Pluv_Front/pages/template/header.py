from dash import html,dcc
import dash_bootstrap_components as dbc




def render_header():
    return (
        dbc.Row(
            [
                dbc.Col([

                    html.Div("CESAR SCHOOL",style={'font-size':'60px','font-family':'Roboto Slab','font-weight':'700'}),
                    html.Div("Projeto Pluviômetro",style={'font-size':'30px','font-family':'Roboto Slab','font-weight':'500'}),
                    html.Div("Embarcados - 2022.2",style={'font-size':'20px','font-family':'Roboto Slab','font-weight':'400'}),
                ],
                lg=dict(size=6,offset=3),
            )
        ],className="p-lg-5 m-lg-0 p-3 m-0",style={'height':'250px','background-color':'#fcb900','font-color':'#1b1b1b',})
    )
