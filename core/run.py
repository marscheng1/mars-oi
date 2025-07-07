import os
import sys
from ctypes import CDLL, Structure, c_bool, c_size_t, c_ubyte, c_char_p


class RunInfoType(Structure):
    _fields_ = [
        ('error', c_bool),
        ('timeout', c_bool),
        ('time_used', c_size_t),
        ('memory_used', c_size_t),
        ('exit_code', c_ubyte)
    ]


if getattr(sys, 'frozen', False):
    _dll_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'core.dll')
elif __file__:
    _dll_path = os.path.join("bin", 'core.dll')
_core_dll = CDLL(_dll_path)
_core_dll.run.argtypes = [
    c_char_p,  # exec
    c_char_p,  # in_file
    c_char_p,  # out_file
    c_size_t   # time_limit
]
_core_dll.run.restype = RunInfoType


class RunInfo:
    def __init__(self, info: RunInfoType):
        self.error = bool(info.error)
        self.timeout = bool(info.timeout)
        self.time_used = int(info.time_used)
        self.memory_used = int(info.memory_used)
        self.exit_code = int(info.exit_code)


def run(exec_path, input_file, output_file, time_limit_ms=5000) -> RunInfo:
    return RunInfo(_core_dll.run(
        exec_path.encode(),
        input_file.encode(),
        output_file.encode(),
        time_limit_ms
    ))
