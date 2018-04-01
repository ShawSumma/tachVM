import time
import math
global vs
global funcs
global hold
global s_hold
global s_vs
global calls
global rets
global perams
global line
vs = {}
def i_map(x,y):
    ret = []
    for i in y:
        ret.append(get_py_fn(x,[i]))
    return ret
def i_apply(x,y):
    ret = []
    for f,i in zip(x,y):
        ret.append(get_py_fn(f,[i]))
    return ret
def i_filter(x,y):
    ret = []
    for i in y:
        if get_py_fn(x,i):
            ret.append(i)
    return ret
def i_fold(x,y):
    ret = []
    for i in y:
        if get_py_fn(x,i):
            ret.append(i)
    return ret
funcs = {
    'print': print,
    'uxtime': time.time,
    'delay': time.sleep,
    'int': int,
    'float': float,
    'false': 0,
    'true': 1,
    'list': lambda *perams: perams,
    'add' : lambda x,y : x+y,
    'sub' : lambda x,y : x-y,
    'mul' : lambda x,y : x*y,
    'div' : lambda x,y : x/y,
    'mod' : lambda x,y : x%y,
    'pow' : lambda x,y : x**y,
    'input' : input,
    'map' : i_map,
    'filter' : i_filter,
    'apply' : i_apply,
    'fold' : i_apply,
}
math_vs = {**vars(math)}#,**vars(time)}
for i in math_vs:
    if callable(math_vs[i]):
        funcs[i] = math_vs[i]
    elif isinstance(math_vs[i],int) or isinstance(math_vs[i],float):
        funcs[i] = math_vs[i]
