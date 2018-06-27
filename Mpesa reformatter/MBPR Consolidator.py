import re
import os
import sys
import datetime
import csv
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.parser import parse

os.curdir
os.chdir("C:/Dropbox/Berkeley MIDS/MIDS+/Tusome/TusomeOps/Mpesa reformatter")

bulk_plan = pd.read_csv("M-pesa bulk payment.csv", sep = ",", skiprows = 3, nrows = 1, usecols = ["Bulk Plan Name", "Bulk Plan Description"])
bulk_plan_dets = bulk_plan.iloc[0,0] + "-" + bulk_plan.iloc[0,1]

columns = ["Record No", "Validation Result", "Transaction Timestamp", "Finished Timestamp", "TransactionID",
           "Transaction Details", " Amount ", "Fee Charge", "Extra Fee Charge", "Status", "Error Code", "Error Message"]
df = pd.DataFrame(pd.read_csv("M-pesa bulk payment.csv", sep = ",", header=12,
                              usecols = columns, index_col = "Record No",
                             parse_dates = ["Transaction Timestamp"]))

cols_corrected = {"Record No": "record_num", "Validation Result": "val_result", "Transaction Timestamp": "trans_time",
                  "Finished Timestamp": "finished_time", "TransactionID": "trans_id", 
                  "Transaction Details": "trans_det", " Amount " : "amt_sent", "Fee Charge" : "fee_1",
                  "Extra Fee Charge" : "fee_2", "Status" : "status", "Error Code" : "err_code", "Error Message" : "err_msg"}

df.rename(columns = cols_corrected, inplace = True)
df.columns

df["trans_time"]

df = df.loc[df.index.dropna()]

def convert(datestr):
    converted = dt.datetime.strptime(str(datestr),"%d%m%Y %H:%M:%S")
    return converted

df.finished_time = df.finished_time.apply(convert)
df.trans_time = df.trans_time.apply(convert)

df=df[["trans_id", "finished_time", "trans_det", "status", "amt_sent", "fee_1", "fee_2", "val_result", "trans_time",
        "err_code", "err_msg"]]

df.trans_id = df.trans_id.str[4:7]

df["bulk_plan_dets"] = bulk_plan_dets


df = df[df.status=="Completed"]