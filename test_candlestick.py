################################################################################################
#2018/08/31 Initial to use pandas, matplotlib to draw candlestick
#           by https://www.techtrekking.com/how-to-plot-simple-and-candlestick-chart-using-python-pandas-matplotlib/
#2018/09/24 Solve issue:TypeError: unsupported operand type(s) for -: 'str' and 'str'
#
################################################################################################
import pandas as pd
import numpy as np
# import pandas_datareader as datareader
import datetime
import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick_ohlc
# finance module is no longer part of matplotlib
# see: https://github.com/matplotlib/mpl_finance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.dates import num2date, DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pylab as mpl
import os,sys

strabspath=os.path.abspath(__file__)
strdirname=os.path.dirname(strabspath)
dirnamelog=os.path.join(strdirname,"log")
dirdatafolder = os.path.join(strdirname,'data')

from lib.readConfig import ReadConfig as readConfig
from lib.dataAnalysis import PandasDataAnalysis as data_analysis
#2018/11/19 Only available on on matplotlib 2.x
mpl.rcParams['font.sans-serif'] = ['SimHei'] #將預設字體改用SimHei字體for中文


if __name__ == '__main__':
    configPath=os.path.join(strdirname,"config.ini")
    localReadConfig = readConfig(configPath)

    str_first_year_month_day = localReadConfig.get_SeymourExcel("first_year_month_day")
    str_color_ma = localReadConfig.get_SeymourExcel('color_ma05_ma20_ma30')
    list_color_ma = str_color_ma.split(',')
    str_candlestick_weekly_subfolder = localReadConfig.get_SeymourExcel("candlestick_weekly_subfolder")
    
    
    str_buysell_opt = 'call'
    
    str_stkidx = localReadConfig.get_SeymourExcel('stock_index')
    list_stkidx = str_stkidx.split(',')
    
    # to get stock index 
    for stkidx in list_stkidx:
        
        localdata_analysis = data_analysis(stkidx,dirnamelog,dirdatafolder,str_first_year_month_day)
        df_delduplicates_sortasc_tradeday = localdata_analysis.get_tradedays_dfinfo()
        print(df_delduplicates_sortasc_tradeday)
        
        ##############################################################
        # Issue:
        #File "C:\ProgramData\Anaconda3\lib\site-packages\mpl_finance.py", line 288, in _candlestick
        #height = close - open
        #TypeError: unsupported operand type(s) for -: 'str' and 'str'
        ###############################################################
        # Solution: cast data to float
        df_delduplicates_sortasc_tradeday['open'] = df_delduplicates_sortasc_tradeday['open'].astype(float)
        df_delduplicates_sortasc_tradeday['high'] = df_delduplicates_sortasc_tradeday['high'].astype(float)
        df_delduplicates_sortasc_tradeday['low'] = df_delduplicates_sortasc_tradeday['low'].astype(float)
        df_delduplicates_sortasc_tradeday['close'] = df_delduplicates_sortasc_tradeday['close'].astype(float)
        # convert timestamp column to matplotlib date numbers
        df_delduplicates_sortasc_tradeday['date'] = pd.to_datetime(df_delduplicates_sortasc_tradeday['date'])
        df_delduplicates_sortasc_tradeday['date'] = df_delduplicates_sortasc_tradeday['date'].apply(mdates.date2num)

        # Creating required data in new DataFrame OHLC
        df_ohlc= df_delduplicates_sortasc_tradeday[['date', 'open', 'high', 'low','close']].copy()
        #print(df_ohlc)

        # to add the calculated Moving Average as a new column to the right after 'Value'
        # to get 2 digitals after point by using np
        df_ohlc['SMA_05'] = np.round(df_ohlc['close'].rolling(window=5).mean(),2 )
        df_ohlc['SMA_20'] = np.round(df_ohlc['close'].rolling(window=20).mean(),2 )
        df_ohlc['SMA_30'] = np.round(df_ohlc['close'].rolling(window=30).mean(),2 )
    
        list_str = [df_delduplicates_sortasc_tradeday.iloc[-1,-2].astype(str) , 
                    df_delduplicates_sortasc_tradeday.iloc[-1,-1]]
        str_title = '_'.join(list_str)
        f1, ax = plt.subplots(figsize = (12,6))

        # In case you want to check for shorter timespan
        if len(df_ohlc) >= 90:
            df_ohlc =df_ohlc.tail(170)
        else:
            df_ohlc =df_ohlc.tail(len(df_ohlc))
        
        #print(df_ohlc)
        print('Len of dataframe ohlc:{} '.format(len(df_ohlc)))
        
        # plot the candlesticks
        candlestick_ohlc(ax, df_ohlc.values, width=.5, colorup='red', colordown='green')

        mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
        alldays = DayLocator()              # minor ticks on the days
        weekFormatter = DateFormatter('%Y-%m-%d')  # e.g., 2018-09-12; Jan 12
        dayFormatter = DateFormatter('%d')      # e.g., 12

        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
        ax.xaxis.set_major_formatter(weekFormatter)
        
        # Plotting SMA columns
        ax.plot(df_ohlc['date'], df_ohlc['SMA_05'], color = list_color_ma[0], label = 'SMA05')
        ax.plot(df_ohlc['date'], df_ohlc['SMA_20'], color = list_color_ma[1], label = 'SMA20')
        ax.plot(df_ohlc['date'], df_ohlc['SMA_30'], color = list_color_ma[2], label = 'SMA30')

        #plt.grid(True)
        plt.title(str_title)
        ax.yaxis.grid(True)
        plt.legend(loc='best')

        ax.xaxis_date()
        ax.autoscale_view()
        # format the x-ticks with a human-readable date. 
        xt = ax.get_xticks()
        new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
        ax.set_xticklabels(new_xticks,rotation=45, horizontalalignment='right')
        
                
        # Check image sudfloder is existing or not
        candlestick_weeklyfolder = os.path.join(dirnamelog,str_candlestick_weekly_subfolder)
        if not os.path.isdir(candlestick_weeklyfolder):
            os.makedirs(candlestick_weeklyfolder) 

        # Saving image
        str_stock_buysell = '_'.join([str_buysell_opt,str_title])
        print('{}/{}.jpg would be saved.'.format(candlestick_weeklyfolder,str_stock_buysell))
        plt.savefig('{}/{}.jpg'.format(candlestick_weeklyfolder,str_stock_buysell), dpi=400)

        # In case you dont want to save image but just displya it
        plt.show()