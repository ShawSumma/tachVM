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
funcs = {
    'print': print,
    'uxtime': time.time,
    'delay': time.sleep,
    'int': int,
    'float': float,
    'false': 0,
    'true': 1,
    'list': lambda *perams: list(perams)
}
math_vs = {**vars(math)}#,**vars(time)}
for i in math_vs:
    if callable(math_vs[i]):
        funcs[i] = math_vs[i]
    elif isinstance(math_vs[i],int) or isinstance(math_vs[i],float):
        funcs[i] = math_vs[i]
