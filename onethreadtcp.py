import threading
from socket import *
import time
from tqdm import tqdm                                 # 进度条，可自行加上
from multiping import MultiPing

lock = threading.Lock()                     # 确保多个线程在共享资源的时候不会出现脏数据
openNum=0                                   # 端口开放数量统计
open_ports = []                             # 记录打开的端口号
 
def tcpScan(host,port):
    global openNum
    try:
        s=socket(AF_INET,SOCK_STREAM)       # TCP 测试
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        open_ports.append(port)
        lock.release()
        s.close()
    except:
        pass

def scan(ip,ports=range(65535)):            # 设置 端口缺省值0-65535
    setdefaulttimeout(1)
    for port in tqdm(ports):
        tcpScan(ip,port)
    print(f"PortScan is Finish ，OpenNum is {openNum}")
    print(f"Open ports: {open_ports}")

if __name__ == '__main__':
    ips = []
    for i in range(255):
        ips.append("192.168.1."+str(i))

    mp = MultiPing(ips)

    mp.send()

    responses, no_responses = mp.receive(1)

    print("unreachable: "+str(no_responses))
    for ip in responses.items():
        print("alive: "+str(ip[0]))
        ip = ip[0]
        t1 = time.time()
        scan(ip, range(200))  # 全端口扫描
        runtime = time.time() - t1
        print("time:" + str(runtime) + "s")
    # ip = "127.0.0.1"
    # t1 = time.time()
    # scan(ip, range(200))  # 全端口扫描
    # runtime = time.time() - t1
    # print("scan-ports time:" + str(runtime) + "s")
