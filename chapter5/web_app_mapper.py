# Mapping Open Source Web App Installations

import Queue
import threading
import os
import urllib2

threads = 10

target    = 'https://www.google.com'
# directory to where we downloaded the web application
directory = '/Applications/Firefox.app'
# file extensions we are not interested in fingerprinting
filters   = ['.jpg', '.gif', '.png', '.css']

os.chdir(directory)

# Queue object where we will store the files we'll attempt to locate
web_paths = Queue.Queue()

# walk through all files and directories in local web app directory
# each valid file found gets added to web_paths Queue
for r,d,f in os.walk('.'):
    for files in f:
        remote_path = '%s/%s' % (r, files)
        if remote_path.startswith('.'):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


# keeps executing until the web_paths Queue is empty
def test_remote():
    # on each iteration, we grab a path from the Queue, add it to the target website's base web_path,
    # and attempt to retrieve it
    while not web_paths.empty():
        path = web_paths.get()
        url = '%s/%s' % (target, path)

        request = urllib2.Request(url)

        try:
            response = irllib2.urlopen(request)
            content  = response.read()

            # if we are successful at retrieving the file, we output the HTTP status code
            # and the full path of the file
            print '[%d] => %s' % (response.code, path)
            response.close()

        # if file not found or protected by an .htaccess file, urllib2 will throw an HTTPError
        # which is handled here, so the loop can continue
        except urllib2.HTTPError as error:
            # print 'Failed %s' % error.code
            pass

# creating a number of threads that will each be called the test_remote function
for i in range(threads):
    print 'Spawning thread: %d' % i
    t = threading.Thread(target=test_remote)
    t.start()
