
import re
cidr = [
 '1.1.1.1', '2.2.2.2']

def ip2cidr(ip):
    ipset = set()
    ipset.add(re.findall('\\d+?\\.\\d+?\\.\\d+?\\.', ip)[0] + '0/24')
    iplists = list(ipset)
    iplists.sort()
    return iplists


def saveContext(s):
    n=0
    ips=set()
    wfile = open('./cidr.txt', 'w')
    for i in s:
        ips.add(i[0])
    for ip in ips:
        n=n+1
        wfile.write(ip + '\n')
    else:
        wfile.close()
    return n,ips

if __name__ == '__main__':
    iplist = ip2cidr(cidr)
    saveContext(iplist)

