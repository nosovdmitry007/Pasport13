import os

fn = 'photo/10000.jpg'
put = fn
out = 'test.txt'
os.system(
    f'darknet/darknet detector test data/obj.data data/yolov4-obj.cfg data/backup/yolov4-obj_last.weights" {put} -thresh 0.5 -ext_output -dont_show -out result.txt > {out}')

# os.system("darknet/darknet detector test data/obj.data data/yolov4-obj.cfg data/backup/yolov4-obj_last.weights" + '"./test1.jpg"' + " -dont_show -ext_output | tee pred.txt")
