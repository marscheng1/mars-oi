import os
from colorama import Fore
from subprocess import Popen, PIPE, TimeoutExpired
from sys import stdout

from config import args_NoInput, run_DefaultInput, run_DefaultOutput, compile_BinDir
from core import run


def read_input(input_file):
    lines = []
    while True:
        try:
            line = input()
            if (not line.strip()):
                break
            lines.append(line)
        except EOFError:
            break

    with open(input_file, "w") as f:
        f.write("\n".join(lines))


def run_console(exec: str, input_file: str, time_limit_ms: int):
    process = Popen(exec, stdin=PIPE, stdout=stdout, stderr=PIPE)
    if process.stdin is None:
        raise Exception("Failed to open stdin or stdout")
    with open(input_file, "r") as f:
        process.stdin.write(f.read().encode())
        process.stdin.flush()
    process.stdin.close()
    try:
        process.wait(timeout=time_limit_ms / 1e3)
    except TimeoutExpired:
        process.terminate()
        print(Fore.BLUE, end="")
        print("Time limit exceeded")
    else:
        if process.returncode != 0:
            print(Fore.MAGENTA, end="")
            print(f"Runtime error: Exit code {process.returncode}")
    print(Fore.RESET, end="")


def do_run(args):
    exec = os.path.join(compile_BinDir, args.exec + ".exe")
    input_file = run_DefaultInput if args.input is None or args.input == args_NoInput else args.input
    output_file = run_DefaultOutput if args.output is None or args.output == args_NoInput else args.output

    if args.input == args_NoInput:
        read_input(input_file)
    if args.console:
        run_console(exec, input_file, args.timeout)
        return

    result = run(
        exec_path=exec,
        input_file=input_file,
        output_file=output_file,
        time_limit_ms=args.timeout)

    if result.error:
        raise Exception("Unknow Error at running or reading infomation")

    if args.output == args_NoInput:
        with open(output_file, "r") as f:
            print(f.read())

    if result.timeout:
        print(Fore.BLUE, end="")
        print("Time limit exceeded")
    else:
        print(Fore.GREEN if result.exit_code == 0 else Fore.MAGENTA, end="")
        if result.exit_code != 0:
            print(f"Runtime error: Exit code {result.exit_code}")
        print(f"Time Used: {result.time_used / 1e7}s")
        print(f"Memory Used: {result.memory_used / 1024 / 1024}MB")
    print(Fore.RESET, end="")
