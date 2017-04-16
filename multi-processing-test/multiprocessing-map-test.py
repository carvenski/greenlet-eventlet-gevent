import multiprocessing
import time

def f(data):
    return (data**10 + data**5 + data*1000) / 3 * (data**3 + data**4 + data*100)*4 + (data**3 + data**4 + data*100)*(data**3 - data%23)

def start_process():
    print 'Starting', multiprocessing.current_process().name

if __name__ =='__main__':
    inputs = list(range(100))
    start = time.time()
    
    # use process pool:
    pool_size = multiprocessing.cpu_count() * 2; print pool_size
    pool = multiprocessing.Pool(processes=pool_size, initializer=start_process)

    pool_outputs = pool.map(f, inputs)
    
    pool.close()
    pool.join()

    print 'Pool  :', pool_outputs
    print '----spent time: ', time.time() - start
