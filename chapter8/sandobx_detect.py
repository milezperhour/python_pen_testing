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
