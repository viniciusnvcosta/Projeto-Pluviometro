from dash import html,dcc,dash_table
import dash_bootstrap_components as dbc
from plotly.colors import DEFAULT_PLOTLY_COLORS

def input(title,id,placeholder,min=1,max=100,step=1,lg=6):
    return (
        dbc.Col(
            html.Div([
                html.P(title),
                dbc.Input(
                    id=id, 
                    type="number", 
                    placeholder=placeholder,
                    min=min, 
                    max=max, 
                    step=step,
                )
            ]),lg=lg,className="mt-3"
        )
    )


def dropdown(dropdown_options,title,id,multi=False,lg=6,value=None,className=None):
    return dbc.Col(
        html.Div([
            html.P(title),
            dcc.Dropdown(
                options=dropdown_options,
                value=value,
                multi=multi,
                id=id,
                className=className
            ),
        ]),lg=lg,className="mt-3"
    )

def slider(id,marks,step,lg=6,value=None):
    return dbc.Col(
        html.Div([
            dcc.RangeSlider(
                marks=marks,
                step=step,
                value=value,
                id=id,
                tooltip={"placement": "bottom", "always_visible": True},
                className='px-0'
            )
        ]),lg=lg,className="mt-3 small"
    )

def checklist(dropdown_options,title,id,inline=False,lg=12):
    return dbc.Col(
        html.Div([
            html.P(title),
            dbc.Checklist(
                options=dropdown_options,
                id=id,
                inline=inline,
            ),
        ],
    ),lg=lg,className="mx-auto mt-3 d-lg-block d-lg-flex justify-content-lg-center"
)


def button(title,id,outline=True,color="primary",lg=0,classname="me-lg-4"):
    return dbc.Button(
                children=title, 
                id=id, 
                outline=outline, 
                color=color, 
                className=classname)



def graph(fig):
    fig.update_layout(
        height=600,
        margin=dict(
            pad=25,
            l=25,
            r=25,
            b=50,
            t=25,
        ),
    )
    return dbc.Card([
            dcc.Graph(
                    figure=fig
            )
        ],className="m-lg-5 p-lg-5 mt-5 p-2",style={"box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)"})


def scatter(fig,df,col,row,idx,showlegend=False):
    color = DEFAULT_PLOTLY_COLORS[idx]

    return fig.add_scatter(
        x=df.index,
        y=df[col],
        legendgroup=col,
        name=col,
        mode='lines',
        row=row,
        showlegend=showlegend,
        col=1,
        line=dict(color=color)
    )


def table(title,df=None,page_size=20,sort_action=True):
    style_header = {
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white',
        'font-size':'16px',
        'text-align': 'center',
        'font-family':'Roboto',
        'margin':'5px'
    }

    style_data = {
        'color': 'gray',
        'backgroundColor': 'white',
        'font-size':'16px',
        'text-align': 'center',
        'font-family':'Roboto',
    }

    style_table = {
        "overflowX": "scroll",
        "::-webkit-scrollbar-thumb": "#119dff" 
    }

    style_data_conditional = [                
        {
            "if": {"state": "selected"},
            "backgroundColor": "rgba(0, 116, 217, 0.15)",
            "color": "black",
            "border": "rgba(0, 116, 217, 0.3)",
        },
    ]
    
    return(
        dbc.Card([
            html.Div([
                html.H5(title),
                html.Hr(),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[dict(id=col,name=col) for col in df.columns],
                    sort_action='native' if sort_action else 'none',
                    style_header=style_header,
                    style_data=style_data,
                    id='table',
                    page_size=page_size,
                    style_table=style_table,
                    style_data_conditional=style_data_conditional
                )
            ],className="p-lg-5 p-3")
        ],className="m-lg-5 mt-5")
) 
