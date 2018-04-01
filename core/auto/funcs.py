import inspect
class curry:
    def __init__(self, curry, fn):
        self.curry = list(curry)
        self.fn = fn

    def __str__(self):
        return "<function with curry>"
    __repr__ = __str__


class flat_fn:
    def __init__(self):
        self.pairs = []

    def append(self, point):
        self.pairs.append(point)

    def __str__(self):
        return '<function>'
    __repr__ = __str__


def get_fn(fn, perams):
    perams = list(perams)
    if isinstance(fn, curry):
        perams = fn.curry + perams
        fn = fn.fn
    elif isinstance(fn, flat_fn):
        fn = fn.pairs
    if callable(fn):
        return get_py_fn(fn,perams)
    # print(perams)
    best = None
    max = 0
    default = None
    if isinstance(fn, dict):
        fn = fn['fn']
    # print(fn)
    alt = []
    for can in fn:
        mats = 0
        kats = 0
        ps = can[0]
        if len(ps) != len(perams):
            continue
        for pl, i in enumerate(ps):
            i = i.split('_')
            if i[0] != 'name':
                if i[1] == str(perams[pl]):
                    mats += 1
            else:
                kats += 1
        if kats == len(perams):
            alt = [can[1]] + alt
            default = can[1]
        if max < mats:
            max = mats
            best = can[1]
    # print(best)
    best = best if best != None else default
    if best == None:
        best = []
        max = 0
        default = None
        if isinstance(fn, dict):
            fn = fn['fn']
        # print(fn)
        alt = []
        for can in fn:
            mats = 0
            kats = 0
            ps = can[0]
            ps = ps[:len(perams)]
            for pl, i in enumerate(ps):
                i = i.split('_')
                if i[0] != 'name':
                    if i[1] == str(perams[pl]):
                        mats += 1
                else:
                    kats += 1
            if kats == len(perams):
                alt = [can[1]] + alt
                default = can[1]
            if max <= mats:
                max = mats
                best.append(can)
        ret = curry(perams, best)
        return ret
    return [best, perams]


def get_py_fn(fn,perams):
    perams = list(perams)
    if isinstance(fn, curry):
        perams = fn.curry + perams
        fn = fn.fn
    ins = inspect.getargspec(fn)
    maxi = len(ins.args)
    if ins.varargs != None:
        if maxi <= len(perams):
            return fn(*perams)
    if maxi == len(perams):
        return fn(*perams)
    if maxi > len(perams):
        return curry(perams,fn)
    print('no candidate function')
    exit()

def i_ret(val):
    # return
    global hold
    global s_vs
    global vs
    global s_hold
    global calls
    global line
    global rets
    got = hold[val]
    vs = s_vs[-1]
    hold = s_hold[-1]
    s_vs = s_vs[:-1]
    s_hold = s_hold[:-1]
    line = calls[-1]
    hold[rets[-1]] = got
    rets = rets[:-1]
    calls = calls[:-1]


def i_call(into, fn):
    global hold
    global s_vs
    global vs
    global s_hold
    global calls
    global rets
    global perams
    global line
    if not callable(hold[fn]):
        got = get_fn(hold[fn], perams)
        if isinstance(got, list):
            s_vs.append(vs)
            s_hold.append(hold)
            calls.append(line)
            rets.append(into)
            hold[fn] = got[0]
            line = hold[fn]
            vs = {}
            hold = {}
            for pl, i in enumerate(got[1]):
                hold[pl + 1] = i
        else:
            hold[into] = got
    else:
        hold[into] = get_py_fn(hold[fn],perams)
