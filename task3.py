import psutil,datetime,json,schedule,time,configparser


'''
● Overall CPU load
● Overall memory usage
● Overall virtual memory usage
● IO information
● Network information

'''
config = configparser.ConfigParser()
config.read('config')
output_type = config.get('common', 'output')
interval = config.get('common', 'interval')

def b2h(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

tf='%Y-%m-%d_%H:%M:%S'
cpu_time = psutil.cpu_percent(percpu=True)
mem_usage=psutil.Process().memory_percent().__round__(2)
virtual_mem = psutil.virtual_memory()[2]
io = psutil.disk_io_counters(perdisk=False)[2:4]
io1=b2h(io[0])
io2=b2h(io[1])
network = psutil.net_io_counters(pernic=False)[0:2]
net1=b2h(network[0])
net2=b2h(network[1])

print("cpu time: ", cpu_time)
print("Overal_mem_usage: ", mem_usage)
print("virt_mem_usage: ", virtual_mem)
print("disk_usage: ", io)
print("network_usage: ", network)
sn_number=0
def write_stat_to_txt():
    global sn_number
    with open("txt.log", "a") as txt_log:
        txt_log.write("Snapshot {}:{}:\n".format(sn_number, datetime.datetime.now().strftime(tf)))
        txt_log.write("Overall CPU load by cores % : {} \n".format(cpu_time))
        txt_log.write("Overall memory usage : {} % \n".format(mem_usage))
        txt_log.write("Overall virtual memory usage : {} % \n".format(virtual_mem))
        txt_log.write("IO information : read_Mbytes = {}, write_Mbytes = {}\n".format(io1, io2))
        txt_log.write("Network information : Mbytes_sends = {} , Mbytes_received = {}%\n".format(net1, net2))
        txt_log.close()
    sn_number+=1


def write_stat_to_json():
    global sn_number
    data = {
        "Overall CPU load by cores % " : cpu_time,
        "Overall memory usage %": mem_usage,
        "Overall virtual memory usage %": virtual_mem,
        "IO information , read ,write to disk ": [io1, io2],
        "Nework information Mbytes_sends, Mbytes_received": [net1, net2 ]
    }

    fdata = ['SNAPSHOT ' + str(sn_number) + ': ' + str(datetime.datetime.now().strftime(tf)), data]

    with open('stat_log.json', 'a+') as log_json:
        json.dump(fdata, log_json, indent=4, sort_keys=True)
    sn_number+=1

def ch_type():
    if output_type == 'txt':
        write_stat_to_txt()
       # schedule.every(int(interval)).seconds.do(write_stat_to_txt)
    elif output_type == 'json':
        write_stat_to_json()
        #schedule.every(int(interval)).seconds.do(write_stat_to_json)

schedule.every(int(interval)).seconds.do(ch_type)
while True:
    schedule.run_pending()









