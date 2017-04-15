import requests
from datetime import datetime


def f(url):
    print '----visit url: %s----' % url
    r = requests.get(url)
    print '----result length: %s----' % len(r.content)

start = datetime.now()
    
urls = ['https://github.com/yxzoro' for i in range(100)]

start = datetime.now()

for url in urls:
    f(url)

print '-'*40 + 'spent time' + '-'*40    
print datetime.now() - start

