from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import numpy as np
from transform import transform
from datetime import datetime


load_figure_template("slate")
style_template = 'slate'

##################################################################################################################################
# Data Management
df = transform()

##################################################################################################################################
# Server

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

##################################################################################################################################
# Plots

def Expenses_pie_chart(df):
    dff = df[df['Type'] == 'Expenses']
    fig = px.pie(dff, values='Amount', names='Category', hole = 0.3, template = style_template)
    fig.update_layout(
        title=dict(text = 'Expenses Breakdown', font = dict(size = 20))
    )
    return fig

def Income_pie_chart(df):
    dff = df[df['Type'] == 'Income']
    fig = px.pie(dff, values='Amount', names='Category', hole = 0.3, template = style_template)
    fig.update_layout(
        title=dict(text = 'Income Breakdown', font = dict(size = 20))
    )
    return fig

def Savings_pie_chart(df):
    dff = df[df['Type'] == 'Savings']
    fig = px.pie(dff, values='Amount', names='Category', hole = 0.3, template = style_template)
    fig.update_layout(
        title=dict(text = 'Savings Breakdown', font = dict(size = 20))
    )
    return fig

# Time series plot

def time_series_plot(df):

    dff = df.groupby(['Start of Month', 'Type'])['Amount'].sum().reset_index()
    fig = px.bar(dff, x='Start of Month', y='Amount', color='Type', 
                 barmode= 'group',
                 template = style_template)
    
    fig.update_layout(xaxis_title='Date')
    fig.update_layout(
        title=dict(text = 'Breakdown of Income, Expenses and Savings over time', font = dict(size = 20))
    )

    return fig

def generate_table(df, type):
    dff = df[df['Type'] == type]
    dff = dff.groupby(['Category'])['Amount'].sum().reset_index()
    dff = dff.sort_values('Amount', ascending=False)
    dff.loc["Total"] = dff.sum()
    dff.loc[dff.index[-1], 'Category'] = 'Total'
    dff['Amount'] = dff['Amount'].apply(lambda x: f"{x:,.2f}")
    return dff

def generate_table_detailed(df, type):
    dff = df[df['Type'] == type]
    dff = dff.groupby(['Category', 'Details'])['Amount'].sum().reset_index()
    dff = dff.sort_values('Amount', ascending=False)
    dff.loc["Total"] = dff.sum()
    dff['Amount'] = dff['Amount'].apply(lambda x: f"{x:,.2f}")
    dff.loc[dff.index[-1], 'Category'] = 'Total'
    return dff


def income_table(df):
    dff = generate_table(df, 'Income').round(2)
    return dff

def income_table_detailed(df):
    dff = generate_table_detailed(df, 'Income').round(2)
    return dff

def expenses_table(df):

    dff = generate_table(df, 'Expenses').round(2)

    return dff

def expenses_table_detailed(df):

    dff = generate_table_detailed(df, 'Expenses').round(2)

    return dff

def savings_table(df):

    dff = generate_table(df, 'Savings').round(2)

    return dff

def savings_table_detailed(df):

    dff = generate_table_detailed(df, 'Savings').round(2)

    return dff

##################################################################################################################################
# Layout Components

header = html.H1(
    "Expense Tracker", className="bg-primary text-white p-2 mb-2 text-left"
)

dropdown_year = dcc.Dropdown(
    options = df['Year'].unique(), value = 2023, id = "dropdown_year"
)

dropdown_month = dcc.Dropdown(
    options = df['Month Name'].unique(), value = 'March', id = "dropdown_month", multi=False
)

# Cards

Income_card = dbc.Card([
    dbc.CardHeader("Income"),
    dbc.CardBody(
        [
            html.P(
                "",
                id = "income_card",
                className="card-text")
        ]
    ),
], color="dark", outline=True)

Expenses_card = dbc.Card([
    dbc.CardHeader("Expenses"),
    dbc.CardBody(
        [
            html.P(
                "",
                id = 'expenses_card',
                className="card-text",
            ),
        ]
    ),
], color="dark", outline=True)

Savings_card = dbc.Card([
    dbc.CardHeader("Savings"),
    dbc.CardBody(
        [
            html.P(
                "",
                id = 'savings_card',
                className="card-text",
            ),
        ]
    ),
], color="dark", outline=True)

detailed_section = html.H2(
    "Detailed Breakdown", className="bg-primary text-white p-2 mb-2 text-left"
)

##################################################################################################################################
# Layout setting


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            header
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dropdown_year
        ], width=2),
        dbc.Col([
            dropdown_month
        ], width=2),
        dbc.Col([
            html.Button('Refresh', id='refresh_button', n_clicks=0, className="btn btn-primary")
        ], width=2)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            Income_card
        ], width=4),
        dbc.Col([
            Expenses_card
        ], width=4),
        dbc.Col([
            Savings_card
        ], width=4)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='income_chart', figure=Income_pie_chart(df))
        ], width=4),
                dbc.Col([
            dcc.Graph(id='expenses_chart', figure=Expenses_pie_chart(df))
        ], width=4),
                dbc.Col([
            dcc.Graph(id='savings_chart', figure=Savings_pie_chart(df))
        ], width=4)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='timeseries_chart', figure=time_series_plot(df))
        ], width=12)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            detailed_section
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
           html.H3("Income Breakdown", className="ms-1")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Table.from_dataframe(income_table(df), id = "income_table",striped=True, bordered=True, hover=True)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
           html.H3("Expense Breakdown", className="ms-1")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Table.from_dataframe(expenses_table(df), id = "expenses_table", striped=True, bordered=True, hover=True)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
           html.H3("Savings Breakdown", className="ms-1")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Table.from_dataframe(savings_table(df), id = "savings_table", striped=True, bordered=True, hover=True)
        ], width=12)
    ])
], fluid=True,id="container")



##################################################################################################################################
# Callbacks

# Graphs

@callback(
    Output('income_chart', 'figure'),
    Output('expenses_chart', 'figure'),
    Output('savings_chart', 'figure'),
    Output('income_card', 'children'),
    Output('expenses_card', 'children'),
    Output('savings_card', 'children'),
    Output('income_table', 'children'),
    Output('expenses_table', 'children'),
    Output('savings_table', 'children'),
    Input('dropdown_year', 'value'),
    Input('dropdown_month', 'value')
)

def update_slicer(year, month):

    df = transform()

    dff = df[(df['Year'] == year) & (df['Month Name'] ==month)]

# Cards
    Income = dff[dff['Type'] == 'Income']['Amount'].sum()
    Expenses = dff[dff['Type'] == 'Expenses']['Amount'].sum()
    Savings = dff[dff['Type'] == 'Savings']['Amount'].sum()

    Income_textout, Expenses_textout, Savings_textout = f"Your income for {month} is {Income:,.2f}", f"Your expenses for {month} is {Expenses:,.2f}", f"Your savings for {month} is {Savings:,.2f}"

    return Income_pie_chart(dff), Expenses_pie_chart(dff), Savings_pie_chart(dff), Income_textout, Expenses_textout, Savings_textout, dbc.Table.from_dataframe(income_table(dff), striped=True, bordered=True, hover=True), dbc.Table.from_dataframe(expenses_table(dff), striped=True, bordered=True, hover=True), dbc.Table.from_dataframe(savings_table(dff), striped=True, bordered=True, hover=True)






if __name__ == "__main__":
    app.run_server(debug=True)
