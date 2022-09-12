from automaticfilter import auto_rotait
import time
from functools import wraps

put ='photo/0001.jpg'
out = 'test.txt'


def fn_timer(function):
  @wraps(function)
  def function_timer(*args, **kwargs):
    t0 = time.time()
    result = function(*args, **kwargs)
    t1 = time.time()
    print ("Total time running %s: %s seconds" %
        (function.func_name, str(t1-t0))
        )
    return result
  return function_timer

@fn_timer
def start():
    auto_rotait(put,out)

start()
