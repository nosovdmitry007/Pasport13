from automaticfilter import auto_rotait
from yolo import yolo
import tracemalloc
import time
# mprof run <executable>
import cv2

#Тест производительности
tracemalloc.start()
start_time = time.time()


put ='10251.jpg'
out = 'test.txt'
# stackedImage = cv2.imread(put)
# cv2.imshow('Result', stackedImage)
# auto_rotait(put,out)
# @profile
yolo(put,out)

print("--- %s seconds ---" % (time.time() - start_time))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**3}KB; Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
tracemalloc.stop()

