import os

args_NoInput = "#####"

compile_BinDir = os.path.join(os.getcwd(), "bin")
compile_ProcessFile = os.path.join(compile_BinDir, "process.cpp")
compile_LastCompile = os.path.join(compile_BinDir, "last_compile.txt")
compile_Flags = [
    "-x", "c++", "-std=c++14", "-Wl,--stack=536870912",
    "-g", "-DONLINE_JUDGE", "-Wall", "-fno-asm", "-lm",
    "-march=native", "-Wno-unused-value"
]
compile_CC = "g++"

test_TestDir = os.path.join(os.getcwd(), "test")
test_OutputFile = os.path.join(test_TestDir, "output.txt")

check_DefaultGen = os.path.join(os.getcwd(), "test", "gen")
check_DefaultSol = os.path.join(os.getcwd(), "test", "sol")
check_GenBin = os.path.join(compile_BinDir, "gen")
check_SolBin = os.path.join(compile_BinDir, "sol")
check_AnsFile = os.path.join(test_TestDir, "answer.txt")

run_DefaultInput = os.path.join(test_TestDir, "input.txt")
run_DefaultOutput = os.path.join(test_TestDir, "output.txt")


def get_last_compile():
    if os.path.exists(compile_LastCompile):
        with open(compile_LastCompile, "r") as f:
            return f.read()
    else:
        return None
