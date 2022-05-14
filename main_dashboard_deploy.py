#!/usr/bin/env python
# coding: utf-8

# In[1]:



from dash import dcc
# import dash_core_components as dcc 
import plotly.express as px
import pandas as pd
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
from dash import Dash, dcc, html, Input, Output, callback_context

from plotly.subplots import make_subplots
import plotly.graph_objects as go


df = pd.read_csv("bills.csv", parse_dates =["bill_start_date"])
df = df.iloc[:1400,:]
df["Year"] = df["bill_start_date"].astype("datetime64[ns]").dt.year
df["month"] = df["bill_start_date"].astype("datetime64[ns]").dt.month
df.rename(columns = ({"Location" : "Site Name"}),inplace = True)
df_kwh = df[df["bill_total_unit"] == "kwh"]
df_therms = df[df["bill_total_unit"] == "therms"]


dff = df.groupby("Site Name")["bill_total"].sum().sort_values(ascending = True ).reset_index()
c = dff.sort_values(by = "bill_total").head(10)

ddf =df.set_index(["bill_start_date"])
new_df = ddf.resample('1M', kind = "period").sum().reset_index()
df_kwh["bill_total_unit"].unique()
dff

trace1 = go.Bar(y=c["Site Name"],x=c["bill_total"],orientation = "h")

data1 = trace1

layout1 = go.Layout(title = "District Energy Expenditure", paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

fig1 = go.Figure(data = trace1, layout = layout1)
fig1.update_layout(autosize = True)

####

df_kwh = df[df["bill_total_unit"] == "kwh"]
df1 = df_kwh.iloc[:12,:]


# In[2]:


app = Dash(__name__)
app.layout = html.Div([    
                        html.Div([html.P("UTILITY DATA ANALYTICS",className ="title"),                       
                                  html.Div(dcc.Dropdown(["Past 12 months","Past 6 months","Past 3 months","Past 1 month"]
                                            ,id="period-dd", value = "Past 6 months"),style ={"width":"25%"}),
                                      html.Div([
                                            html.Div(dcc.Link("Home", id='Home', href='#',className = "li"),className="link-styles"),
                                            html.Div(dcc.Link("Location", id='Location', href='#',className = "li"),className="link-styles"),
                                            html.Div(dcc.Link("Meter", id='Meter', href='#',className = "li"),className="link-styles")],
                                            className="links-flex")
                                                       
                        ],className="container1"),
    
                        html.Div([                                 
                                html.Div([
                                html.Div((dcc.Graph(id="indicator1",config={'displayModeBar': False},style={"display":"inline"})), className="card"),
                                 html.Div((dcc.Graph(id="indicator2",config={'displayModeBar': False},style={"display":"inline"})), className="card"),
                                 html.Div((dcc.Graph(id="indicator3",config={'displayModeBar': False},style={"display":"inline"})), className="card")
                                ], className="inside-container2")
                                 
                        ],className="container2"),
    
    
                       html.Div(                                 
                                 html.Div(dcc.Graph(id="Graph2",config={'displayModeBar': False},style={"display":"inline"}),className="inside-container3")
                              ,className="container3"),
    
                        html.Div(                                 
                                 html.Div(dcc.Graph(id="Graph3",config={'displayModeBar': False},style={"display":"inline"}),className="inside-container4")
                                 
                               
                                 
                                 ,className="container4"),
                         html.Div(                                 
                                 html.Div(dcc.Graph(id="Graph4",config={'displayModeBar': False},style={"display":"inline"}),className="inside-container5")
                          ,className="container5")

],className="main-container")


# In[3]:


@app.callback(
    Output('indicator1', 'figure'),
    Input('period-dd', 'value')
    
)
def displayClick(select_period):
    if select_period == "Past 12 months":
        period_selector = 12
     
    elif select_period == "Past 6 months":
        period_selector = 6
        
    elif select_period == "Past 3 months":
        period_selector = 3
        
    elif select_period == "Past 1 month":
        period_selector = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector:,:]
    lag_df_total_kwh["bill_total"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector,:]
    x = show_df_total_kwh["bill_total"].sum()
    
    ddf_bill_therms =df_therms.set_index(["bill_start_date"])
    new_df_total_therms = ddf_bill_therms["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_therms.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_therms["month_year"]=new_df_total_therms["bill_start_date"].dt.strftime("%b %y")
    new_df_total_therms
    
    total_df_total_therms= new_df_total_therms.iloc[:period_selector*2,:]
    lag_df_total_therms = total_df_total_therms.iloc[period_selector:,:]
    lag_df_total_therms["bill_total"].sum()
    
    show_df_total_therms = new_df_total_therms.iloc[:period_selector,:]
    y = show_df_total_therms["bill_total"].sum()
    

    fig = go.Figure()
    

    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"kWh", 'font': {'size': 15}},    
#           domain={'x': [0, 1], 'y': [.6, 1]}
                domain = {'row': 0, 'column': 0}
        ))
    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"Cost", 'font': {'size': 15}},        
                domain = {'row': 1, 'column': 0}

        ))
    
    
    fig.update_layout(
            title={'text': 'Electric',
                   'font': {'size': 20},
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='white'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 256,
        grid = {'rows': 2, 'columns': 1, 'pattern': "independent", 'ygap': .99},
        autosize = True,
#         margin={'t': 0,'l':0,'b':0,'r':0}
        )
  
 
    return fig


# In[4]:


@app.callback(
    Output('indicator2', 'figure'),
    Input('period-dd', 'value')
    
)
def displayClick(select_period):
    if select_period == "Past 12 months":
        period_selector = 12
     
    elif select_period == "Past 6 months":
        period_selector = 6
        
    elif select_period == "Past 3 months":
        period_selector = 3
        
    elif select_period == "Past 1 month":
        period_selector = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector:,:]
    lag_df_total_kwh["bill_total"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector,:]
    x = show_df_total_kwh["bill_total"].sum()
    
    ddf_bill_therms =df_therms.set_index(["bill_start_date"])
    new_df_total_therms = ddf_bill_therms["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_therms.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_therms["month_year"]=new_df_total_therms["bill_start_date"].dt.strftime("%b %y")
    new_df_total_therms
    
    total_df_total_therms= new_df_total_therms.iloc[:period_selector*2,:]
    lag_df_total_therms = total_df_total_therms.iloc[period_selector:,:]
    lag_df_total_therms["bill_total"].sum()
    
    show_df_total_therms = new_df_total_therms.iloc[:period_selector,:]
    y = show_df_total_therms["bill_total"].sum()
    

    fig = go.Figure()
    

    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"Therms", 'font': {'size': 15}},    
#           domain={'x': [0, 1], 'y': [.6, 1]}
                domain = {'row': 0, 'column': 0}
        ))
    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"Cost", 'font': {'size': 15}},        
                domain = {'row': 1, 'column': 0}

                   
#          domain={'y': [0.8, 1.0], 'x': [0, 1.00]}
        ))
    
    
    fig.update_layout(
            title={'text': 'Gas',
                   'font': {'size': 20},
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='white'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 256,
        grid = {'rows': 2, 'columns': 1, 'pattern': "independent", 'ygap': .99},
        autosize = True,
#         margin={'t': 0,'l':0,'b':0,'r':0}
        )
 
    return fig


# In[5]:


@app.callback(
    Output('indicator3', 'figure'),
    Input('period-dd', 'value')
    
)
def displayClick(select_period):
    if select_period == "Past 12 months":
        period_selector = 12
     
    elif select_period == "Past 6 months":
        period_selector = 6
        
    elif select_period == "Past 3 months":
        period_selector = 3
        
    elif select_period == "Past 1 month":
        period_selector = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector:,:]
    lag_df_total_kwh["bill_total"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector,:]
    x = show_df_total_kwh["bill_total"].sum()
    
    ddf_bill_therms =df_therms.set_index(["bill_start_date"])
    new_df_total_therms = ddf_bill_therms["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_therms.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_therms["month_year"]=new_df_total_therms["bill_start_date"].dt.strftime("%b %y")
    new_df_total_therms
    
    total_df_total_therms= new_df_total_therms.iloc[:period_selector*2,:]
    lag_df_total_therms = total_df_total_therms.iloc[period_selector:,:]
    lag_df_total_therms["bill_total"].sum()
    
    show_df_total_therms = new_df_total_therms.iloc[:period_selector,:]
    y = show_df_total_therms["bill_total"].sum()
    

    fig = go.Figure()
    

    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"lbs of CO2", 'font': {'size': 15}},    
#           domain={'x': [0, 1], 'y': [.6, 1]}
                domain = {'row': 0, 'column': 0}
        ))
    
    fig.add_trace(go.Indicator(
               mode='number+delta',
               value=show_df_total_therms["bill_total"].sum(),
               delta = {'reference': lag_df_total_therms["bill_total"].sum(),
                        'position': 'bottom',
                        'valueformat': ',g',
                        'relative': False,
                        'font': {'size': 15}},
               number={'valueformat': ',',
                       'font': {'size': 20}},
                 title = {'text':"Emissions", 'font': {'size': 15}},        
                domain = {'row': 1, 'column': 0}

                   
#          domain={'y': [0.8, 1.0], 'x': [0, 1.00]}
        ))
    
    
    fig.update_layout(
            title={'text': 'Emissions',
                   'font': {'size': 20},
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color='white'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height = 256,
        grid = {'rows': 2, 'columns': 1, 'pattern': "independent", 'ygap': .99},
        autosize = True,
#         margin={'t': 0,'l':0,'b':0,'r':0}
        )
 
    return fig


# In[ ]:





# In[6]:


@app.callback(
    Output('Graph2', 'figure'),
    Input('period-dd', 'value')
    
)
def displayClick(select_period):
    if select_period == "Past 12 months":
        period_selector = 12
     
    elif select_period == "Past 6 months":
        period_selector = 6
        
    elif select_period == "Past 3 months":
        period_selector = 3
        
    elif select_period == "Past 1 month":
        period_selector = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector:,:]
    lag_df_total_kwh["bill_total"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector,:]
    x = show_df_total_kwh["bill_total"].sum()
    
    ddf_bill_therms =df_therms.set_index(["bill_start_date"])
    new_df_total_therms = ddf_bill_therms["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_therms.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_therms["month_year"]=new_df_total_therms["bill_start_date"].dt.strftime("%b %y")
    new_df_total_therms
    
    total_df_total_therms= new_df_total_therms.iloc[:period_selector*2,:]
    lag_df_total_therms = total_df_total_therms.iloc[period_selector:,:]
    lag_df_total_therms["bill_total"].sum()
    
    show_df_total_therms = new_df_total_therms.iloc[:period_selector,:]
    y = show_df_total_therms["bill_total"].sum()
    
    
    
    
    trace2 = go.Pie(
            labels=['Electric Cost', 'Gas Cost'],
            values=[x,y],
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=45,
                  )
    data2 = trace2
    
    layout2 = go.Layout(
            title={'text': 'Energy Expenditure: ',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.4}

        )
    fig2 = go.Figure(data = trace2, layout = layout2)
    fig2.update_layout(autosize = True)
    
    return fig2 


# In[7]:


@app.callback(
    Output('Graph3', 'figure'),
    [Input('period-dd', 'value')]
    
)
def displayClick(select_period):
    global period_selector2
    if select_period == "Past 12 months":
        period_selector2 = 12
     
    elif select_period == "Past 6 months":
        period_selector2 = 6
        
    elif select_period == "Past 3 months":
        period_selector2 = 3
        
    elif select_period == "Past 1 month":
        period_selector2 = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_volume"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector2*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector2:,:]
    lag_df_total_kwh["bill_volume"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector2,:]
    show_df_total_kwh["bill_volume"].sum()
    
    trace2 = go.Bar(x =show_df_total_kwh["month_year"], y=show_df_total_kwh["bill_volume"],marker_color = "orange")
    data2 = trace2
    layout2 = go.Layout(title={'text': 'Electric Cost:',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Month/Year</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=0.5,
                       ticks='outside',
                       tickfont=dict(
                           family='sans-serif',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Total Cost</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='sans-serif',
                           color='white',
                           size=12
                       )
                      ))
     
    fig2 = go.Figure(data = trace2, layout = layout2)
    fig2.update_layout(autosize = True)
    
    return fig2 


# In[8]:


@app.callback(
    Output('Graph4', 'figure'),
    [Input('period-dd', 'value')]
    
)
def displayClick(select_period):
    global period_selector2
    if select_period == "Past 12 months":
        period_selector2 = 12
     
    elif select_period == "Past 6 months":
        period_selector2 = 6
        
    elif select_period == "Past 3 months":
        period_selector2 = 3
        
    elif select_period == "Past 1 month":
        period_selector2 = 1
        
    from dash import dcc
    import plotly.graph_objs as go
    
    ddf_bill_kwh =df_kwh.set_index(["bill_start_date"])
    new_df_total_kwh = ddf_bill_kwh["bill_total"].resample('1M', kind = "period").sum().reset_index()
    new_df_total_kwh.sort_values(by=["bill_start_date"], ascending = False, inplace = True)
    new_df_total_kwh["month_year"]=new_df_total_kwh["bill_start_date"].dt.strftime("%b %y")
    new_df_total_kwh
    
    total_df_total_kwh= new_df_total_kwh.iloc[:period_selector2*2,:]
    lag_df_total_kwh = total_df_total_kwh.iloc[period_selector2:,:]
    lag_df_total_kwh["bill_total"].sum()
    
    show_df_total_kwh = new_df_total_kwh.iloc[:period_selector2,:]
    show_df_total_kwh["bill_total"].sum()
    
    trace2 = go.Bar(x =show_df_total_kwh["month_year"], y=show_df_total_kwh["bill_total"],marker_color = "orange")
    data2 = trace2
    layout2 = go.Layout(title={'text': 'Gas Cost:',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Month/Year</b>',
                       color = 'white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=0.5,
                       ticks='outside',
                       tickfont=dict(
                           family='sans-serif',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b>Total Cost</b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='sans-serif',
                           color='white',
                           size=12
                       )
                      ))
     
    fig2 = go.Figure(data = trace2, layout = layout2)
    fig2.update_layout(autosize = True)
    
    return fig2 


# In[ ]:



if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





# In[ ]:





# In[ ]:




