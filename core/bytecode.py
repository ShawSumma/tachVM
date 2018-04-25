# A = before op
# B = after op
# S = set
# C = flow condition
# B = block
# R = raw name
# F = function name
# P = perams
# E = return
# D = def
doret = False


def make_expr(tree, pref, main=False):
    global doret
    doret = False
    if tree is None:
        return ''
    if isinstance(tree, list):
        ret = ''
        # ret += 'from '
        # ret += pref
        # ret += '\n'
        for pl, i in enumerate(tree):
            ret += make_expr(i, pref + '_' + str(pl)) + '\n'
            if doret and not main:
                ret += 'return %s\n' % (pref + '_' + str(pl))
        ret = ret[:-1]
        doret = True
        return ret
    type = tree['type']
    if type == 'set':
        if tree['pre']['type'] == 'name':
            if tree['set'] == '=':
                ret = ''
                ret += make_expr(tree['post'], pref + '_S')
                ret += '\n'
                ret += 'set '
                ret += 'R_'
                ret += tree['pre']['data']
                ret += ' '
                ret += pref + '_S'
                doret = False
                return ret
        elif tree['pre']['type'] == 'tuple':
            tree_perams = tree['pre']['data']
            perams = ''
            for i in tree_perams:
                perams += i['type'] + '_' + i['data'] + ' '
            ret = ''
            ret += 'def ' + pref + ' ' + perams
            r2 = ''
            r2 += make_expr([tree['post']], pref)
            ret += str(len(r2.split('\n')))
            ret += '\n'
            ret += r2
            doret = True
            return ret
        else:
            name = tree['pre']['fn']['data']
            tree_perams = tree['pre']['perams']
            perams = ''
            for i in tree_perams:
                perams += i['type'] + '_' + i['data']+' '
            ret = ''
            ret += 'def R_' + name + ' ' + perams
            r2 = ''
            r2 += make_expr([tree['post']], pref)
            ret += str(len(r2.split('\n')))
            ret += '\n'
            ret += r2
            doret = True
            return ret
    if type == 'oper':
        ret = ''
        ret += make_expr(tree['pre'], pref + '_A')
        ret += '\n'
        ret += make_expr(tree['post'], pref + '_B')
        ret += '\n'
        ret += 'oper '
        ret += tree['oper'] + ' '
        ret += pref + ' '
        ret += pref + '_A' + ' ' + pref + '_B'
        doret = True
        return ret
    if type == 'int':
        doret = True
        return 'int ' + pref + ' ' + str(tree['data'])
    if type == 'str':
        doret = True
        return 'str ' + pref + ' ' + str(tree['data'])
    if type == 'name':
        ret = ''
        ret += 'load '
        ret += pref
        ret += ' R_'
        ret += tree['data']
        doret = True
        return ret
    if type == 'flow':
        flow = tree['flow']
        cond = tree['condition']
        then = tree['then']
        if flow == 'if':
            ret = ''
            ret += make_expr(cond, pref + '_C')
            r2 = ''
            r2 += make_expr(then, pref)
            ret += '\n'
            ji = 'jump not '
            ji += pref + '_C '
            ji += str(len(r2.split('\n')))
            ji += '\n'
            ret += ji + r2
            doret = False
            return ret
    if type == 'code':
        ret = ''
        ret += make_expr(tree['data'], pref + '_B')
        ret = 'def %s %s' % (pref+'_B', len(ret.split('\n'))+1) + '\n' + ret
        ret += '\n'
        ret += 'load %s %s' % (pref, pref+'_B')
        ret += '\n'
        ret += 'perams'
        ret += '\n'
        ret += 'do %s %s' % (pref, pref+'_B')
        doret = True
        return ret
    if type == 'fn':
        ret = ''
        ret += make_expr(tree['fn'], pref + '_F')
        ret += '\n'
        for pl, i in enumerate(tree['perams']):
            ret += make_expr(i, pref + '_P_' + str(pl))
            ret += '\n'
        ret += 'perams'
        for pl, i in enumerate(tree['perams']):
            ret += ' ' + pref + '_P_' + str(pl)
        ret += '\n'
        ret += 'call ' + pref + ' ' + pref + '_F'
        ret += '\n'
        doret = True
        return ret
    print(type)


def make(tree):
    return make_expr(tree, pref='B', main=True)
