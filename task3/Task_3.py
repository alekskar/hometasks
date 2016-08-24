import psutil
import datetime
import json
import schedule
import configparser
import sys

"""
This script gather some information from system:
● Overall CPU load
● Overall memory usage
● Overall virtual memory usage
● IO information
● Network information

"""


config = configparser.ConfigParser()
config.read('config')
output_type = config.get('common', 'output')
interval = config.get('common', 'interval')

# human readable format


def b2h(n):

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


tf = '%Y-%m-%d_%H:%M:%S'
cpu_time = psutil.cpu_percent(percpu=True)

# memory information

mem_usage = psutil.Process().memory_percent().__round__(2)
virtual_mem = psutil.virtual_memory().percent

# io information

io_read_bytes = b2h(psutil.disk_io_counters(perdisk=False).read_bytes)
io_write_bytes = b2h(psutil.disk_io_counters(perdisk=False).write_bytes)

# network information

net_Mb_sent = b2h(psutil.net_io_counters(pernic=False).bytes_sent)
net_Mb_received = b2h(psutil.net_io_counters(pernic=False).bytes_recv)

sn_number = 0


def write_stat_to_txt():
    global sn_number
    with open("txt.log", "a") as txt_log:
        txt_log.write("Snapshot {}:{}:\n".format(
            sn_number, datetime.datetime.now().strftime(tf)))
        txt_log.write("Overall CPU load by cores % : {} \n".format(cpu_time))
        txt_log.write("Overall memory usage : {} % \n".format(mem_usage))
        txt_log.write(
            "Overall virtual memory usage : {} % \n".format(virtual_mem))
        txt_log.write("IO information : read_Mbs = {}, write_Mbs = {}\n".format(
            io_read_bytes, io_write_bytes))
        txt_log.write("Network information : Mb_sends = {} , Mb_received = {}%\n".format(
            net_Mb_sent, net_Mb_received))

    sn_number += 1

# writing data to json file


def write_stat_to_json():
    global sn_number
    data = {
        "Overall CPU load by cores % ": cpu_time,
        "Overall memory usage %": mem_usage,
        "Overall virtual memory usage %": virtual_mem,
        "IO information , read ,write to disk ": [io_read_bytes, io_write_bytes],
        "Network information Mb_sends, Mb_received": [net_Mb_sent, net_Mb_received]
    }

    f_data = ['SNAPSHOT ' + str(sn_number) + ': ' +
              str(datetime.datetime.now().strftime(tf)), data]

    with open('stat_log.json', 'a+') as log_json:
        json.dump(f_data, log_json, indent=4, sort_keys=True)
    sn_number += 1

# define output file to process:


def ch_type():
    if output_type == 'txt':
        write_stat_to_txt()
       # schedule.every(int(interval)).seconds.do(write_stat_to_txt)
    elif output_type == 'json':
        write_stat_to_json()
        # schedule.every(int(interval)).seconds.do(write_stat_to_json)
    else:
        sys.exit()

schedule.every(int(interval)).seconds.do(ch_type)
while True:
    schedule.run_pending()