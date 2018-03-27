holds = 0
flows = 0
last_line = 0
def need(tree):
    if isinstance(tree, list):
        if tree != []:
            return max(map(need, tree))
        return 1
    t = tree['type']
    if t == 'set':
        return need(tree['post'])
    elif t == 'name':
        return 1
    elif t == 'oper':
        return max(need(tree['pre']),need(tree['post']))
    elif t == 'fn':
        return need(tree['perams'])
    elif t == 'int':
        return 1
    elif t == 'str':
        return 1
    elif t == 'float':
        return 1
    elif t == 'code':
        return need(tree['data'])
    elif t == 'tuple':
        return need(tree['data'])
    elif t == 'flow':
        return need(tree['condition']) + need(tree['then'])
    else:
        print('need unkown', tree)
        exit()

def ll(data):
    return ''

def line(tree):
    global holds
    global flags
    global flows
    if isinstance(tree, list):
        return make(tree, r=True)
    elif tree['type'] == 'set':
        if tree['set'] == '=':
            if tree['pre']['type'] == 'name':
                o = holds
                holds += need(tree['post'])
                a = holds
                ret = line(tree['post'])
                holds -= need(tree['post'])
                ret += 'set '
                ret += tree['pre']['data']
                ret += ' '
                ret += '%' + str(a)
                return ret
            else:
                ret = ''
                ret += 'def ' + tree['pre']['fn']['data']
                for i in tree['pre']['perams']:
                    ret += ' '+i['type']+'_'+i['data']
                ret += '\n'
                for pl, i in enumerate(tree['pre']['perams']):
                    ret += 'set ' + i['data'] + ' %'
                    ret += str(pl + 1) + '\n'
                ret += make([tree['post']], r=True)
                ret = ret.split('\n')
                ret = [ret[0] + ' ' + str(len(ret) - 1)] + ret[1:]
                ret = ''.join(i + '\n' for i in ret)
                return ret
            flags[-1] = None
    elif tree['type'] == 'name':
        ret = 'load %' + str(holds) + ' $' + tree['data'] + '\n'
        flags[-1] = 'return'
        return ret
    elif tree['type'] == 'oper':
        op = tree['oper']
        o = holds
        holds += need(tree['pre'])
        a = holds
        ret = line(tree['pre'])
        holds += need(tree['post'])
        b = holds
        ret += line(tree['post'])
        ret += 'op '
        ret += tree['oper']
        ret += ' %' + str(o) + ' %' + str(a) + \
            ' %' + str(b)
        holds = o
        ret = ret.strip()+'\n'
        flags[-1] = 'return'
        return ret
    elif tree['type'] in ['fn', 'tuple']:
        if tree['type'] == 'tuple':
            tree['perams'] = tree['data']
            tree['fn'] = {'data': 'list'}
        ret = ''
        h = holds
        holds += need(tree['fn'])
        ns = []
        for i in tree['perams']:
            ret += make([i]) + '\n'
            ns.append(holds+need(i))
            holds = ns[-1]
        #holds = h
        ret += make([tree['fn']])+'\n'
        ret += 'perams'
        for i,hi in zip(range(len(tree['perams'])),ns):
            ret += ' %' + str(hi-1)
        ret += '\n'
        ret += 'load %'+str(h+1)+' %'+str(holds)
        ret += '\n'
        ret += 'call %' + str(h) + ' %'+str(h+1)
        holds = h
        ret = ret.strip() + '\n'
        flags[-1] = 'return'
        return ret
    elif tree['type'] == 'int':
        flags[-1] = 'return'
        return 'int %' + str(holds) + ' ' + tree['data'] + '\n'
    elif tree['type'] == 'float':
        flags[-1] = 'return'
        return 'float %' + str(holds) + ' ' + tree['data'] + '\n'
    elif tree['type'] == 'str':
        flags[-1] = 'return'
        return 'str %' + str(holds) + ' ' + tree['data'] + '\n'
    elif tree['type'] == 'code':
        flags[-1] = 'return'
        return make(tree['data']) + '\n'


def make(tree, r=False):
    global flags
    flags.append(None)
    ret = ''
    for i in tree:
        ret += line(i) + '\n'
        if flags[-1] == 'return' and r:
            ret += 'return %' + str(holds) + '\n'
    flags = flags[:-1]
    #ret = ret.replace('\n\n','\n')
    return ret.strip()


flags = []
