import os
import re
import time
import json
import pickle
import datetime
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None  # default='warn'

class Utils:

    def __init__(self, mypath):
        
        self.mypath = mypath
        self.stage = os.path.dirname(self.mypath)
        self.env = os.path.dirname(self.stage)
        self.home_dir = os.path.dirname(self.env)
        
        # data
        self.data = os.path.join(self.home_dir, 'Data')
        
    def open_json(self, filename):
        with open(f'{filename}', 'r', encoding='utf-8') as f:
            d = json.load(f)
        return(d)

    def save_json(self, data, filename):
        with open(f'{filename}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
    def get_all_filenames(self, path):
        onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return onlyfiles
    
    def get_all_filepaths(self, path):
        onlyfiles = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return onlyfiles
    
    def flatten_list(self, main_list):
        flat_list = [item for sublist in main_list for item in sublist]
        return flat_list
    
    # pickle 
    def create_pickle(self, data, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def read_pickle(self, filename):
        with open(filename, 'rb') as handle:
            b = pickle.load(handle)
        return b
    
    # datetime
    def date_10_yr_back(self):
        first_date_s = '9/7/2009' # reference dates
        first_date_e = '9/7/2019' # reference dates
        first_datetime_s = datetime.datetime.strptime(first_date_s, '%m/%d/%Y')
        first_datetime_e = datetime.datetime.strptime(first_date_e, '%m/%d/%Y')
        days_ahead = first_datetime_s - first_datetime_e # measuring 10 years worth of data

        dt_end = datetime.datetime.now() 
        dt_start = datetime.datetime.now() + days_ahead

        date_end = dt_end.strftime('%Y-%m-%d')
        date_start = dt_start.strftime('%Y-%m-%d')
        return date_start, date_end
    
    # e.g. utils.delta_days('%Y/%m/%d', '2021/02/01', 100)
    def delta_days(self, date_format, date_str, days_delta):
        prior_dt = datetime.datetime.strptime(date_str, date_format) - datetime.timedelta(int(days_delta))
        return prior_dt.strftime(date_format)
    
    def T_n(self, dt, n, seq = [0,1,2,3,4,5,6]):

        T_n_date = dt + datetime.timedelta(n)
        DayOfWeek = T_n_date.weekday()

        seq_idx = seq.index(DayOfWeek)

        delta = 0
        if (seq_idx > 4):
            if (n < 0):
                delta = -(seq_idx - 4)
            elif (n > 0):
                delta = 7 - seq_idx

        return T_n_date + datetime.timedelta(delta)
        
mypath = os.path.dirname(os.path.abspath(__file__))
utils = Utils(mypath)