import pandas as pd
import numpy as np

class PandasDataAnalysis:
        
    def __init__(self,stkidx,dirnamelog,dirdatafolder,str_first_year_month_day,opt_verbose='OFF'):
        
        csv_datafolder = '{}/{}.csv'.format(dirdatafolder,stkidx)
        self.stkidx = stkidx
        self.dirnamelog = dirnamelog
        self.str_first_year_month_day = str_first_year_month_day
        self.opt_verbose = opt_verbose

        # get date, open, high, low, close price and volume from csv file
        ################## remark index_col = [0] ###############
        ## then 'date' become a column name \
        #          date    volume   open   high    low  close CmpName
        #0   2018-05-02   4715058  17.20  18.10  17.00  17.05      台航
        #1   2018-05-03    956738  16.85  16.95  16.65  16.85      台航
        #2   2018-05-04    612524  17.00  17.30  16.90  16.95      台航
        #3   2018-05-07    776401  17.15  17.25  16.70  16.75      台航

        # get date and close from csv file
        csv_stockfile = pd.read_csv(csv_datafolder, header = None, encoding = 'cp950', 
                            usecols = [0,3,4,5,6,9,10], #index_col = [0], 
                            names = ['date', 'open', 'high', 'low', 'close', 'Stkidx','CmpName'],
                            parse_dates = [0],
                            date_parser = lambda x:pd.datetime.strptime(x,'%Y/%m/%d'))
        df = csv_stockfile.copy()
        self.df = df

    # delete dataframe of both duplicates and nonetradeday
    def get_tradedays_dfinfo(self):

        df_delduplicates = self.df.drop_duplicates()

        if self.opt_verbose.lower == 'on':
            # get row count after delet duplicated row
            print("row counts after drop duplicated rows: {}".format(len(df_delduplicates.index)) )

        # sort pandas dataframe from column 'date'
        df_delduplicates_sortasc = df_delduplicates.sort_values('date',ascending=1)

        # check clsoe price if includes '---' or '--' or not, but
        # 2018/09/04 dtype of close price icluding '---' and '--' is object except float64
        # convert value to string if value does have digitals
        if self.df['close'].dtype == np.object:
            # DataFrame filter close column by regex
            df_delduplicates_sortasc_nonetradeday = df_delduplicates_sortasc.loc[
                                                    df_delduplicates_sortasc['close'].str.contains(r'^-+-$')]
            if self.opt_verbose.lower == 'on':
                #print(df_delduplicates_sortasc_nonetradeday)
                print("row counts with none trade: {}".format(len(df_delduplicates_sortasc_nonetradeday)) )

            # df_delduplicates_sortasc['close'] exclude (r'^-+-$')
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc[~df_delduplicates_sortasc['close'].str.contains(r'^-+-$')]
        elif self.df['close'].dtype == np.float64:
            df_delduplicates_sortasc_tradeday = df_delduplicates_sortasc

        if self.opt_verbose.lower == 'on':
            print("row counts with trade: {}".format(len(df_delduplicates_sortasc_tradeday)) )

        return df_delduplicates_sortasc_tradeday    