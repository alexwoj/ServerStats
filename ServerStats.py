import csv
import os
import psutil
import matplotlib.pyplot as plt
import datetime
import pandas as pd

# Server identification 
server = 'belta'

# Path where CSV and PNG files are going to be generated
path = '/home/admin/web/belta.warpnet.com.br/public_html/'

# Name used for apache and mysql processes
apache_process_name = 'apache2'
mysql_process_name = 'mysql'

# Other variables
filename = str(path) + str(server) + '-ps.csv'
apache_connections = 0
number_of_processes = 0
mysql_load = 0
mysql_memory_usage = 0
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
load_1, load_5, load_15 = os.getloadavg()
load_avg = (load_1 + load_5 + load_15) / 3
listOfProcessNames = list()
available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total


######################################################################################################
# Iterate over all running processes                                                                 #
# https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/ #
######################################################################################################

for proc in psutil.process_iter():
   pInfoDict = proc.as_dict(attrs=['pid', 'memory_percent', 'name', 'cpu_times', 'create_time', 'memory_info'])
   listOfProcessNames.append(pInfoDict)
   number_of_processes += 1

for p in listOfProcessNames:
    if(p['name'] == apache_process_name):
        apache_connections += 1

    if(p['name'] == mysql_process_name):
        mysql_load = p['cpu_times'][0]
        mysql_memory_usage = p['memory_percent']

print("######################################################################################################")
print("now,load_1,load_5,load_15,load_avg,apache_connections,number_of_processes,available_memory")
print(now,load_1,load_5,load_15,load_avg,apache_connections,number_of_processes,available_memory)
print("######################################################################################################")

with open(filename, 'a') as csvfile:
    fieldnames = ['date_time','load_1','load_5','load_15','load_avg','apache_connections','number_of_processes','available_memory','mysql_load','mysql_memory_usage']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerow({'date_time': now, 'load_1': load_1,'load_5': load_5, 'load_15': load_15, 'load_avg': load_avg, 'apache_connections': apache_connections,'number_of_processes': number_of_processes, 'mysql_load': mysql_load,'mysql_memory_usage': mysql_memory_usage,'available_memory': available_memory})

series = pd.read_csv(filename,header=1,parse_dates=True,squeeze=True,names=fieldnames)
date_series = pd.to_datetime(series['date_time'], format='%Y/%m/%d %H:%M:%S')
#y = series.drop(['date_time', 'number_of_processes', 'available_memory'], axis=1)
y = series.drop(['date_time'], axis=1)
plt.legend(['load_1','load_5','load_15'])
fig = plt.plot_date(date_series, y,linestyle ='solid')
plt.legend(fieldnames)
plt.savefig(str(path) + 'server_stats.png')
