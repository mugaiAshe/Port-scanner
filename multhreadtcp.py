import threading
from socket import *
import time
from tqdm import tqdm                                 # 进度条
from multiping import MultiPing
 
lock = threading.Lock()                     # 确保 多个线程在共享资源的时候不会出现脏数据
openNum=0                                   # 端口开放数量统计
threads=[]                                  # 线程池
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
        t = threading.Thread(target=tcpScan,args=(ip,port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"PortScan is Finish ，OpenNum is {openNum}")
    print(f"Open ports: {open_ports}")
 
if __name__ == '__main__':
    ips = []
    for i in range(256):
        ips.append("192.168.1."+str(i)) #检测192.168.1.0/24

    t0 = time.time()
    mp = MultiPing(ips) # 创建一个MultiPing对象来测试
    mp.send()# 发送ping
    responses, no_responses = mp.receive(1) # 超时设置为1秒, 等待回答
    runtime = time.time() - t0
    print("scan-ips time:" + str(runtime) + "s")
    print("unreachable: "+str(no_responses))
    #
    for ip in responses.items():
        print("alive: "+str(ip[0]))
        ip = ip[0]
        t1 = time.time()
        scan(ip,range(1000))  # 全端口扫描
        runtime = time.time() - t1
        print("scan-ports time:" + str(runtime) + "s")

    # ip = "127.0.0.1"
    # t1 = time.time()
    # scan(ip,range(200))  # 全端口扫描
    # runtime = time.time() - t1
    # print("scan-ports time:" + str(runtime) + "s")