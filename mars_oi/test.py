import os
from colorama import Fore

from config import test_TestDir, test_OutputFile, compile_BinDir
from core import run, check, show_diff


def do_test(args):
    exec = os.path.join(compile_BinDir, args.exec + ".exe")
    input_files = [f for f in os.listdir(test_TestDir)
                   if f.startswith(args.name) and f.endswith('.in')]
    ans_files = [f for f in os.listdir(test_TestDir)
                 if f.startswith(args.name) and (f.endswith('.ans') or f.endswith('.out'))]

    input_files.sort(), ans_files.sort()
    test_num = min(len(input_files), len(ans_files))
    accept_num = 0
    for id, (input, ans) in enumerate(zip(input_files, ans_files)):
        input_file = os.path.join(test_TestDir, input)
        ans_file = os.path.join(test_TestDir, ans)
        print("Test Case", id + 1, end="")

        result = run(exec_path=exec,
                     input_file=input_file,
                     output_file=test_OutputFile,
                     time_limit_ms=args.timeout)

        if result.error:
            raise Exception("Unknow Error at running or reading infomation")

        if result.timeout:
            print(Fore.BLUE + f"\rTest Case {id + 1} Time limit Exceeded")
            print("Input/Answer:\t", ans)
        else:
            if result.exit_code != 0:
                print(Fore.MAGENTA + f"\rTest Case {id + 1} Runtime Error Exit code {result.exit_code}")
                print("Input/Answer:\t", input, ans)
            elif check(input_file, test_OutputFile, ans_file, args.check_func):
                print(Fore.GREEN + f"\rTest Case {id + 1} Accepted")
                print("Input/Answer:\t", input, ans)
                accept_num += 1
            else:
                print(Fore.RED + f"\rTest Case {id + 1} Wrong Answer")
                print("Input/Answer:\t", input, ans)
                show_diff(input_file, test_OutputFile, ans_file, args.check_func)
            print(f"Time Used:\t{result.time_used / 1e7}s")
            print(f"Memory Used:\t{result.memory_used / 1024 / 1024}MB")
        print(Fore.RESET)
    print(Fore.GREEN if accept_num == test_num else Fore.RED, end="")
    print("Total Score:", accept_num / test_num * 100)
    print(Fore.RESET, end="")
