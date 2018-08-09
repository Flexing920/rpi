# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:32:53 2018

@author: Tianxin Desktop
"""


import pandas as pd


mac_dict = {}
data_dir = r'C:\Users\Tianxin Desktop\Desktop\test.txt'

data = pd.read_csv(data_dir, sep="\t", dtype=object, header=None)
data.columns = ["mac_address", "timestamp"]

if bool(mac_dict):
    i = int(max(mac_dict.values())) + 1
else:
    i = 1

for index, row in data.iterrows():
    mac = row["mac_address"]
    if mac not in mac_dict.keys():
        mac_dict[mac] = '{0:010d}'.format(i)
        i += 1

df = pd.concat([data,pd.DataFrame(columns=["id"])])

for index, row in df.iterrows():
    df.iloc[index, 0] = mac_dict[df.iloc[index, 1]]
    
out_df = pd.DataFrame(df, columns=['id', 'timestamp'])
out_df['timestamp'] = pd.to_datetime(out_df['timestamp'], unit='s')