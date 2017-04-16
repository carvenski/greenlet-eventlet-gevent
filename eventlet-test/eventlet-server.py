#encoding=utf-8
#import eventlet
#from eventlet.green import socket
from gevent import socket
import gevent
import requests

def http_handler(data):  # writer, reader == req, res
        r = requests.get('https://github.com/yxzoro')
        print data
	return

def main():
	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
	    sock.bind(('0.0.0.0', 3000))
	    print 'Server started!'
	    while True:
			data, addr = sock.recvfrom(8024)
                        greenlet = gevent.spawn(http_handler, data)
		        gevent.joinall(greenlet)
	except KeyboardInterrupt:
		pass
	return

if __name__=='__main__':
	main()


