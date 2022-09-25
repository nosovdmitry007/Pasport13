import time
from memory_profiler import profile
from yolo_4 import yolo_4
from yolo import yolo
put ='baza/test/20195.jpg'

out = 'test.txt'
@profile()
def start(put):
    start_time_y = time.time()
    yolo(put,out)
    print("--- %s seconds all---" % (time.time() - start_time_y))

start(put)

