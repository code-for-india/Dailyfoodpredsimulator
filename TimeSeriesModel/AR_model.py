'''
Created on May 10, 2014

@author: ykotres
'''

import pandas as pd
import gspread as gs
import datetime
import gdata.spreadsheet.service as gservice
from datetime import timedelta
username='weihandev@gmail.com'
password='AdchemyWalmartLabs'
worksheet_name="HKH"

def gs_import(username,password,worksheet_name):
    gc=gs.login(username,password)
    sh=gc.open(worksheet_name)
    wks = sh.get_worksheet(0)
    list_of_lists = wks.get_all_values()
    return list_of_lists

def appending_row(pred_value,updated_date,school_name,password,email,worksheet_name):
#     client = gservice.SpreadsheetsService()
#     client.debug = True
#     client.email = email
#     client.password = password
#     client.source = 'test client'
#     client.ProgrammaticLogin()
#     #rows = []
#     row=({'Date':updated_date,'School_name':school_name,'Students':pred_value})
#     client.InsertRow(row, worksheet_name, 'Sheet1')
    gc=gs.login(email,password)
    sh=gc.open(worksheet_name)
    wks = sh.get_worksheet(0)
    wks.append_row([updated_date, school_name, pred_value]) 

    return 


def data_process(data_list,username,password,worksheet_name):
    df=pd.DataFrame(data_list[1:],columns=['Date','School_name','Students'])
    df['Students']=[int(i) for i in df['Students']]
    school_list=list(set(df['School_name']))
    for school in school_list:
        df_filtered=df[df['School_name']==school][['Date','Students']]
        grouped_data=df_filtered.groupby('Date').max()
        pred_value=pred(grouped_data,3)
        updated_date=next_date(grouped_data.index[-1])
        appending_row(pred_value,updated_date,school,password,username,worksheet_name)
    
        
def pred(dataset,number_of_lags=3):
    pred=dataset['Students'].tail(number_of_lags).mean()
    return pred

def next_date(date):
    last_date=pd.to_datetime(date)
    weekday=last_date.weekday()
    if weekday==5:
        current_date=last_date+timedelta(days=2)
    else:
        current_date=last_date+timedelta(days=1)
    return '%s/%s/%s' % (current_date.month, current_date.day, current_date.year)
#file="/Users/ykotres/Documents/extra_coding/akshaya-patra-data/Indentwise-Menu.xlsx"


#code for importing 

#function give a school name and den split the data into two parts

def splitdata(schoolname,filename):
    xls = pd.ExcelFile(filename)
    df=xls.parse('Indentwise-Menu')
    df_filtered=df[df['SGDESCRIPTION']==schoolname][['INDENTDATE','Indentqty']]
    grouped_data=df_filtered.groupby('INDENTDATE').max()
    
    return grouped_data

#pd_data=pd.DataFrame(reader)
#print pd_data
#pd.read_csv(file,delimiter='\t')
#output=pd.read_csv(file)
#print output
if __name__ == '__main__':
    list1= gs_import(username,password,worksheet_name)
    data_process(list1,username,password,worksheet_name)