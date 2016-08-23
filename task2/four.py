from collections import Counter
log = open('./access_log.txt')
ip_dict={}
for line in log:
    ip=line.split(" -")
    ip=(ip[0])
    ip_dict[ip] = ip_dict.get(ip,0) +1
print(dict(Counter(ip_dict).most_common(10)))




