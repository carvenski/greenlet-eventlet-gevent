from gevent import monkey; monkey.patch_all() #must do patch to repace socket in python otherwise gevent has no effect !!
# import gevent
from gevent import pool
import requests
from datetime import datetime

def f(url):
    print '----visit url: %s----' % url
    r = requests.get(url)
    print '----result length: %s----' % len(r.content)
    return 0
    
start = datetime.now()

# greenlets = [gevent.spawn(f, 'https://github.com/yxzoro') for i in range(100)]
# gevent.joinall(greenlets)

urls = ['https://github.com/yxzoro'] * 100
p = pool.Pool(100)
result = p.map(f, urls)  #result of the function in every greenlet !!

print result  #get result of the function in every greenlet !!

print '-'*40 + 'spent time' + '-'*40
print datetime.now() - start

