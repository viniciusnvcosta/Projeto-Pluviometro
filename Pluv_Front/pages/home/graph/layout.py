from dash import html,dcc


def render_graph():

    return html.Div([
                dcc.Interval(id='interval-component',interval=1 * 1000, n_intervals=0),
                html.Div(id='time-component',style={'font-size':'30px','font-family':'Roboto Slab','font-weight':'500','text-align':'center'}),
                html.Div(id='fig_graph',style={'height':'1000px'})
        ])
