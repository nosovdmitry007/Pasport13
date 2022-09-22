import os
from automaticfilter import auto_rotait
from yolo import yolo

puti = os.listdir('baza/test')
for fn in puti:
    print(fn)
    put = 'baza/test/'+fn
    # out = 'test.txt'
    out = 'test_obl/'+ fn.split('.')[0] + '.txt'
    # auto_rotait(put,out)
    yolo(put,out)

# print(len(puti))
