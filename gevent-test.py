from gevent import monkey; monkey.patch_all()
import gevent
import requests
from datetime import datetime

def f(url):
    print '----visit url: %s----' % url
    r = requests.get(url)
    print '----result length: %s----' % len(r.content)

start = datetime.now()

greenlets = [gevent.spawn(f, 'https://github.com/yxzoro') for i in range(100)]

gevent.joinall(greenlets)

print '-'*40 + 'spent time' + '-'*40
print datetime.now() - start

