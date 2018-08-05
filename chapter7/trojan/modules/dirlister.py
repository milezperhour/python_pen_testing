# Exposes a run function that lists all of the files in the current directory
# and returns the list as a string


import os

def run(**args):

    print '[*] In dirlister module.'
    files = os.listdir('.')

    return str(files)
