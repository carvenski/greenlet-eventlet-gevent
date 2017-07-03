

import sys
import socket
import time
import gevent
 
from gevent import socket,monkey
monkey.patch_all()
 
def server(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli)
 
def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            print("recv:", data)
            conn.send(data)
            if not data:
                conn.shutdown(socket.SHUT_WR)
 
    except Exception as  ex:
        print(ex)
    finally:
        conn.close()

if __name__ == '__main__':
    server(9999)

    
## there are maybe thousands of client in concurrency:
 1 import socket
 2  
 3 HOST = 'localhost'    # The remote host
 4 PORT = 9999         # The same port as used by the server
 5 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 6 s.connect((HOST, PORT))
 7 while True:
 8     msg = bytes(input(">>:"),encoding="utf8")
 9     s.sendall(msg)
10     data = s.recv(1024)
11     #print(data)
12  
13     print('Received', repr(data))
14 s.close()

