import locale
import calendar
from plotly.subplots import make_subplots
# from calendra.core import Calendar
# from  workalendar import Calendar
# from workalendar.europe import Germany
from datetime import date
from calendra.europe import Germany
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import pdb
#===========================================
# scratch
#===========================================


#===========================================
#-------------------------------------------
def custom_calendar() -> None: 

    #-------------------------------------------
    # calendar definition
    locale.setlocale(locale.LC_ALL, 'de_DE')
    year = 2022
    months = [3, 4, 5]
    size = 2048  # size of calendar
    aspect_ratio = 0.1

    c1 = calendar.Calendar()

    #-------------------------------------------
    # German holidays (not equals Beyern)
    cal_label = Germany()
    #-------------------------------------------
    # color definition
    rowEvenColor = 'floralwhite'
    rowEvenColor = 'white'
    rowOddColor = 'linen'

    header_color = ['chocolate', 'crimson', 'maroon', ]
    header_color = ['tomato', 'crimson', 'brown', 'maroon', ]
    header_color = ['tomato', 'deeppink', 'brown', 'maroon', ]
#    header_color = ['tomato', 'brown', 'mediumvioletred', 'brown', 'maroon', ]
#    header_color = ['orange', 'darkseagreen','steelblue', 'darkturquoise']

    date_color = 'salmon'
    wd_color = ['darkgray'] * 5 
    wd_color.append('slategray')
#    wd_color.append('steelblue')
#    wd_color.append('skyblue')
#    wd_color.append('orange')
    wd_color.append('chocolate')
    holiday_color = 'rosybrown'
#    holiday_color = 'plum'
#    holiday_color = 'thistle'
#    holiday_color = 'pink'
#    holiday_color = 'lightslategray'
#    holiday_color = 'lightsteelblue'
 
    #-------------------------------------------
    # data prepartion -> df_list
    #-------------------------------------------
    df_list = []
    dowc_list = []
    for i in months:
        date_list = []
        dow_color = []
        for w in c1.monthdays2calendar(year,i):
            for (d, wd), dn in zip(w, calendar.day_abbr):
                if d !=0: 
                    c = cal_label.get_holiday_label(date(year, i, d))
                    if c == None:
                        c = ''

                    date_list.append((d, dn, c) )
                    dow_color.append(wd_color[wd]) 

        #-------------------------------------------
        df = pd.DataFrame(list(date_list), columns=['date', 'day_of_week', 'note'])
        df_list.append(df) 
        dowc_list.append(dow_color)

    #-------------------------------------------
    # plot preparation
    #-------------------------------------------
    # calculate plotting area
    v_space = -0.01
    v_len = 1.0 - (len(months) -1.0 ) * v_space 

    v_p = np.array([len(df) for df in df_list]) 
    v_p = v_p/v_p.sum() * v_len
    v_p = np.array([[v,v_space]  for v in v_p]).flatten().cumsum()
    v_p = np.insert(v_p, 0, [0.0])

    yr = [v_p[i*2:i*2+2].tolist() for i in list(reversed(range(len(months))))]
    xr = [[0,1] for i in range(len(months))]

    #-------------------------------------------
    # to store traces
    data =[]
    #-------------------------------------------
    for ix, df in enumerate(df_list):
#        print(f"{ix} month {ix}")

        trace = go.Table(domain = dict(x=xr[ix], y=yr[ix]),
            columnwidth=[2.2,2.3,12],
            columnorder=[0,1,2],
                        header=dict(values=['', '', calendar.month_name[months[ix]]],
                            height=24, 
                            line = dict(width=0),
                            font = dict(family='Arial Black',
                                        size=14, color='floralwhite'),

                            fill_color=header_color[ix],
                            align=['left']*3),

                        cells = dict(values=[df['date'],
                            df['day_of_week'], 
                            df['note']],
                            fill_color = [[rowOddColor,rowEvenColor] * df.shape[0]],
                            height= 21, 
                            line = dict(color='lightgray', width=2),
                            align=['right', 'left', 'left'], 
                            font = dict(family=['Arial Black','Arial Black','Arial'],
                                        size=12, 
                                        color=[[date_color] * df.shape[0],
                                               dowc_list[ix], 
                                               [holiday_color]* df.shape[0]],))
        )
        data.append(trace)

    layout = go.Layout(
        showlegend=False, 
        height=size,
        width=size * aspect_ratio,  # width=width,
        margin=dict(l=0, r=0, t=0, b=0))

    fig = go.Figure(data=data, layout=layout)
#    fig.show()
    fig.write_image("./custom_calendar.pdf")
    fig.write_image("./custom_calendar.png")



#===========================================
if __name__ == "__main__":
    #    args = sys.argv
    #     if len(args) == 5:
    #         outfile = args[1]
    #         n_stopper = int(args[2])
    #         t_sleep = int(args[3])
    #         innen = args[4]
    #     else:
    #         print(f'\033[33mUsage : \033[96mpython3 \033[0mpolling_mbs.py \
    # [outfile="tweet.csv"] [n_stopper=100] [t_sleep=1] [innen False]')
    #         exit()
    custom_calendar()


#-------------------------------------------

# The Chart Studio Cloud (at https://chart-studio.plotly.com or on-premise) 
# generates images on a server, 
# where only a select number of fonts are installed and supported. These include 
# "Arial", "Balto", "Courier New", "Droid Sans",, "Droid Serif", 
# "Droid Sans Mono", "Gravitas One", "Old Standard TT", 
# "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman".