# encoding=utf-8

from gevent import monkey; monkey.patch_all()
from gevent import pool
import time
import traceback

# from Utilities.movoto.SqlHelper import SqlHelper
import umysql  # umysql support gevent

def get_conn():
	con = umysql.Connection() 
	# host, port, username, password, database, autocommit
	con.connect('db3.ng.movoto.net', 3306, 'movoto','movoto123!', 'movoto', True)
	return con

def decorator(f):
    def wrapper(*args, **kw):
        s = time.time()
        f(*args, **kw)
        print '-----------------[spent time]: %s---------------' % str(time.time()-s)
    return wrapper

def get_total_count():
	sql = ''' 
		SELECT COUNT(*)
		FROM  mls_public_record_association as a 
		INNER JOIN mls_listing as b ON a.primary_listing_id=b.id 
		INNER JOIN address as d ON d.id=b.mls_address_id 
		INNER JOIN attribute as c ON b.standard_status=c.id 
		WHERE (c.name='ACTIVE' or c.name='PENDING') and d.state NOT in ('FL', 'TN', 'IL', 'MD', 'WA', 'MI') and a.url NOT LIKE '%/for-sale/';
	'''

	con = get_conn()
	total_count = con.query(sql).rows[0][0]
	print '----------------[total] url conut: %d-------------------' % total_count

	return total_count

def update_url_batch(start):  # update 10000 records once in a coroutine
	try:
		coroutine_id = start/10000
		print '---------------------[start] fix url in coroutine: %d-----------------' % coroutine_id
		sql1 = ''' 
		SELECT a.id
		FROM  mls_public_record_association as a 
		INNER JOIN mls_listing as b ON a.primary_listing_id=b.id 
   		INNER JOIN address as d ON d.id=b.mls_address_id 
		INNER JOIN attribute as c ON b.standard_status=c.id
		WHERE  (c.name='ACTIVE' or c.name='PENDING') and d.state NOT in ('FL', 'TN', 'IL', 'MD', 'WA', 'MI') and a.url NOT LIKE '%/for-sale/' 
    		limit {0},{1};
		'''.format(start, 10000)

		con = get_conn()				
		resultSet = con.query(sql1).rows
		id_list = map(lambda row: row[0].encode('utf-8'), resultSet) # remove u'

		sql2 = '''
         		UPDATE mls_public_record_association 
			SET url=replace(concat(url, '/for-sale/'), '//', '/')  # incase url already has / in end
			WHERE id in ({0});
			'''.format(str(id_list)[1:-1])
		con.query(sql2)
		print '-------[end] fix: %d url in coroutine: %d----------' % (len(id_list), coroutine_id)
	except Exception:
		print '----------------------[Exception] in sql in coroutine: %d-----------------' % coroutine_id
		print traceback.print_exc()

#use gevent pool:
@decorator
def main():
	total_count = get_total_count()
	args = xrange(0, total_count, 10000)

	pool_size = 20  # pool_size = total_count/10000
	p = pool.Pool(pool_size)
	p.map(update_url_batch, args)

if __name__ == '__main__':
	main()

# sql INNER JOIN's query condition --> after ON or WHERE:
'''
SELECT a.id
FROM  mls_public_record_association as a 
INNER JOIN mls_listing as b ON a.primary_listing_id=b.id 
INNER JOIN attribute as c ON b.standard_status=c.id 
WHERE (c.name='ACTIVE' or c.name='PENDING') and a.url NOT LIKE '%/for-sale/' limit 0,10000;
# (c.name='ACTIVE' or c.name='PENDING') must have () !!!!
#or c.name in ('ACTIVE', 'PENDING') 

SELECT a.id
FROM  mls_public_record_association as a 
INNER JOIN mls_listing as b ON a.primary_listing_id=b.id and a.url NOT LIKE '%/for-sale/'
INNER JOIN attribute as c ON b.standard_status=c.id and c.name in ('ACTIVE', 'PENDING')
limit {0},{1};
'''


