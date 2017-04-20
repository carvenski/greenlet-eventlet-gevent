
## use gevent to improve concurrent task !! 
## use gevent's Greenlet to run mysql update task 10000 records each Greenlet.
from gevent import monkey; monkey.patch_all()
import umysql  ## must use `umysql` cause only it support gevent's monkey_patch !!
from gevent import pool
import time

def get_con():
    con = umysql.Connection()
    con.connect('localhost', 3306, 'test', 'test', 'test', True)
    return con

def get_all():
    con = get_con()
    sql = '''select count(*) from B '''
    count = con.query(sql).rows[0][0]
    print count
    return count

def f(i):
    print '---------------- start in greenlet----------------------'
    con = get_con()
    sql1 = '''select id from B limit {}, 10000; '''.format(i)
    r = con.query(sql1).rows
    ids = map(lambda i: i[0].encode('utf-8'), r)
    sql2 = '''update B set test2=CONCAT(test2, '/test2/') where id in ({});'''.format( str(ids)[1:-1] ) 
    r = con.query(sql2)
    print '---------success---------result:', str(r), '--------'

s = time.time()
args = xrange(0, get_all(), 10000)
p = pool.Pool(16)
p.map(f, args)
print '-------------------time:', str(time.time()-s), '-----------------'




