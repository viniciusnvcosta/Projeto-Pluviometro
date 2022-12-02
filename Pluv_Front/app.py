import dash
import dash_bootstrap_components as dbc
from pages import init_pages

def create_app():
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
        "https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@100;200;300;400;500;600;700;800;900&display=swap"
    ]
    

    app = dash.Dash(external_stylesheets=external_stylesheets, use_pages=True)
    
    
    init_pages(app)
    
    return app

if __name__=='__main__':
    app = create_app()
    app.run_server(host='localhost',debug=True)
