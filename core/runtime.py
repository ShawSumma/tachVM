import time
import extern
import jit


def setss(name, val):
    global ss
    ss[name] = val


def set(name, val):
    global ss
    if not type(name) in [type(str), type(int), type(float),
                          type(tuple), type(list)]:
        fs[name] = val
    if name != 'del':
        ss[name] = val


def get(name):
    if name in ss:
        return ss[name]
    elif name in fs:
        return fs[name]
    elif name in bs:
        return name
    elif name in bs:
        return name
    print('unkown ->', name, list(ss))
    exit()


def get_fn(fn, perams):
    # print(fn)
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
            default = can
        if max < mats:
            max = mats
            best = can
    # print(best)
    best = best if best is not None else default
    if best is None:
        print('no candidate function')
        print(fn)
        print(perams)
        exit()
    # print(best)
    return best


def oo_get(a, b):
    ret = vars(a)[b]
    return ret


def run(bytecode, place=0):
    # jit.jit_comp(bytecode)
    global ss_h
    global ss
    global fs
    global rets
    global ops
    if len(bytecode) == 0:
        return
    split = bytecode.split('\n')
    loops = 0
    # tot = 0
    # threads = 0
    # points = {}
    calls = []
    callrets = []
    perams = []
    ons = 0
    hotspot = [0] * len(split)
    while place < len(split):
        hotspot[place] += 1
        # print(hotspot[place])
        cur = split[place]
        # print(place+1)
        # print(cur)
        # print(ss)
        cur = cur.split()
        if len(cur) < 1:
            # hotspot[place] -= time.time()
            place += 1
            continue
        if cur[0] == 'oper':
            a, b = get(cur[3]), get(cur[4])
            op = cur[1]
            res = ops[op](a, b)
            setss(cur[2], res)
        elif cur[0] == 'int':
            setss(cur[1], int(cur[2]))
        elif cur[0] == 'float':
            setss(cur[1], float(cur[2]))
        elif cur[0] == 'str':
            re = ''.join(i+' ' for i in cur[2:])[:-1]
            setss(cur[1], re)
        elif cur[0] == 'set':
            setss(cur[1], get(cur[2]))
        elif cur[0] == 'load':
            setss(cur[1], get(cur[2]))
        elif cur[0] == 'def':
            if not cur[1] in fs:
                fs[cur[1]] = {'type': 'fn', 'fn': []}
            fs[cur[1]]['fn'].append([cur[2:-1], place])
            place += int(cur[-1])
        elif cur[0] == 'return':
            got = get(cur[1])
            # print(ss_h)
            if ss_h[-1] is not None:
                ss = ss_h[-1]
            ss_h = ss_h[:-1]
            perams = []
            setss(callrets[-1], got)
            place = calls[-1]
            calls = calls[:-1]
            callrets = callrets[:-1]
            ons -= 1
        elif cur[0] == 'perams':
            perams = []
            for i in cur[1:]:
                perams.append(get(i))
        elif cur[0] == 'do':
            calls.append(place)
            cur[2] = get(cur[2])
            ffn, place = get_fn(cur[2], perams)
            ss_h.append(ss)
            for i, p in zip(ffn, perams):
                # print(i)
                name = i
                name = ''.join(
                    j + '_' for j in name.split('_')[1:])[:-1]
                name = 'R_' + name
                setss(name, p)
            callrets.append(cur[1])
        elif cur[0] == 'call':
            ons += 1
            cur[2] = get(cur[2])
            if cur[2] not in bs and not isinstance(cur[2], str):
                fn = cur[2]
                if callable(fn):
                    setss(cur[1], fn(*perams))
                else:
                    calls.append(place)
                    ffn, place = get_fn(fn, perams)
                    ss_h.append(ss)
                    ss = {}
                    ss = {**oss, **bull}
                    for i, p in zip(ffn, perams):
                        # print(i)
                        name = i
                        name = ''.join(
                            j + '_' for j in name.split('_')[1:])[:-1]
                        name = 'R_' + name
                        setss(name, p)
                    # print(ss)
                    # callrets.append('%'+str(int(cur[1][1:])-1))
                    callrets.append(cur[1])
            else:
                cur[2] = cur[2][2:]
                if cur[2] == 'extern':
                    setss(cur[1], extern.imp(perams[0]))
                elif cur[2] == 'uxtime':
                    setss(cur[1], time.time())
                elif cur[2] == 'list':
                    setss(cur[1], perams)
                elif cur[2] == 'first':
                    setss(cur[1], perams[0][0])
                elif cur[2] == 'last':
                    setss(cur[1], perams[0][-1])
                elif cur[2] == 'head':
                    setss(cur[1], perams[0][:-1])
                elif cur[2] == 'tail':
                    setss(cur[1], perams[0][1:])
                elif cur[2] == 'push':
                    setss(cur[1], perams[0] + [perams[1]])
                elif cur[2] == 'size':
                    setss(cur[1], len(perams[0]))
                elif cur[2] == 'load':
                    setss(cur[1], oo_get(perams[0], perams[1]))
                elif cur[2] == 'print':
                    print('out :', *perams)
                    setss(cur[1], ''.join(str(i) for i in perams))
                else:
                    print('fn not found', cur[2])
                    exit()

        elif cur[0] == 'jump':
            if not get(cur[1]):
                place += int(cur[2])
        elif cur[0] == 'jump_if':
            if get(cur[1]):
                place += int(cur[2])
        else:
            print('err')
            exit()
        # hotspot[place] -= time.time()
        place += 1
        loops += 1
        # time.sleep(0.005)
    for pl, i in enumerate(hotspot):
        pl = str(pl)
        pl = ' ' * (8 - len(pl)) + pl
        print('hotspot %s : %s' % (pl, i))
    # print(ss)
    # print(ss)


# def b_load(perams):
#     a = perams[0]
#     for i in perams[1:]:
#         a = oo_get(a, i)
#     setss(cur[1], a)


_bull = {
    # 'print': lambda x: print('-> ' + str(x)),
    # 'print': print,
    'int': int,
    'float': float,
    'str': str,
    'trunc': lambda num, to: int(num * 10**to) / 10**to
}


_bs = ['extern', 'load', 'uxtime', 'list', 'jit', 'push',
       'pop', 'last', 'init', 'size', 'head', 'tail', 'size',
       'print']

bull = dict()
for i in _bull:
    bull['R_' + i] = _bull[i]

bs = []
for i in _bs:
    bs.append('R_' + i)

ss = dict()
rets = dict()
fs = dict()
oss = {
    'true': 1,
    'false': 0,
}
ss = oss
ss_h = []
ops = {
    # '+': jit.Ops.add,
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
    '!!': lambda x, y: x[y],
    '.': oo_get,
}
quit = exit
