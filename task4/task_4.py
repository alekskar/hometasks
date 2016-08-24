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


def b2h(n):
    """ returns bytes to human readable format """

    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class CollectedData:

    """ define data to collect from system """

    sn_number = 0

    def __init__(self):

        self.tf = '%Y-%m-%d_%H:%M:%S'
        self.cpu_time = psutil.cpu_percent(percpu=True)

        # memory information

        self.mem_usage = psutil.Process().memory_percent()
        self.virtual_mem = psutil.virtual_memory().percent

        # io information

        self.io_read_bytes = b2h(
            psutil.disk_io_counters(perdisk=False).read_bytes)
        self.io_write_bytes = b2h(
            psutil.disk_io_counters(perdisk=False).write_bytes)

        # network information

        self.net_Mb_sent = b2h(psutil.net_io_counters(pernic=False).bytes_sent)
        self.net_Mb_received = b2h(
            psutil.net_io_counters(pernic=False).bytes_recv)


class ExportToFormat(CollectedData):

    """ this class exports collected data to chosen format """

    def export(self, output_format):

        if output_format == 'txt':

            with open("log.txt", "a") as txt_log:
                txt_log.write("Snapshot {}:{}:\n".format(
                    CollectedData.sn_number, datetime.datetime.now().strftime(self.tf)))
                txt_log.write(
                    "Overall CPU load by cores % : {} \n".format(self.cpu_time))
                txt_log.write("Overall memory usage : {} % \n".format(
                    self.mem_usage.__round__(2)))
                txt_log.write(
                    "Overall virtual memory usage : {} % \n".format(self.virtual_mem))
                txt_log.write("IO information : read_Mb = {}, write_Mbytes = {}\n".format(
                    self.io_read_bytes, self.io_write_bytes))
                txt_log.write("Network information : Mb_sends = {} , Mb_received = {}%\n".format(
                    self.net_Mb_sent, self.net_Mb_received))

            CollectedData.sn_number += 1

        elif output_format == 'json':
            data = {
                "Overall CPU load by cores % ": self.cpu_time,
                "Overall memory usage %": self.mem_usage.__round__(2),
                "Overall virtual memory usage %": self.virtual_mem,
                "IO information , read ,write to disk ": [self.io_read_bytes, self.io_read_bytes],
                "Network information Mb_sends, Mb_received": [self.net_Mb_sent, self.net_Mb_received]
            }

            f_data = ['SNAPSHOT ' + str(CollectedData.sn_number) + ': ' + str(
                datetime.datetime.now().strftime(self.tf)), data]

            with open('stat_log.json', 'a+') as log_json:
                json.dump(f_data, log_json, indent=4, sort_keys=True)
            CollectedData.sn_number += 1

        else:
            sys.exit()


def run():
    sys_snap = ExportToFormat()
    sys_snap.export(output_type)


schedule.every(int(interval)).seconds.do(run)
while True:
    schedule.run_pending()
