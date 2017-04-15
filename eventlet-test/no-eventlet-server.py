#encoding=utf-8
import eventlet
import socket
import requests

def http_handler(writer, reader):  # writer, reader == req, res
	req=''
	while True:
		chunk=reader.readline()
		if not chunk:
			break
		req += chunk
		if chunk=='\r\n':  # end of one http request, last line == '\r\n'
			break
        r = requests.get('http://news.baidu.com')
	response = 'Hello world! here is response data from server...\r\n'
	writer.write('HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (len(response), response))
	writer.close(); reader.close()
	return

def main():
	try:
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
	    sock.bind(('0.0.0.0', 3000))
	    sock.listen(1)
	    print 'Server started!'
	    while True:
			conn, addr = sock.accept()
			writer = conn.makefile('w')   
			reader = conn.makefile('r')   
                        http_handler(writer, reader)
	except KeyboardInterrupt:
		pass
	return

if __name__=='__main__':
	main()


