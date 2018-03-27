import time
def seths(name, val):
    hs[int(name[1:])] = val


def setvs(name, val):
    global vs
    if name in vs:
        print('immutable error on ',name)
        exit()
    if name != 'del':
        vs[name] = val


def get(name):
    if name[0] == '%':
        return hs[int(name[1:])]
    elif name == '-':
        return None
    else:
        if name[1:] in vs:
            return vs[name[1:]]
        else:
            return fs[name[1:]]

def get_fn(fn,perams):
    best = None
    max = 0
    default = None
    if isinstance(fn,dict):
        fn = fn['fn']
    #print(fn)
    for can in fn:
        mats = 0
        kats = 0
        ps = can[0]
        for pl,i in enumerate(ps):
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
    #print(best)
    best = best if best != None else default
    return best
def run(bytecode):
    # return
    global hs_h
    global vs_h
    global vs
    global hs
    global fs
    if len(bytecode) == 0:
        return
    split = bytecode.split('\n')
    place = 0
    points = {}
    calls = []
    callrets = []
    perams = []
    while place < len(split):
        cur = split[place].split()
        if len(cur) < 1:
            place += 1
            continue
        #print(split[place])
        #print('hs_h',hs_h)
        #print('\t\t',hs)
        if cur[0] == 'int':
            seths(cur[1], int(cur[2]))
        elif cur[0] == 'set':
            setvs(cur[1], get(cur[2]))
        elif cur[0] == 'load':
            seths(cur[1], get(cur[2]))
        elif cur[0] == 'op':
            a, b = get(cur[3]), get(cur[4])
            res = ops[cur[1]](a, b)
            seths(cur[2], res)
        elif cur[0] == 'def':
            if not cur[1] in fs:
                fs[cur[1]] = {'type':'fn','fn':[]}
            fs[cur[1]]['fn'].append([cur[2:-1],place])
            place += int(cur[-1])
        elif cur[0] == 'return':
            got = get(cur[1])
            vs = vs_h[-1]
            hs = hs_h[-1]
            vs_h = vs_h[:-1]
            hs_h = hs_h[:-1]
            perams = []
            #print(callrets)
            seths(callrets[-1], got)
            place = calls[-1]
            calls = calls[:-1]
            callrets = callrets[:-1]
        elif cur[0] == 'perams':
            perams = []
            for i in cur[1:]:
                perams.append(get(i))
        elif cur[0] == 'call':
            if cur[2] in fs or cur[2] in vs:
                calls.append(place)
                name = cur[2]
                if name in vs:
                    fn = vs[name]
                else:
                    fn = fs[name]
                fn['fn']
                place = get_fn(fn,perams)
                vs_h.append(vs)
                hs_h.append(hs)
                hs = {}
                vs = {}
                for pl, i in enumerate(perams):
                    seths('%'+str(pl + 1), i)
                #callrets.append('%'+str(int(cur[1][1:])-1))
                callrets.append(cur[1])
            elif cur[2] == 'print':
                print(*perams)
            elif cur[2] == 'list':
                seths(cur[1],perams)
            elif cur[2] == 'uxtime':
                seths(cur[1],time.time())
            else:
                print('fn not found',cur[2])
                exit()
        elif cur[0] == 'jump':
            if not get(cur[1]):
                place += int(cur[2])
        #time.sleep(0.03)
        place += 1
    #print('hs =',hs)
    #print('vs =',vs)
    #print('fs =',fs)

vs = {}
hs = {}
fs = {}
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
}
quit = exit
