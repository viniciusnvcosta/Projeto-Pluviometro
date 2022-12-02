from dash import html,dcc,register_page
from .home import layout_home,init_callbacks_home


def init_pages(app):
    register_page("home",  path='/',layout=layout_home)   
    
    init_callbacks_home(app)

    