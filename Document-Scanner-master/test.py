import os
put ='photo/0000.jpg'
out = 'test.txt'
os.system(f'./darknet/darknet detector test darknet/data/obj.data darknet/cfg/yolov4-obj.cfg yolov4-obj_last.weights {put} -thresh 0.3 -ext_output -dont_show -out result.txt > {out}')
