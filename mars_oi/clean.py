import os

from config import test_TestDir


def do_clean(_):
    for f in os.listdir(test_TestDir):
        if f.endswith('.txt') or f.endswith(".in") or f.endswith(".out") or f.endswith(".ans"):
            os.remove(os.path.join(test_TestDir, f))
