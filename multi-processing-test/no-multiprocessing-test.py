import multiprocessing
import time

def f(data):
    return (data**10 + data**5 + data*1000) / 3 * (data**3 + data**4 + data*100)*4 + (data**3 + data**4 + data*100)*(data**3 - data%23)

if __name__ =='__main__':
    inputs = list(range(100))
    start = time.time()

    outputs = map(f, inputs)
    
    print 'Pool  :', outputs
    print '----spent time: ', time.time() - start
