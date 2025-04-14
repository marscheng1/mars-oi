import os
from subprocess import call

from config import compile_ProcessFile, compile_LastCompile, compile_CC, compile_Flags


def do_compile(args):
    with open(args.source + ".cpp", 'r', encoding='utf-8-sig') as f, \
            open(compile_ProcessFile, "w", encoding='utf-8') as g:
        g.write("#define LOCAL\n")
        for line in f.readlines():
            if "freopen" not in line or args.with_freopen:
                g.write(line)
    os.makedirs(os.path.join(os.getcwd(), "bin",
                os.path.dirname(args.source)), exist_ok=True)
    call([compile_CC] + compile_Flags +
         [compile_ProcessFile, "-o", os.path.join(os.getcwd(), "bin", args.source)])
    with open(compile_LastCompile, "w") as f:
        f.write(args.source)
