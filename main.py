import argparse

from config import args_NoInput, get_last_compile, check_DefaultGen, check_DefaultSol
from mars_oi import do_run, do_compile, do_test, do_check, do_clean


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mars OI')
    subparsers = parser.add_subparsers(dest='command')

    run_parser = subparsers.add_parser('run', help='Run the program')
    run_parser.add_argument("-i", "--input", nargs='?', type=str,
                            default=args_NoInput,
                            help="Input file", required=False)
    run_parser.add_argument("-o", "--output", nargs='?', type=str,
                            default=args_NoInput,
                            help="Output file", required=False)
    run_parser.add_argument("-t", "--timeout", type=int, default=5000,
                            help="Timeout in milliseconds", required=False)
    run_parser.add_argument("-c", "--console", action='store_true',
                            help="Run in console mode", required=False)
    run_parser.add_argument("-e", "--exec", type=str, default=get_last_compile(),
                            help="Executable file", required=False)
    run_parser.set_defaults(func=do_run)

    compile_parser = subparsers.add_parser('compile', help='Compile the code')
    compile_parser.add_argument("-f", "--with_freopen", action='store_true',
                                help="Compile with freopen", required=False)
    compile_parser.add_argument("source", type=str, help="Source file")
    compile_parser.set_defaults(func=do_compile)

    test_parser = subparsers.add_parser('test', help='Test the code')
    test_parser.add_argument("-e", "--exec", type=str, default=get_last_compile(),
                             help="Executable file", required=False)
    test_parser.add_argument("-t", "--timeout", type=int, default=5000,
                             help="Timeout in milliseconds", required=False)
    test_parser.add_argument("-c", "--check_func", type=str, default="fc",
                             help="Check function", required=False)
    test_parser.add_argument("name", type=str, help="Test name")
    test_parser.set_defaults(func=do_test)

    check_parser = subparsers.add_parser('check', help='Check the code')
    check_parser.add_argument("-e", "--exec", type=str, default=get_last_compile(),
                              help="Executable file", required=False)
    check_parser.add_argument("-g", "--gen", default=check_DefaultGen, type=str,
                              help="Generator program", required=False)
    check_parser.add_argument("-s", "--sol", default=check_DefaultSol, type=str,
                              help="Solution program", required=False)
    check_parser.add_argument("-c", "--check_func", type=str, default="fc",
                              help="Check function", required=False)
    check_parser.set_defaults(func=do_check)

    clean_parser = subparsers.add_parser('clean', help='Clean the test')
    clean_parser.set_defaults(func=do_clean)

    args = parser.parse_args()
    args.func(args)
