# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 12:16:40 2018

@author: Tianxin Desktop

Run this code every day at 00:30 to get the previous day's data from each pi
Results will be saved to the COA computer
"""
import paramiko
from scp import SCPClient
from datetime import date, timedelta
import os
from fnmatch import fnmatch

# create today and yesterday datatime string
def datatime_str():
    today_str = date.today().strftime('%Y%m%d')
    yesterday_str = (date.today() - 
                     timedelta(1)).strftime('%Y%m%d')
    return today_str, yesterday_str

def copy_and_del_txt_from_a_pi(ip, save_dir):
    
#    ip_in_hyphen_form = ip_in_dot_form.replace('.', '-')
#    new_name = 'pi172-18-161-48pi20180621.txt'
    # create ssh object
    ssh = paramiko.SSHClient()

    # Solve unknown host issue
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.load_system_host_keys()

    # Connect to the pi
    ssh.connect(ip, port=22, username='pi', password='raspberry')

    # get all files in the directory
    stdin, stdout, stderr = ssh.exec_command('ls')
    output = stdout.readlines()

    # create scp object
    scp = SCPClient(ssh.get_transport())

    ip_hyphen = ip.replace('.', '-')

    for name in output:
        if fnmatch(name, 'pi*.txt*'):
            txt = name.rstrip()
            if txt < compare_str:
                new_name = txt[:2] + ip_hyphen + txt
                print(new_name)
                new_dir = save_dir + '/' + new_name
                print(new_dir)
                scp.get(txt, new_dir)
                print("scp OK~")
                ssh.exec_command('sudo rm -f {0}'.format(txt))
                print("delete copied txt ok~")


    # close the scp connection
    scp.close()
    # close the ssh connection
    ssh.close() 
    print("{} done!".format(ip))








    
def copy_txt_from_pi_list_to_coa_computer(ip_list, coa_dir):
    # adjust the current time to the similar string of file names
    # which used to set the time so the prog will fetch files earlier than this
    today_str, yes_str = datatime_str()
    compare_str = 'pi' + today_str + '.txt'
    save_dir = coa_dir+'/'+ yes_str
    #Create save_dir
    os.mkdir(save_dir)
    for ip in ip_list:
        copy_and_del_txt_from_a_pi(ip, save_dir)
        
## Case test
# define dir in local machine to copy the data from pi
root_dir = '/home/Perrinek/wifi'
# put the ip of pi's in this list
lst_pi = ['172.16.181.45', '172.16.181.48']
copy_txt_from_pi_list_to_coa_computer(lst_pi, root_dir)