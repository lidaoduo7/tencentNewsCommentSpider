# -*- coding: utf-8 -*-



s = "一定是不还钱"
print(s.encode('utf-8'))

import datetime
now_time = datetime.datetime.now()
print(now_time)
format_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(format_time)


import socket
hostname = socket.gethostname()
print(hostname)

ip_addr = socket.gethostbyname(hostname)
print(ip_addr)