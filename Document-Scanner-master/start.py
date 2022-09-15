from automaticfilter import auto_rotait
put ='photo/0001.jpg'
out = 'test.txt'
from memory_profiler import profile
@profile()
def start():
    auto_rotait(put,out)

start()
