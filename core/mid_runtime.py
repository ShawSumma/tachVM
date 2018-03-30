import time
import extern
import threading

def seths(name, val, hname):
    global hs
    hs[hname][int(name[1:])] = val


def setvs(name, val, hname):
    global vs
    if name in vs[hname]:
        #print('immutable error on ', name)
        #exit()
        pass
    if not type(name) in [type(str), type(int), type(float), type(tuple), type(list)]:
        fs[hname][name] = val
    if name != 'del':
        vs[hname][name] = val


def load_bui(hname):
    global hs, vs, fs
    vs[hname] = {'true':1,'false':0}


def get(name, hname):
    if name[0] == '%':
        return hs[hname][int(name[1:])]
    elif name == '-':
        return None
    else:
        if name[1:] in vs[hname]:
            return vs[hname][name[1:]]
        elif name[1:] in fs[hname]:
            return fs[hname][name[1:]]
        elif name[1:] in bs:
            return name[1:]
        elif name in bs:
            return name
        print('unkown ->', name, list(fs[hname]))
        exit()


def get_fn(fn, perams):
    best = None
    max = 0
    default = None
    if isinstance(fn, dict):
        fn = fn['fn']
    # print(fn)
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
            default = can[1]
        if max < mats:
            max = mats
            best = can[1]
    # print(best)
    best = best if best != None else default
    if best == None:
        print('no candidate function')
        print(perams)
        exit()
    return best


def oo_get(a, b):
    ret = vars(a)[b]
    return ret


def run(bytecode, name, place=0):
    #print('\t',place)
    load_bui(name)
    global hs_h
    global vs_h
    global vs
    global hs
    global fs
    global rets
    global ops
    if len(bytecode) == 0:
        return
    split = bytecode.split('\n')
    loops = 0
    tot = 0
    threads = 0
    points = {}
    calls = []
    callrets = []
    perams = []
    ons = 0
    hotspot = [0]*len(split)
    while place < len(split):
        hotspot[place] += 1
        cur = split[place].split()
        #print(split[place])
        #print('\t\t\t\t',list(hs))
        if len(cur) < 1:
            place += 1
            continue
        if cur[0] == 'op':
            a, b = get(cur[3], name), get(cur[4], name)
            op = cur[1]
            res = ops[op](a,b)
            #print('-- op',cur[1],res,a,b,'--')
            #print('\t\t\t\top :',place,'  ',cur[1],'with',[a,b])
            seths(cur[2], res, name)
        elif cur[0] == 'int':
            seths(cur[1], int(cur[2]), name)
        elif cur[0] == 'float':
            seths(cur[1], float(cur[2]), name)
        elif cur[0] == 'str':
            re = split[place][5+len(cur[1]):]
            seths(cur[1], re, name)
        elif cur[0] == 'set':
            setvs(cur[1], get(cur[2], name), name)
        elif cur[0] == 'load':
            seths(cur[1], get(cur[2], name), name)
        elif cur[0] == 'def':
            if not cur[1] in fs[name]:
                fs[name][cur[1]] = {'type': 'fn', 'fn': []}
            fs[name][cur[1]]['fn'].append([cur[2:-1], place])
            place += int(cur[-1])
        elif cur[0] == 'return':
            got = get(cur[1], name)
            vs[name] = vs_h[-1]
            hs[name] = hs_h[-1]
            vs_h = vs_h[:-1]
            hs_h = hs_h[:-1]
            perams = []
            seths(callrets[-1], got, name)
            #print('\t\t',callrets[-1],'<-',got)
            place = calls[-1]
            calls = calls[:-1]
            callrets = callrets[:-1]
            #print(got)
            #print('\t\t\t\tre :',place,'   # from',got)
            ons -= 1
        elif cur[0] == 'perams':
            perams = []
            for i in cur[1:]:
                perams.append(get(i, name))
        elif cur[0] == 'call':
            ons += 1
            cur[2] = get(cur[2], name)
            #print('\t\t\t\ton :',place,'   ? with',perams)
            if cur[2] not in bs and not isinstance(cur[2], str):
                fn = cur[2]
                if callable(fn):
                    seths(cur[1], fn(*perams), name)
                else:
                    calls.append(place)
                    place = get_fn(fn, perams)
                    vs_h.append(vs[name])
                    hs_h.append(hs[name])
                    hs[name] = {}
                    vs[name] = {}
                    for pl, i in enumerate(perams):
                        seths('%' + str(pl + 1), i, name)
                    # callrets.append('%'+str(int(cur[1][1:])-1))
                    callrets.append(cur[1])
            elif cur[2] == 'extern':
                seths(cur[1], extern.imp(perams[0]), name)
            elif cur[2] == 'uxtime':
                seths(cur[1], time.time(), name)
            elif cur[2] == 'list':
                seths(cur[1], perams, name)
            elif cur[2] == 'first':
                seths(cur[1], perams[0][0], name)
            elif cur[2] == 'last':
                seths(cur[1], perams[0][-1], name)
            elif cur[2] == 'head':
                seths(cur[1], perams[0][:-1], name)
            elif cur[2] == 'tail':
                seths(cur[1], perams[0][1:], name)
            elif cur[2] == 'push':
                seths(cur[1], perams[0]+[perams[1]], name)
            elif cur[2] == 'size':
                seths(cur[1], len(perams[0]), name)
            elif cur[2] == 'load':
                seths(cur[1], oo_get(perams[0], perams[1]), name)
            else:
                print('fn not found', cur[2])
                exit()

        elif cur[0] == 'jump':
            if not get(cur[1], name):
                place += int(cur[2])
        else:
            print('err')
        place += 1
        loops += 1
        #time.sleep(0.01)
        #tot += int((time.time() - t) * 10**8)
    # print(int(1/(tot/loops/10**8)))
    for i in hotspot:
        pass
        #print(i)

def b_load(perams):
    a = perams[0]
    for i in perams[1:]:
        a = oo_get(a, i)
    seths(cur[1], a, name)


bull = {
    'print': lambda x : print('-> '+str(x)),
    'print': print,
    'int': int,
    'float': float,
    'str': str,
    'trunc': lambda num, to: int(num * 10**to) / 10**to
}

vs = dict()
hs = {('main',):dict()}
fs = dict()
rets = dict()
fs = {('main',):bull}
bs = ['extern', 'load','uxtime','list','jit','push','pop','last','init','size','head','tail','size']
vs_h = []
hs_h = []
ops = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '^': lambda x, y: x ** y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '&&': lambda x, y: x and y,
    '||': lambda x, y: x or y,
    '!!': lambda x, y: x[y] ,
    '.': oo_get,
}
quit = exit
