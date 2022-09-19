from automaticfilter import auto_rotait
from yolo import yolo
import time
from memory_profiler import profile
put ='baza/20017.jpg'
@profile()

def start(put):
    out = 'test.txt'
    start_time_y = time.time()
    # auto_rotait(put,out)
    yolo(put,out)
    print("--- %s seconds all---" % (time.time() - start_time_y))
start(put)
