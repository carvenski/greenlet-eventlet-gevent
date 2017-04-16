from gevent import monkey; monkey.patch_all() #must do patch to repace socket in python otherwise gevent has no effect !!
import gevent
import requests
from datetime import datetime

def f(url):
    print '----visit url: %s----' % url
    r = requests.get(url)
    print '----result length: %s----' % len(r.content)
    return 0

start = datetime.now()

greenlets = [gevent.spawn(f, 'https://github.com/yxzoro') for i in range(100)]

gevent.joinall(greenlets)

print [greenlet.value for greenlet in greenlets]  #use greenlet.value to get result of the function in this greenlet !!


print '-'*40 + 'spent time' + '-'*40
print datetime.now() - start

