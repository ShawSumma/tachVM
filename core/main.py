import lex
import tree
import run
import sys
import gen
import view
import time

def run_code(code):
    toks = lex.make(code)
    code_tree = tree.tree(toks)
    #ret = run.run(code_tree)
    #view.view(code_tree)
    ret = gen.make(code_tree,r=False)
    f = open('interm.ion','w')
    f.write(ret)
    f.close()
    run.run(ret,('main',))
    return ret


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
