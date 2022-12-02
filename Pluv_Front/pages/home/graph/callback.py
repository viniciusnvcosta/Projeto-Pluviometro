from dash import Input, Output,State
import firebase_admin
from firebase_admin import firestore,db
from plotly.subplots import make_subplots
import pandas as pd
import collections
from datetime import datetime as dt
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

import utils.components as components


pio.templates.default = "plotly_white"



cred = firebase_admin.credentials.Certificate('projeto-pluviometro-58413fbabcd4.json')
firebase_admin.initialize_app(cred,{'databaseURL':'https://projeto-pluviometro-default-rtdb.firebaseio.com'})



def init_graph_callback(app):
    @app.callback(
        Output(component_id="fig_graph", component_property="children"),
        Output(component_id="dados_firebase", component_property="data"),
        Input(component_id="interval-component", component_property="n_intervals"),
        State(component_id="dados_firebase", component_property="data"),
        prevent_initiall_call=True,suppress_callback_exceptions=True)
    def graph(n_intervals,dados_firebase):
        
        buffer_firebase = dados_firebase if dados_firebase else []

        buffer = collections.deque(buffer_firebase,maxlen=60)
        
        resp = db.reference('/').get()
        resp['DATA'] = dt.now()

        hora = resp['DATA'].strftime('%Y-%m-%d %H:%M:%S')
        
        buffer += [resp]


        fig = go.Figure()      
        df = pd.DataFrame(buffer)
        fig.add_scatter(y=df['PRECIP'],x=df['DATA'],fill='tozeroy')
        
        fig.add_hrect(y0=160, y1=200, line_width=0, fillcolor="red", opacity=0.05)
        fig.add_hline(y=160, line_width=1, line_dash="dash", fillcolor="red",line_color="red", opacity=0.5)

        fig.update_layout(
            title="Nível da chuva",
            yaxis_range=[0,200],
            legend=dict(
                yanchor="top",
                xanchor="left",
                y=0.99,
                x=0.01
            ),
        )

        graph = components.graph(fig)

        return [graph,list(buffer)]



    

