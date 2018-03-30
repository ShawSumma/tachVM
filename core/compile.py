def instr(stri):
    ins = stri.split(' ')
    if ins[0] == 'load':
        ret = 'hold[' + ins[1][1:] + '] = '
        if ins[2][0] == '$':
            ret += '{**funcs,**vs}[\'' + ins[2][1:] + '\']'
        else:
            ret += 'hold[' + ins[2][1:] + ']'
        return ret
    if ins[0] == 'set':
        return 'vs[\'' + ins[1] + '\'] = hold[' + ins[2][1:] + ']'
    if ins[0] == 'int':
        return 'hold[' + ins[1][1:] + '] = ' + ins[2]
    if ins[0] == 'float':
        return 'hold[' + ins[1][1:] + '] = ' + ins[2]
    if ins[0] == 'op':
        ret = ''
        ret += 'a = hold[' + ins[3][1:] + ']\n'
        ret += 'b = hold[' + ins[4][1:] + ']\n'
        ret +=  'hold[' + ins[2][1:] + '] =  a '+ ins[1] + ' b '
        return ret
    if ins[0] == 'perams':
        return 'perams = (' + ''.join(['hold[' + i[1:] + '], ' for i in ins[1:]]) + ')'
    if ins[0] == 'call':
        ret = ''
        ret += 'i_call('+ins[1][1:]+', '+ins[2][1:]+')'
        #exit()
        return ret
    if ins[0] == 'def':
        ret = ''
        ret += 'if not \'' + ins[1] + '\' in funcs:\n'
        ret += '\tfuncs[\'' + ins[1] + '\'] = []\n'
        g = ''.join('\'' + i + '\', ' for i in ins[2:-1])
        ret += 'funcs[\'' + ins[1] + '\'].append(((' + g + '), '+str(pl)+'))\n'
        #ret += 'vs[\'' + ins[1] + '\'] = ' + str(pl)+'\n'
        #fs[name][cur[1]]['fn'].append([cur[2:-1], place])
        ret += 'line += ' + ins[-1]
        return ret
    if ins[0] == 'return':
        ret = 'i_ret('+ins[1][1:]+')'
        return ret
    if ins[0] == 'jump':
        ret = ''
        ret += 'if not bool(hold['+ins[1][1:]+']):\n'
        ret += '\tline += int('+ins[2]+')\n'
        return ret
    elif ins[0] == 'str':
        return 'hold[' + ins[1][1:] + '] = "' + stri[5+len(ins[1]):-1] + '"'
    print(stri)
    print('error')
    exit()

def auto():
    return open('core/auto/auto.py').read()


def comp(byc):
    global pl
    code = byc.split('\n')
    pl = 1
    ret = ''
    ret += auto()
    ret += 'line = 0\n'
    ret += 'calls = []\n'
    ret += 'rets = []\n'
    #ret += 'funcs = {}\n'
    ret += 'hold = {}\n'
    ret += 's_vs = [{"x":0}]\n'
    ret += 's_hold = []\n'
    ret += 'orig = open("/Users/shawsumma/Desktop/code/mar-18/tachvm/tachVM/core/emit/interm.rion").read().split("\\n")\n'
    ret += 'while line <= ' + str(len(code)) + ':\n'
    #ret += '\tprint("\t",hold)\n'
    #ret += '\tprint("\t",s_vs)\n'
    #ret += '\tprint(orig[line-1])\n'
    for line in code:
        if len(line) == 0:
            pl += 1
            continue
        s = instr(line)
        if s != None:
            if pl == 1:
                ret += '\tif line == ' + str(pl) + ':\n'
            else:
                ret += '\telif line == ' + str(pl) + ':\n'
            for i in s.split('\n'):
                ret += '\t\t' + i + '\n'
        pl += 1
    ret += '\tline += 1'
    body = ret
    ret = open('core/auto/funcs.py').read()
    ret += 'def main():\n'
    for i in body.split('\n'):
        ret += '\t' + i + '\n'
    ret += 'if __name__ == "__main__":\n'
    ret += '\tmain()'
    ret = ret.replace('\t', '    ')
    #print(ret)
    return ret
