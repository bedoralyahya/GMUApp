from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import datetime
import numpy as np
from dash import dash_table
import spintax


def generate_BreakPointAndIRR():
    servicesTable=[]
    f = open("allData.json","r")
    allData = json.loads(f.read())
    breakPoint={"Financial term":"Break point(s)",
                    "Green 2025":str(allData["output2025.json"]["breakeven"]),
                    "Green 2030":str(allData["output2030.json"]["breakeven"]),
                    "Green 2035":str(allData["output2035.json"]["breakeven"]),
                    # "Green 2040":str(allData["output2040.json"]["breakeven"])
                }
    servicesTable.append(breakPoint)
    irr={"Financial term":"IRR (BaseLine2040)",
         "Green 2025":str('{:.2%}'.format(allData["output2025.json"]["IRR"])),
         "Green 2030":str('{:.2%}'.format(allData["output2030.json"]["IRR"])),
         "Green 2035":str('{:.2%}'.format(allData["output2035.json"]["IRR"]))}
    servicesTable.append(irr)
    irrBase1={"Financial term":"IRR (BaseLine1)",
                 "Green 2025":str('{:.2%}'.format(allData["output2025.json"]["IRR (base1)"])),
                 "Green 2030":str('{:.2%}'.format(allData["output2030.json"]["IRR (base1)"])),
                 "Green 2035":str('{:.2%}'.format(allData["output2035.json"]["IRR (base1)"]))}
    servicesTable.append(irrBase1)
    return servicesTable
def generate_table():
    servicesTable=[]
    f = open("allData.json","r")
    allData = json.loads(f.read())
    for data in allData:
        oneline={"Target Year":allData[data]["name"]}
        for s in allData[data]["services"].keys():
            oneline.update({s:str(allData[data]["services"][s])})
        servicesTable.append(oneline)

    return servicesTable
def findMaxMin(fig):
    y_mins = []
    y_maxs = []
    for trace_data in fig.data:
        #print(fig.data)
        y_mins.append(min(trace_data.y))
        y_maxs.append(max(trace_data.y))
    y_min = min(y_mins)
    y_max = max(y_maxs)
    return ([y_min,y_max])
def readSeg():
    f = open("allData.json","r")
    allData = json.loads(f.read())
    rowNames=[]
    data=[]
    #columnNames=allData[dataLine]["breakevenSegment"]["year"]
    columnNames=["Start","End","p1","p2"]
    for dataLine in allData:
        if "breakevenSegment" in allData[dataLine]:
            for j in range(0,len(allData[dataLine]["breakevenSegment"])) :
                line=allData[dataLine]["breakevenSegment"][j]["year"]
                line.extend(allData[dataLine]["breakevenSegment"][j]["npv"])
                data.append(line)
                rowNames.append("b"+allData[dataLine]["id"]+str("-")+str(j))
    #data.append(columnNames)
    #rowNames.append("Row")
    #rowLabel=["expBaseLine1","eBaseLine1","expBaseLine2030","eBaseLine2030","expGreenInvestments2030","eGreenInvestments2030","expBaseLine2035","eBaseLine2035","expBaseLine2040","eBaseLine2040","Year"]
    ds=pd.DataFrame(data,index=rowNames)

    return ds
def readOutput():
    f = open("allData.json","r")
    allData = json.loads(f.read())
    rowNames=[]
    data=[]
    d = datetime.datetime.strptime("2025-01-01", "%Y-%d-%m")
    startingYear=d.year
    columnNames=[str(startingYear+y)  for y in range(0,25)]
    for dataLine in allData:
        data.append(allData[dataLine]["npv"])
        rowNames.append("exp"+allData[dataLine]["id"])
        data.append(allData[dataLine]["co2"])
        rowNames.append("e"+allData[dataLine]["id"])

    data.append(columnNames)
    rowNames.append("Year")
    #rowLabel=["expBaseLine1","eBaseLine1","expBaseLine2030","eBaseLine2030","expGreenInvestments2030","eGreenInvestments2030","expBaseLine2035","eBaseLine2035","expBaseLine2040","eBaseLine2040","Year"]
    df=pd.DataFrame(data,index=rowNames)
    return df.T
def readCashOutput():
    f = open("allData.json","r")
    allData = json.loads(f.read())
    rowNames=[]
    data=[]
    d = datetime.datetime.strptime("2025-01-01", "%Y-%d-%m")
    startingYear=d.year
    columnNames=[str(startingYear+y)  for y in range(0,25)]
    for dataLine in allData:
        data.append(allData[dataLine]["cashPAPeriod"])
        rowNames.append("exp"+allData[dataLine]["id"])
        data.append(allData[dataLine]["co2"])
        rowNames.append("e"+allData[dataLine]["id"])

    data.append(columnNames)
    rowNames.append("Year")
    #rowLabel=["expBaseLine1","eBaseLine1","expBaseLine2030","eBaseLine2030","expGreenInvestments2030","eGreenInvestments2030","expBaseLine2035","eBaseLine2035","expBaseLine2040","eBaseLine2040","Year"]
    df=pd.DataFrame(data,index=rowNames)
    return df.T
def readOutput2():
    f = open("allData.json","r")
    allData = json.loads(f.read())
    rowNames=[]
    data=[]
    #d = datetime.datetime.strptime("2025-01-01", "%Y-%d-%m")
    #startingYear=d.year
    columnNames=[d["interval"] for d in allData["outputBASE2030.json"]["accCash"] ]
    #columnNames=[str(startingYear+y)  for y in range(0,25)]
    for dataLine in allData:
        data.append([d["amt"] for d in allData[dataLine]["accCash"] ])
        rowNames.append("exp"+allData[dataLine]["id"])


    data.append(columnNames)
    rowNames.append("Year")
    #rowLabel=["expBaseLine1","eBaseLine1","expBaseLine2030","eBaseLine2030","expGreenInvestments2030","eGreenInvestments2030","expBaseLine2035","eBaseLine2035","expBaseLine2040","eBaseLine2040","Year"]
    df=pd.DataFrame(data,index=rowNames)
    return df.T
def readOutput3():
    f = open("allData.json","r")
    allData = json.loads(f.read())
    rowNames=[]
    data=[]
    #d = datetime.datetime.strptime("2025-01-01", "%Y-%d-%m")
    #startingYear=d.year
    columnNames=[d["interval"] for d in allData["outputBASE2030.json"]["cash"] ]
    #columnNames=[str(startingYear+y)  for y in range(0,25)]
    for dataLine in allData:
        data.append([d["amt"] for d in allData[dataLine]["cash"] ])
        rowNames.append("exp"+allData[dataLine]["id"])


    data.append(columnNames)
    rowNames.append("Year")
    df=pd.DataFrame(data,index=rowNames)
    return df.T
def readNPVandIRR():
        fTable=[]
        f = open("allData.json","r")
        data=[]
        allData = json.loads(f.read())
        #columnNames=["NPV","IRR"]
        rowNames=["Green 2025","Green 2030","Green 2035"]
        #saving2030=allData["outputBASE2040.json"]["npvTotal"]-allData["output2030.json"]["npvTotal"]
        #saving2035=allData["outputBASE2040.json"]["npvTotal"]-allData["output2035.json"]["npvTotal"]
        #saving2040=allData["outputBASE2040.json"]["npvTotal"]-allData["output2040.json"]["npvTotal"]
        npv2025=allData["output2025.json"]["npvTotal"]
        npv2030=allData["output2030.json"]["npvTotal"]
        npv2035=allData["output2035.json"]["npvTotal"]
        #npv2040=allData["output2040.json"]["npvTotal"]
        data.append([npv2025,allData["output2025.json"]["IRR"]*100])
        data.append([npv2030,allData["output2030.json"]["IRR"]*100])
        data.append([npv2035,allData["output2035.json"]["IRR"]*100])
        #data.append([npv2040,allData["output2040.json"]["IRR"]*100])
        #data.append(columnNames)
        #rowNames.append("term")

        df=pd.DataFrame(data,index=rowNames)
        pd.options.display.float_format = '{:,.2f}'.format
        #m=df.T
        #print(m["term"].values.tolist())
        #print(m["Green 2030"].values.tolist())
        #print(df.iloc[0].values.tolist())
        #print(df.iloc[:,0].values.tolist())
        #print(df.columns.values.tolist())
        #print("data ff"+ str(df.iloc[0][3]))

        return df
def readIRR():
        fTable=[]
        f = open("allData.json","r")
        data=[]
        allData = json.loads(f.read())
        #columnNames=["NPV","IRR"]
        rowNames=["Green 2025","Green 2030","Green 2035"]
        data.append([allData["output2025.json"]["IRR"]*100])
        data.append([allData["output2030.json"]["IRR"]*100])
        data.append([allData["output2035.json"]["IRR"]*100])


        df=pd.DataFrame(data,index=rowNames)
        pd.options.display.float_format = '{:,.2f}'.format


        return df
def readNPV():
        fTable=[]
        f = open("allData.json","r")
        data=[]
        allData = json.loads(f.read())
        rowNames=["Green 2025","Green 2030","Green 2035"]

        npv2025=allData["output2025.json"]["npvTotal"]
        npv2030=allData["output2030.json"]["npvTotal"]
        npv2035=allData["output2035.json"]["npvTotal"]
        data.append([npv2025])
        data.append([npv2030])
        data.append([npv2035])


        df=pd.DataFrame(data,index=rowNames)
        pd.options.display.float_format = '{:,.2f}'.format


        return df
app = Dash(__name__)
server = app.server
ScenarioList = ['Baseline 1: Annual GMU cost (Doing nothing)',
'Baseline (target year): Annual GMU cost under the assumption that RECs or carbon offsets are purchased every year to fully offset Scope 1 & 2 emissions after the target year',
 'Green (target year): Annual GMU cost under the assumption of optimal (i.e., minimal net present cost for the time horizon of 2025-2050) while guaranteeing carbon neutrality from (target year) onward by investing in Green solutions (solar, energy storage, electric boilers, RECs and offsets). ']
app.layout = html.Div([
    html.H4('Green Assessment and Decision Guidance Tool (GADGET)'),
    html.P('Scenario:'),
    html.Div(
        className="Scenario",
        children=[
            html.Ul(id='my-list', children=[html.Li(i) for i in ScenarioList])
        ],
    ),
    dcc.Graph(id="graph"),
    html.H4('Cost lines:'),
    dcc.Checklist(
        id="checklist",
        options=["BaseLine1","BaseLine2025","Green2025","BaseLine2030","Green2030","BaseLine2035","Green2035","BaseLine2040"], #,"Green2040"
        value=["BaseLine1","BaseLine2025","Green2025","BaseLine2030","Green2030","BaseLine2035","Green2035","BaseLine2040"], #,"Green2040"
        inline=True
    ),
    html.H4('Emission lines:'),
    dcc.Checklist(
            id="checklistEmission",
            options=["BaseLine1","BaseLine2025","Green2025","BaseLine2030","Green2030","BaseLine2035","Green2035","BaseLine2040"], #,"Green2040"
            value=["BaseLine1","BaseLine2025","Green2025","BaseLine2030","Green2030","BaseLine2035","Green2035","BaseLine2040"], #,"Green2040"
            inline=True
    ),
    dcc.Graph(id="graphCashPerYear"),
    dash_table.DataTable(
        id='tablePoints',
        #columns=generate_table()[0].keys(),
        data = generate_BreakPointAndIRR(),
        page_current=0,
        page_size=5,
        page_action='native',
        sort_action='native',
        column_selectable="single",
        #row_selectable="single",
        sort_mode='multi',
        style_table={'overflowX':'scroll',
                     'maxHeight':'300px'},
        style_header={'backgroundColor':'rgb(30, 30, 30)'},
        style_cell={'backgroundColor':'rgb(110,107,107)',
                    'color':'white'},
        sort_by=[]),
    html.H4("Recommendation of investments in (solar, energy storage, electric boilers, RECs and offsets) for every investment period: "),
    dash_table.DataTable(
            id='tableData',
            #columns=generate_table()[0].keys(),
            data = generate_table(),
            page_current=0,
            page_size=10,
            page_action='native',
            sort_action='native',
            column_selectable="single",
            #row_selectable="single",
            sort_mode='multi',
            style_table={'overflowX':'scroll',
                         'maxHeight':'300px'},
            style_header={'backgroundColor':'rgb(30, 30, 30)'},
            style_cell={'backgroundColor':'rgb(110,107,107)',
                        'color':'white'},
            sort_by=[]),
    dcc.Graph(id="graphNPVandIRR"),
    dcc.Graph(id="graphNPV"),
    dcc.Graph(id="graphIRR"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3"),
    #])

])
@app.callback(
    Output("graphIRR", "figure"),
    Input("checklist", "value"))
def update_line_chart(v):
    df =  readIRR()# replace with your own data source
    fig = go.Figure()

    fig.add_trace(go.Bar(x=["Green 2025 ","Green 2030 ","Green 2035 "], y=df[0].values.tolist(),text=df[0].values.tolist(),offsetgroup=0, name="IRR",
        marker=dict(color=['rgba(145,9,9,1)','rgba(172,63,63,1)','rgba(217,78,78,1)']))) #
    fig.update_layout(title_text="IRR (Base2040)")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, texttemplate='%{y:.2f}%')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text="<b> IRR(%)</b>")

    return fig
@app.callback(
    Output("graphNPV", "figure"),
    Input("checklist", "value"))
def update_line_chart(v):
    df =  readNPV()# replace with your own data source
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Green 2025 ","Green 2030 ","Green 2035 "], y=df[0].values.tolist(), text=df[0].values.tolist(),offsetgroup=0,name="NPV",
        marker=dict(color=['rgba(3,94,35,1)','rgba(87,150,109,1)','rgba(160,204,175,1)']))) #
    fig.update_layout(title_text=" Total NPV")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, texttemplate='%{y:.2f} $')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text="<b> Total NPV (dollars) </b>")


    return fig
@app.callback(
    Output("graphNPVandIRR", "figure"),
    Input("checklist", "value"))
def update_line_chart(v):
    df =  readNPVandIRR()# replace with your own data source
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=["Green 2025 ","Green 2030 ","Green 2035 "], y=df[0].values.tolist(), text=df[0].values.tolist(),offsetgroup=0,name="NPV",
        marker=dict(color=['rgba(3,94,35,1)','rgba(87,150,109,1)','rgba(160,204,175,1)'])),secondary_y=False) #
    fig.add_trace(go.Bar(x=["Green 2025 ","Green 2030 ","Green 2035 "], y=df[1].values.tolist(),text=df[1].values.tolist(),offsetgroup=1, name="IRR",
        marker=dict(color=['rgba(145,9,9,1)','rgba(172,63,63,1)','rgba(217,78,78,1)'])),secondary_y=True) #
    fig.update_layout(title_text=" Total NPV and IRR")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, texttemplate='%{y:.2f}')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title_text="<b>primary</b> Total NPV (dollars)", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> IRR(%) " , secondary_y=True)

    return fig

@app.callback(
    Output("graph2", "figure"),
    Input("checklist", "value"))
def update_line_chart(v):
    df =  readOutput2()# replace with your own data source
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig = go.Figure()
    colors=['#361c0a','#EF553B','#00CC96','#FFA15A','#AB63FA','#FF97FF','#636EFA','#19D3F3','#FF6692''#B6E880',]
    count=0
    for x in v:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["exp"+x].values.tolist(), line_shape='hv',name=x,line = dict(color=colors[count])),secondary_y=False)
        #fig.add_trace(go.Scatter(x=["2022","2022"],y=findMaxMin(fig),line=dict(color='black', dash='dot', width=2),mode='lines',opacity=.7, name="payback BaseLine 1"))
        count=count+1
    # Add figure title
    fig.update_layout(title_text=" Cumulative CashFlow")
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> Cumulative Cash Flow (dollars)", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> CO2-eq (Tons)".translate(SUB) , secondary_y=True)

    return fig
@app.callback(
    Output("graph3", "figure"),
    Input("checklist", "value"))
def update_line_chart(v):
    df =  readOutput3()# replace with your own data source
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig = go.Figure()
    colors=['#361c0a','#19D3F3','#00CC96','#FFA15A','#AB63FA','#FF97FF','#636EFA','#EF553B','#FF6692''#B6E880',]
    colorsL=['#FECB52','#bbe8f0','#b4dbd1','#fce5d4','#ead6ff','#fcd4fc','#b2d5eb','#facfc8','#ffd1de','#d1e3bf']
    count=0
    for x in v:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["exp"+x].values.tolist(),mode='lines+markers',name=x,line = dict(color=colors[count])),secondary_y=False)
        #fig.add_trace(go.Scatter(x=["2022","2022"],y=findMaxMin(fig),line=dict(color='black', dash='dot', width=2),mode='lines',opacity=.7, name="payback BaseLine 1"))
        count=count+1
    # Add figure title
    fig.update_layout(title_text=" CashFlow")
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> Cash Flow (dollars)", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> CO2-eq (Tons)".translate(SUB) , secondary_y=True)

    return fig
@app.callback(
    Output("graph", "figure"),
    [Input("checklist", "value"),Input("checklistEmission", "value")]
    )
def update_line_chart(v,e):
    df =  readOutput()# replace with your own data source
    ds = readSeg()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    colors=['#361c0a','#19D3F3','#00CC96','#FFA15A','#AB63FA','#FF97FF','#636EFA','#EF553B','#FF6692''#B6E880',]
    colorsL=['#FECB52','#bbe8f0','#b4dbd1','#fce5d4','#ead6ff','#fcd4fc','#b2d5eb','#facfc8','#ffd1de','#d1e3bf']

    xColorIndex={"BaseLine1":0,"BaseLine2025":1,"Green2025":2,"BaseLine2030":3,"Green2030":4,"BaseLine2035":5,"Green2035":6,"BaseLine2040":7,"Green2040":8}
    count=0

    for x in v:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["exp"+x].values.tolist(), name="cost <i>"+x+"</i>",line = dict(color=colors[xColorIndex[x]])),secondary_y=False)

        if x in ["Green2025","Green2030","Green2035","Green2040"]:
            list=ds.index.values.tolist()
            m=0
            for v in list:
                if x in v:
                    m=m+1
            for i in range(0,m):
                # 'rgba(200,107,243,0.2)'
                fig.add_trace(go.Scatter(x=[int(ds.loc["b"+x+"-"+str(i)][0]),int(ds.loc["b"+x+"-"+str(i)][1])], y=[ds.loc["b"+x+"-"+str(i)][2],ds.loc["b"+x+"-"+str(i)][3]],line_color=colors[xColorIndex[x]], fill='tozeroy',fillcolor=colorsL[xColorIndex[x]],name='Breakeven <i>'+x+'</i>'),secondary_y=False) #+str(i+1)
    for z in e:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["e"+z].values.tolist(),name="emission <i>"+z+"</i>",line = dict(color=colors[xColorIndex[z]], dash='dash')),secondary_y=True)

        #fig.add_trace(go.Scatter(x=["2022","2022"],y=findMaxMin(fig),line=dict(color='black', dash='dot', width=2),mode='lines',opacity=.7, name="payback BaseLine 1"))
        count=count+1
    # Add figure title
    fig.update_layout(title_text="Annual cost(NPV) and emission",height=700)
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> annual NPV (dollars)", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> CO2-eq (Tons)".translate(SUB) , secondary_y=True)
    names = set()
    fig.for_each_trace(lambda trace:
        trace.update(showlegend=False)
        if (trace.name in names) else names.add(trace.name))

    return fig
@app.callback(
    Output("graphCashPerYear", "figure"),
    [Input("checklist", "value"),Input("checklistEmission", "value")]
    )
def update_line_chart(v,e):
    df =  readCashOutput()# replace with your own data source
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig = go.Figure()
    colors=['#361c0a','#19D3F3','#00CC96','#FFA15A','#AB63FA','#FF97FF','#636EFA','#EF553B','#FF6692''#B6E880',]
    colorsL=['#FECB52','#bbe8f0','#b4dbd1','#fce5d4','#ead6ff','#fcd4fc','#b2d5eb','#facfc8','#ffd1de','#d1e3bf']

    xColorIndex={"BaseLine1":0,"BaseLine2025":1,"Green2025":2,"BaseLine2030":3,"Green2030":4,"BaseLine2035":5,"Green2035":6,"BaseLine2040":7,"Green2040":8}
    count=0

    for x in v:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["exp"+x].values.tolist(), name="cashFlow <i>"+x+"</i>",line = dict(color=colors[xColorIndex[x]])),secondary_y=False)

    for z in e:
        fig.add_trace(go.Scatter(x=df["Year"].values.tolist(), y=df["e"+z].values.tolist(),name="emission <i>"+z+"</i>",line = dict(color=colors[xColorIndex[z]], dash='dash')),secondary_y=True)

        #fig.add_trace(go.Scatter(x=["2022","2022"],y=findMaxMin(fig),line=dict(color='black', dash='dot', width=2),mode='lines',opacity=.7, name="payback BaseLine 1"))
        count=count+1
    # Add figure title
    fig.update_layout(title_text="Annual cashFlow and emission",height=700)
    # Set x-axis title
    fig.update_xaxes(title_text="Year")
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> annual cashFlow (dollars)", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> CO2-eq (Tons)".translate(SUB) , secondary_y=True)
    names = set()
    fig.for_each_trace(lambda trace:
        trace.update(showlegend=False)
        if (trace.name in names) else names.add(trace.name))

    return fig
@app.callback(
    Output('tableData','data'),
    Input('checklist','value'))
def update_tableData(value):
    dataAll=[]
    newData=generate_table()
    return newData


if __name__ == '__main__':
    app.run_server(debug=True)
