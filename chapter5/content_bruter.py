# Brute Forcing Directories and File Locations

# This tool will accept wordlists from common brute forcers like DirBuster or SVNDigger
# and attempt to discover files on a target web server

import urllib2
import threading
import Queue
import urllib

threads       = 5
target_url    = 'http://testphp.vulnweb.com'
wordlist_file = '/tmp/all.txt' # from SVNDigger
resume        = None
user_agent    = 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

def build_wordlist(wordlist_file):
    # read in the word word list
    fd = open(wordlist_file, 'rb')
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words        = Queue.Queue()

    # iterate over each line in the wordlist file
    for word in raw_words:
        word = word.rstrip()

        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print 'Resuming wordlist from: %s' % resume

        else:
            words.put(word)

    return words


# this function accepts a Queue object that is populated with words for brute-Forcing
# and an optional list of file extensions to test
def dir_bruter(word_queue, extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # check to see if there is a file extension; of not,
        # it's a directory path we're bruting
        if '.' not in attempt:
            attempt_list.append('/%s/' % attempt)
        else:
            attempt_list.append('/%s' % attempt)

            # if we want to bruteforce extensions
            if extensions:
                for extension in extensions:
                    attempt_list.append('/%s%s' % (attempt, extension))

            # iterate over our list of attempt_list
            for brute in attempt_list:
                url = '%s%s' % (target_url, urllib.quote(brute))

                try:
                    headers = {}
                    header['User-Agent'] = user_agent # set User-Agent header to something innocuous
                    r = urllib2.Request(url, headers=headers)

                    response = urllib2.urlopen(r)

                    # if the response code is 200, we output the url
                    if len(response.read()):
                        print '[%d] => %s' % (response.code, url)

                except urllib2.URLError, e:
                    # and if we receive anything but a 404 we also output it
                    if hasattr(e, 'code') and e.code != 404:
                        print '!!! %d => %s' % (e.code, url)

                    pass



# setting up wordlist, creating a list of extensions, and spinning up the brute-forcing threads
word_queue = build_wordlist(wordlist_file)
extensions = ['.php', '.bak', '.orig', '.inc']

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
    t.start
