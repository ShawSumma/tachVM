holds = 0


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
        return need(tree['pre']) + need(tree['post']) - 1
    elif t == 'fn':
        return need(tree['perams'])
    elif t == 'int':
        return 1
    elif t == 'code':
        return need(tree['data'])
    elif t == 'tuple':
        return need(tree['data'])
    elif t == 'flow':
        return need(tree['condition']) + need(tree['then']) - 1
    else:
        print('need unkown', tree)
        exit()


def line(tree):
    global holds
    global flags
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
    elif tree['type'] == 'name':
        ret = 'load %' + str(holds) + ' $' + tree['data'] + '\n'
        flags = 'return'
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
        holds -= 2
        ret = ret.strip()+'\n'
        flags = 'return'
        return ret
    elif tree['type'] in ['fn', 'tuple']:
        if tree['type'] == 'tuple':
            tree['perams'] = tree['data']
            tree['fn'] = {'data': 'list'}
        ret = ''
        h = holds
        ns = []
        for i in tree['perams']:
            ret += make([i]) + '\n'
            ns.append(holds+need(i))
            holds = ns[-1]
        #holds = h
        ret += 'perams'
        for i,hi in zip(range(len(tree['perams'])),ns):
            ret += ' %' + str(hi-1)
        ret += '\n'
        ret += 'call %' + str(h) + ' ' + tree['fn']['data']
        holds = h
        ret = ret.strip() + '\n'
        flags = 'return'
        return ret
    elif tree['type'] == 'int':
        flags = 'return'
        return 'int %' + str(holds) + ' ' + tree['data'] + '\n'
    elif tree['type'] == 'code':
        flags = 'return'
        return make(tree['data']) + '\n'
    elif tree['type'] == 'flow':
        if tree['flow'] == 'if':
            need(tree)
            pre = make([tree['condition']])
            mid = 'jump %' + str(holds)
            post = make([tree['then']], r=True)
            post = post.replace('\n\n', '\n')
            post = post.strip()
            mid += ' ' + str(len(post.split('\n')))
            ret = pre + mid + '\n' + post
            need(tree)
            return ret


def make(tree, r=False):
    global flags
    uflags = flags
    flags = None
    ret = ''
    for i in tree:
        ret += line(i) + '\n'
        if flags == 'return' and r:
            ret += 'return %' + str(holds) + '\n'
    flags = uflags
    #ret = ret.replace('\n\n','\n')
    return ret.strip()


flags = None
