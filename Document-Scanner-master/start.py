import time
from memory_profiler import profile
from yolo_4 import yolo_4
put ='baza/test/20133.jpg'
@profile()

def start(put):
    start_time_y = time.time()
    yolo_4(put)
    print("--- %s seconds all---" % (time.time() - start_time_y))

start(put)

