import ctypes
import inspect
import time


def log(case, msg):
    if case == 0:
        pass
    elif case == 1:
        msg = "当前执行: " + msg
    elif case == 2:
        msg = "完成执行: " + msg
    elif case == 3:
        msg = "发生错误: " + msg
    elif case == 4:
        msg = "完成选择: " + msg
    cur_time = time.strftime("%H:%M:%S", time.localtime(time.time()))
    msg = cur_time + "  " + msg
    return msg


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)



