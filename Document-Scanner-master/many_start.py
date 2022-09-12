import os

from yolo import yolo

nebrat = '10167 10191 10188 10125 10134 10148'
puti = os.listdir('photo')
for fn in puti:
    if fn.split('.')[0] not in nebrat:
        put = 'photo/'+fn
        out = 'test_obl/'+ fn.split('.')[0] + '.txt'

        yolo(put,out)
