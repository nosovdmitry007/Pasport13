import time
import os
from oblasty import oblasty
#Производим детекцию с помощью YOLO4
from memory_profiler import profile
# @profile()
def yolo(put,out):
    start_time_y = time.time()
    os.system(f'./darknet/darknet detector test darknet/data/obj.data darknet/cfg/yolov4-obj.cfg yolov4-obj_last.weights {put} -thresh 0.3'
              f' -ext_output -dont_show -out result.txt > {out}')
    print("--- %s seconds yolo ---" % (time.time() - start_time_y))
    oblasty(out,put) #запускаем вырезание областей с последующим распознанием
