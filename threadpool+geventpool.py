#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
sys.path.append('..')

from multiprocessing.dummy import Pool as ThreadPool
from gevent import monkey; monkey.patch_all()
from gevent import pool as gevent_pool
import requests


def x(url):
    print 'thread--' + url + 'is starting'
    j = 0
    while j<10:
        print 'thread--' + url + 'is working'
        j += 1
        urls = ['http://github.com/yxzoro' for i in xrange(5)]
        p = gevent_pool.Pool(5)
        p.map(requests.get, urls)



def main():
    urls = [str(i) for i in xrange(5)]

    pool = ThreadPool(5)
    pool.map(x, urls)

    pool.close() 
    pool.join()

main()


