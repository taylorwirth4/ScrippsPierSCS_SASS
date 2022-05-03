#  Calculate k0ext for each calibration point
def plot_all(unq_sen,df,datetime,pHint,pHext,O2con,O2sat,SBEtemp,O2temp,pHtemp,SBEsal,pressure,pdf,ddf):
      import plotly.express as px
      import plotly.graph_objects as go
      from plotly.subplots import make_subplots
      import pandas as pd
      import numpy as np
      from matplotlib.cm import get_cmap

      fig = make_subplots(rows=5, cols=1,
                    specs=[[{"secondary_y": True}], [{"secondary_y": True}],
                           [{"secondary_y": True}], [{"secondary_y": True}],
                           [{"secondary_y": True}]],
                   vertical_spacing=0.01,
                   shared_xaxes=True,)


# pH
      fig.add_trace(go.Scatter(x=datetime, y=pHint,
                    #mode='lines+markers',
                    name='pHint'),
                    secondary_y=False,
                    row=1, col=1)
      fig.add_trace(go.Scatter(x=datetime, y=pHext,
                    #mode='lines+markers',
                    name='pHext'),
                    secondary_y=False,
                    row=1, col=1)
      fig.add_trace(go.Scatter(x=ddf.date, y=ddf.pH_insitu,
                    mode='markers',
                    marker_symbol='circle-open',
                    #marker_size=15,
                    marker_color='black',
                    name='pHdisc'),
                    secondary_y=False,
                    row=1,col=1)
      fig.update_xaxes(range=[min(datetime), max(datetime)])


# delta pH
      fig.add_trace(go.Scatter(x=datetime, y=pHint-pHext,
                    #mode='lines+markers',
                    name='delta_pH (int-ext)'),
                    secondary_y=False,
             row=2, col=1)
      fig.update_yaxes(range=[-np.max(abs(pHint-pHext)), np.max(np.abs(pHint-pHext))], row=2, col=1)
      fig.add_hline(y=0, row=2)
      fig.add_vline(x=datetime[1])

# Oxygen
      fig.add_trace(go.Scatter(x=datetime, y=O2con,
                    #mode='lines+markers',
                    name='O2con'),
              secondary_y=False,
              row=3, col=1)
      fig.add_trace(go.Scatter(x=datetime, y=O2sat,
                    #mode='lines+markers',
                    name='O2sat'),
              secondary_y=True,
              row=3, col=1)

# Temp (SBE & pH & Optode)
      fig.add_trace(go.Scatter(x=datetime, y=SBEtemp,
                    #mode='lines+markers',
                    name='SBEtemp'),
              secondary_y=False,
              row=4, col=1)
      fig.add_trace(go.Scatter(x=datetime, y=O2temp,
                    #mode='lines+markers',
                    name='O2temp'),
              secondary_y=False,
              row=4, col=1)
      fig.add_trace(go.Bar(x=pdf.date, y=pdf.prec,
                             name='DailyPrecip',
                           marker_color = 'red',
                          opacity=0.5),
                      secondary_y=True,
                      row=4,col=1)
                      

      TC_offset = np.mean(SBEtemp)-np.mean(pHtemp)
      #fig.add_trace(go.Scatter(x=datetime, y=pHtemp+TC_offset,
      #              #mode='lines+markers',
      #              name='pHtemp',
      #              text=["pH_temp offset"],
      #              textposition="top center"),
      #        secondary_y=False,
      #        row=4, col=1)


# Salinity and pressure
      fig.add_trace(go.Scatter(x=datetime, y=SBEsal,
                    #mode='lines+markers',
                    name='SBEsal'),
              secondary_y=False,
              row=5, col=1)
      #fig.update_yaxes(range=[33, 34], row=5, col=1,secondary_y=False)
      fig.add_trace(go.Scatter(x=datetime, y=pressure,
                    #mode='lines+markers',
                    name='press',
                    opacity=0.5),
              secondary_y=True,
              row=5, col=1)
      fig.update_yaxes(range=[np.min(pressure), np.max(pressure)], row=5, col=1,secondary_y=True)

# edit axis labels
      fig['layout']['yaxis']['title']='pH'
      #fig['layout']['yaxis2']['title']='pHext'
      fig['layout']['yaxis3']['title']='delta_pH'
      fig['layout']['yaxis5']['title']='O2con (umol/kg)'
      fig['layout']['yaxis6']['title']='O2sat (%)'
      fig['layout']['yaxis7']['title']='Temperature (C)'
      fig['layout']['yaxis8']['title']='Precip (in)'
      fig['layout']['yaxis9']['title']='Salinity (PSU)'
      fig['layout']['yaxis10']['title']='Pressure (dbar)'
    
        
      fig.update_layout(height=1000, width=950)
      fig.update_layout(title={
          'text' : 'SIO Pier SASS SCS',
          'x' : 0.5,
          'y' : 0.99,
          'xanchor': 'center',
          'yanchor': 'top'})
      fig.update_layout(hovermode='x unified')
      fig.update_traces(xaxis='x5')
      fig.update_layout(legend=dict(
          orientation="h",
          yanchor="bottom",
          y=1.0,
         xanchor="right",
          x=0.9))
    
      fig.update_xaxes(
          tickangle = 90,
          nticks=50,
          tickformat='%Y-%b-%d',
      )

      # add TCoffset annotation
      #TCstring = 'pH_temp offset = '+ '{:.2f}'.format(TC_offset)
      #fig.add_annotation(dict(font=dict(color='#B6E880',size=12),
      #                                  x=0,
      #                                  y=.38,
      #                                  showarrow=False,
      #                                  text=TCstring,
      #                                  textangle=0,
      #                                  xanchor='left',
      #                                  xref="paper",
      #                                  yref="paper"))
      fig.show()
      return