import os
from subprocess import call
from colorama import Fore

from config import check_GenBin, check_SolBin, run_DefaultOutput, run_DefaultInput, check_AnsFile, compile_BinDir
from core import check, show_diff


def do_check(args):
    exec = os.path.join(compile_BinDir, args.exec + ".exe")
    call(["g++", "-o", check_GenBin, args.gen + ".cpp"])
    call(["g++", "-o", check_SolBin, args.sol + ".cpp"])
    count = 1
    while True:
        try:
            print(f"Test {count}", end=" ")
            call([check_GenBin], stdout=open(run_DefaultInput, "w"))
            call([check_SolBin], stdin=open(run_DefaultInput, "r"), stdout=open(check_AnsFile, "w"))
            call([exec], stdin=open(run_DefaultInput, "r"),
                 stdout=open(run_DefaultOutput, "w"))
            if check(run_DefaultInput, run_DefaultOutput, check_AnsFile, args.check_func):
                print(Fore.GREEN + f"\rTest {count} Accepted!" + Fore.RESET)
            else:
                print(Fore.RED + f"\rTest {count} Failed!")
                show_diff(run_DefaultInput, run_DefaultOutput, check_AnsFile, args.check_func)
                print(Fore.RESET, end="")
                break
            count += 1
        except KeyboardInterrupt:
            break
