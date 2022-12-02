from dash import html,register_page,dcc

from ..template.header import render_header
from .graph.layout import render_graph
from .graph.callback import init_graph_callback


def init_callbacks_home(app):
    init_graph_callback(app)
    

layout_home = html.Div([
        dcc.Store(id='dados_firebase'),
        render_header(),
        render_graph(),
    ],className="bg-light")


