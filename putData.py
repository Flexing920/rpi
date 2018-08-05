# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 10:30:03 2018

@author: Tianxin Desktop

Run this code every day at 12:30 to send the saved txts to the CTR server
and put the txt file to the database
"""
import os
from re import findall
from glob import glob
from datetime import date, timedelta
import paramiko
import psycopg2


def get_all_txt_from_a_dir(dir):
    os.chdir(dir)
    txts = []
    for file in glob("pi*.txt"):
        txt = os.path.join(dir, file)
        txts.append(txt)	
    return txts

# get the ip in the form of xxx.xx.xxx.xx from the name of each txt
def find_pattern_content(str):
    pattern = r'pi(.*?)pi'
    content = findall(pattern, str)
    ip = content[0].replace('-', '.')
    return ip

# add the corresponding ip address to each line of a txt
# do this for a bunch of txts
def add_ip_to_txt(txts):
    content = []
    for txt in txts:
        ip = find_pattern_content(txt)
        with open(txt, 'r') as readtxt:
            lines = readtxt.readlines()
            for i in lines:
                temp_1 = i.rstrip('\n')
                temp_2 = temp_1+'\t{}\n'.format(ip)
                content.append(temp_2)
    return content

    
def write_all_to_txt(content, result_txt):
    with open(result_txt, 'w') as w:
        for i in content:
            w.write(i)
            
def datatime_str():
    today_str = date.today().strftime('%Y%m%d')
    yesterday_str = (date.today() - 
                     timedelta(1)).strftime('%Y%m%d')
    return today_str, yesterday_str

# send file to CTR server
def send_file_to_ctr_server(txt, file_save_dir):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    t = paramiko.Transport('nmc-compute2.ctr.utexas.edu', 22)
    t.connect(username='tl24782',password='123$$qwe') # hide for information safety
    sftp = paramiko.SFTPClient.from_transport(t)    
    sftp.put(txt, file_save_dir)
    print("txt upload to CTR OK~ {}".format(today_str))


def create_db_and_copy_day_data(date_info, file_save_dir):
    try:     
        conn = psycopg2.connect("dbname=test2 user=vista password=vista00 host=nmc-compute2.ctr.utexas.edu")
    except:
        print("Unable to connect to the database!")
    
    cur = conn.cursor()
    tbl_name = 'wifi{}'.format(date_info)
    #create a table
    try:
        cur.execute("create table {}(mac char(30),unixtime numeric(15),ip char(15))".format(tbl_name))
    except:
        print("Can't create table {}".format(tbl_name))
    
    conn.commit()
    
    # copy txt to db
    try:
        cur.execute("copy {0} from '{1}' with delimiter E'\t'".format(tbl_name, file_save_dir))
    except:
        print("Can't copy txt {0} to db {1}".format(file_save_dir, tbl_name))
    
    conn.commit()
    
    cur.close()
    conn.close()
    
    print("create_db_and_copy_day_data OK~")


# case test        
today_str, yes_str = datatime_str()

fld = r'C:\Users\Tianxin Desktop\Desktop\test1'
txt_fld = os.path.join(fld, yes_str)            
writeTxt_path = os.path.join(txt_fld, 'all{}.txt'.format(yes_str))
write_all_to_txt(add_ip_to_txt(get_all_txt_from_a_dir(txt_fld)), writeTxt_path)

file_save_dir = '/home/tl24782/test'+'/'+os.path.basename(writeTxt_path)
send_file_to_ctr_server(writeTxt_path, file_save_dir)   
create_db_and_copy_day_data(yes_str, file_save_dir)