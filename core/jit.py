
class Jit:
    def __init__(self):
        self.fn = self.oper()

    def make_jit(self):
        pass

    def gen_ll(self):
        int_fn_int = ir.FunctionType(int_type, [int_type, int_type])
        jit_mod = ir.Module(name="jit")
        jit_fn = ir.Function(jit_mod, int_fn_int, name='jit_main')
        jit_0 = jit_fn.append_basic_block(name='jit_0')
        self.jit = ir.IRBuilder(jit_0)
        self.args = jit_fn.args
        # print('jit')
        # for i in dir(jit):
        #     print('\t', i)
        # print('ir')
        # for i in dir(ir):
        #     print('\t', i)
        # res = self.jit.add(arg_0, arg_1)
        # self.jit.ret(res)
        return jit_mod

    def gen_engine(self, module):
        mod = llvm.parse_assembly(str(module))
        mod.verify()
        engine.add_module(mod)
        engine.finalize_object()
        return engine

    def begin(self):
        global ir
        global llvm
        global c_fn_type
        global c_int64
        global engine
        global int_type
        from llvmlite import ir
        import llvmlite.binding as llvm
        from ctypes import CFUNCTYPE as c_fn_type
        from ctypes import c_int64
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly("")
        engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        int_type = ir.IntType(64)

    def oper(self):
        self.begin()
        ll = self.gen_ll()
        self.make_jit()
        eng = self.gen_engine(ll)
        fnptr = eng.get_function_address("jit_main")
        fn = c_fn_type(c_int64, c_int64)(fnptr)
        return fn


class Jit_int:
    class Add(Jit):
        def make_jit(self):
            res = self.jit.add(self.args[0], self.args[1])
            self.jit.ret(res)

class Ops:
    def add(a, b):
        if isinstance(a, float):
            return 0
        if isinstance(b, float):
            return 0
        return iAdd(a, b)

iAdd = Jit_int.Add().fn
