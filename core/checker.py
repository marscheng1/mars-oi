import sys
from subprocess import call, PIPE

from config import check_DefaultCheckerExec


class Checker:
    def check(self, input_file: str, output_file: str, ans_file: str) -> bool:
        raise NotImplementedError

    def show_diff(self, input_file: str, output_file: str, ans_file: str) -> None:
        raise NotImplementedError


class FcChecker(Checker):
    def check(self, _, output_file, ans_file):
        return call(["fc", "/A", "/W", output_file, ans_file], stdout=PIPE) == 0

    def show_diff(self, _, output_file, ans_file):
        call(["fc", "/A", "/W", "/N", output_file, ans_file], stdout=sys.stdout, stderr=sys.stderr)


class CheckChecker(Checker):
    def check(self, input_file, output_file, ans_file):
        return call([check_DefaultCheckerExec, input_file, output_file, ans_file], stdout=PIPE) == 0

    def show_diff(self, input_file, output_file, ans_file):
        call([check_DefaultCheckerExec, input_file, output_file, ans_file],
             stdout=sys.stdout, stderr=sys.stderr)


_checkers = {
    "fc": FcChecker(),
    "check": CheckChecker()
}


def check(input_file: str, output_file: str, ans_file: str, func: str):
    if func not in _checkers:
        raise ValueError(f"Checker for {func} not found")
    return _checkers[func].check(input_file, output_file, ans_file)


def show_diff(input_file: str, output_file: str, ans_file: str, func: str):
    if func not in _checkers:
        raise ValueError(f"Checker for {func} not found")
    _checkers[func].show_diff(input_file, output_file, ans_file)
