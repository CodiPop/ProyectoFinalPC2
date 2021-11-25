import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#25274D',
    'text': '#FFFFFF'
}


server = app.server


app.layout = html.Div(style={'backgroundColor': colors['background'], 'margin-left': '50px', 'margin-right': '50px', 'margin-bottom': '30px', 'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px'}, children=[
    html.H1(
        children='Rendimiento de Cultivos',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Grafica 1: Toneladas de aguacate cosechadas por año.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([dcc.Graph(id="grafica1")],
        style={
            'backgroundColor': colors['background'], 'margin-left': '70px', 'margin-right': '70px'
        }
    ),

    html.Div(children='Grafica 2: Produccion: Area sembrada vs. Area cosechada.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([dcc.Graph(id="grafica2")],
        style={
            'backgroundColor': colors['background'], 'margin-left': '70px', 'margin-right': '70px'
        }
    ),

    html.Div(children='Grafica 3: Tipos de cultivos sembrados.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([dcc.Graph(id="grafica3")],
        style={
            'backgroundColor': colors['background'], 'margin-left': '70px', 'margin-right': '70px', 'margin-bottom': '30px'
        }
    ),

])


@app.callback(
    dash.dependencies.Output("grafica1", "figure"),
    dash.dependencies.Input("grafica1", "id"),
)
def grafica_1(id):
    df = df_og.copy()
    df = df[df["CULTIVO"] == "AGUACATE"]
    df = df[["Producción(t)","Área Cosechada(ha)","AÑO"]]
    df = df.groupby("AÑO").sum().reset_index()
    fig2 = go.Figure(
    data=[
        go.Bar(name='Toneladas aguacate', x=df["AÑO"], y=df["Producción(t)"], yaxis='y', offsetgroup=1),
        go.Scatter(name="Toneladas aguacate pero en rojo",x=df["AÑO"],y=df["Producción(t)"])
    ],
    layout={
    	'xaxis': {'title': 'Años'},
    	'yaxis': {'title': 'Producción (t)'},
    	}
    )
    
    # Change the bar mode
    fig2.update_layout(barmode='group')
    return fig2


@app.callback(
    dash.dependencies.Output("grafica2", "figure"),
    dash.dependencies.Input("grafica2", "id"),
)
def grafica_2(id):
    df = df_og.copy()
    df = df[["DEPARTAMENTO","Área Sembrada(ha)","Área Cosechada(ha)"]]
    df = df.groupby("DEPARTAMENTO").sum().reset_index()
    df = df.sort_values(by='Área Cosechada(ha)', ascending=True)
    df = df.melt(id_vars=["DEPARTAMENTO"])
    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].str.capitalize()
    fig = px.bar(df,y="DEPARTAMENTO",x="value",color="variable", barmode='group',labels={
    	"DEPARTAMENTO": "Departamento",
    	"value": "Producción",
    	"variable": "Área"
    })
    return fig


@app.callback(
    dash.dependencies.Output("grafica3", "figure"),
    dash.dependencies.Input("grafica3", "id"),
)
def grafica_3(id):
	df = df_og.copy()
	df = df[["CULTIVO","Producción(t)"]]
	df = df.groupby("CULTIVO").sum().reset_index()
	df = df.sort_values(by='Producción(t)', ascending=False)
	df = df.reset_index().drop(labels=["index"],axis=1)
	grupo1 = df.loc[0:12,]
	suma = df.loc[13:,]["Producción(t)"].sum()
	grupo1 = grupo1.append({"CULTIVO":"OTROS","Producción(t)": suma},ignore_index=True)
	df = grupo1
	fig3 = px.pie(df,values=df["Producción(t)"],names=df["CULTIVO"])
	return fig3


if __name__ == "__main__":
    conexion = psycopg2.connect("dbname=postgres host=db user=postgres password=example")
    df_og = pd.read_sql_query("SELECT * FROM data;",conexion)
    df_og.columns = [col.replace("\n", " ").strip() for col in df_og.columns]
    app.run_server(host="0.0.0.0", debug=False, port=8055)

