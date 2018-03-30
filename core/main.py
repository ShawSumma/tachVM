import lex
import tree
import sys
import gen
import view
import time
import compile as comp
#import mid_runtime as run

def run_code(code,mid=0):
    toks = lex.make(code)
    code_tree = tree.tree(toks)
    #ret = run.run(code_tree)
    #view.view(code_tree)

    ret = gen.make(code_tree)
    f = open('core/emit/interm.rion','w')
    f.write(ret)
    f.close()
    comd = comp.comp(ret)
    f = open('core/emit/out.py','w')
    f.write(comd)
    f.close()
    print('done')

def repl():
    while 1:
        uin = input('>>> ')
        ran = run_code(uin)['data']
        if ran != None:
            print(ran)

if len(sys.argv) > 1:
    if sys.argv[1][0] != '-':
        run_code(open(sys.argv[1]).read())
    else:
        f = open(sys.argv[2]).read()
        run.run(f)
else:
    repl()
