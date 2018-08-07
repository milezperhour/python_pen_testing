# SCREENSHOT GRABBER
# Uses Windows Graphics Device Interface (GDI) to dermine image properties and to grab the image

import win32win
import win32ui
import win32con
import win32api

# grab a handle to the main desktop window
#1
hdesktop = win32gui.GetDesktopWindow()

# determine the size of all monitors in pixels
#2
width  = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left   = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top    = win32api.GetSystemMetrics(win32con.SM_YXVIRTUALSCREEN)

# create a devive context
#3
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc     = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device context
#4
mem_dc = img_dc.CreateCompatibleDC()

# create a bitmap object
#5
screenshot = win32ui.CreateBitmap()
