import os
from automaticfilter import auto_rotait
from yolo import yolo

nebrat = ''#'10167 10191 10092 10188 10125 10134 10148 ' \
         #'10211 10145 10168 10142 10098 10084 10240 10225 10200 10046 10129 10056 10190 10184 ' \
         #'10245 10234 10045 10176 10088 10244 10223 10212 10051'

puti = os.listdir('baza')
for fn in puti:
    if fn.split('.')[0] not in nebrat:
        put = 'baza/'+fn
        out = 'test.txt'
        # out = 'test_obl/'+ fn.split('.')[0] + '.txt'
        # auto_rotait(put,out)
        yolo(put,out)
print(len(puti))
