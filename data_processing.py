#!/usr/bin/env python3

import pandas as pd
import numpy as np

def create_database():
    #Opens the excel csv and assigns it a database to be manipulated
    covDataRaw = pd.read_csv('data/covid_data_bristol.csv')
    dF = pd.DataFrame(covDataRaw)

    #Just taking out all the columns of info we do not need
    del dF['regionCode']
    dF.pop('regionName')
    dF.pop('UtlaCode')
    dF.pop('UtlaName')
    dF.pop('LtlaCode')
    dF.pop('LtlaName')
    dF.pop('areaType')
    
    return dF
    
