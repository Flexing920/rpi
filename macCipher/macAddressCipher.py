# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 09:32:53 2018

@author: Tianxin Desktop
"""

import os
import pandas as pd


def txt_to_df(file_dir):
    data = pd.read_csv(file_dir, sep="\t", dtype=object, header=None)
    data.columns = ["mac_address", "timestamp"]
    return data

def mac_lookup(df, save_list):
    if bool(save_list):
        i = int(max(save_list.values())) + 1
    else:
        i = 1

    for index, row in df.iterrows():
        mac = row["mac_address"]
        if mac not in save_list.keys():
            save_list[mac] = '{0:010d}'.format(i)
            i += 1
            
    return save_list

def mac_change(df, mac_lookuptable):
    df = pd.concat([df, pd.DataFrame(columns=["id"])])

    for index, row in df.iterrows():
        df.iloc[index, 0] = mac_dict[df.iloc[index, 1]]
#        df.id[index] = mac_dict[df.address[index]]

    return df[["id", "timestamp"]]

#def unixtime_to_date(df):
#    df = pd.DataFrame(df, columns=['id', 'timestamp'])
#    df['date'] = pd.to_datetime(df['timestamp'], unit='s')
#    
#    return df

def read_mac_dict_from_txt(dict_txt_dir):
    df = {}
    if os.stat(dict_txt_dir).st_size == 0:
        df = {}
    else:
        with open(dict_dir, "r") as f:
            for line in f:
                key, value = line.split()
                df[key] = value
    return df

def update_mac_dict(df, dict_txt_dir):
    (pd.DataFrame.from_dict(data=df, orient="index").
     to_csv(dict_txt_dir, sep="\t", header=False))
    
def write_converted_data_to_txt(df, save_dir):
    df.to_csv(save_dir, header=None, index=None, sep="\t", mode="w")

    
if __name__ == "__main__":
    fld = r'C:\Users\Tianxin Desktop\Desktop\test'

    data_dir = os.path.join(fld, 'test.txt')
    dict_dir = os.path.join(fld, 'dict.txt')
    
    mac_dict = read_mac_dict_from_txt(dict_dir)
    data = txt_to_df(data_dir)
    print("The input data looks like: \n", data.head())

    existing_mac_lookup_table = mac_lookup(data, mac_dict)
    print("Existing mac lookup table looks like: \n", 
          existing_mac_lookup_table)

    mac_to_id = mac_change(data, existing_mac_lookup_table)
    print("mac to id done\n", mac_to_id.head())
    
    output_df_dir = os.path.join(fld, "output_df.txt")
    write_converted_data_to_txt(mac_to_id, output_df_dir)

    update_mac_dict(existing_mac_lookup_table, dict_dir)