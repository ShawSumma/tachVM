from importlib.machinery import SourceFileLoader
import importlib
from config import tach_path


def py(path):
    ret = path
    for i in tach_path.tachp:
        if path.startswith(i):
            ret = tach_path.tachp[i] + path[len(i):]
            break
    return ret


def tach(path):
    ret = path
    for i in tach_path.tachp:
        if path.startswith(i):
            ret = tach_path.tachp[i] + path[len(i):]
            ret += '.ion'
    return ret


def imp(f):
    f = py(f)+'.py'
    ext = SourceFileLoader('extern', f).load_module()
    return ext

def pys_std(f):
    return importlib.import_module(f)
