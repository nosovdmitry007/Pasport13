from automaticfilter import auto_rotait
from yolo import yolo
import tracemalloc
import time
#Тест производительности
tracemalloc.start()
start_time = time.time()


put ='photo/10012.jpg'
out = 'test.txt'
# auto_rotait(put,out)
yolo(put,out)

print("--- %s seconds ---" % (time.time() - start_time))
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**3}KB; Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
tracemalloc.stop()

