# SCREENSHOT GRABBER
# Uses Windows Graphics Device Interface (GDI) to dermine image properties and to grab the image

import win32gui
import win32ui
import win32con
import win32api

# grab a handle to the main desktop window (entire viewable area across multiple monitors)
hdesktop = win32gui.GetDesktopWindow()

# determine the size of all monitors in pixels
#2
width  = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left   = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top    = win32api.GetSystemMetrics(win32con.SM_YXVIRTUALSCREEN)

# create a devive context using GetWindowDC and pass in handle to our desktop
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc     = win32ui.CreateDCFromHandle(desktop_dc)

# create a memory based device context (this is where the image capture will be stored)
mem_dc = img_dc.CreateCompatibleDC()

# create a bitmap object, set to the device context of our Desktop
# the SelectObject call sets the memory-based device content to point to bitmap object we're capturing
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy the screen into the memory device context
# Use BitBlt to take a bit-for-bit copy of the desktop image and store it in memory-based context
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# save the bitmap to a file
screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

# free the objects
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
