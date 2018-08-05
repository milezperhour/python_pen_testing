# Creates a context menu in Burp UI
# Stores wordlist in a set, to ensures no duplicate words

from burp import IBurpExtender # import the IBurpExtender class (required)
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import re
from datetime import datetime
from HTMLParser import HTMLParser

# strips the HTML tags out of the HTTP responses that get proccessed later on
class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    # stores page text in a member variable
    def handle_data(self, data):
        self.page_text.append(data)

    # words will get store in developer comments to be added to the password list
    # for flexibility, in case we want to change how page text is proccessed
    def handle_comment(self, data):
        self.handle_data(data)

    # feeds HTML to the base class HTMLParser and returns the page text
    def strip(self, html):
        self.feed(html)
        return ' '.join(self.page_text)


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderClassbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()
        self._context   = None
        self.hosts      = set()

        # start with something that is common
        # initialize the set
        self.wordlist   = set(['password'])

        #set up the extension
        callbacks.setExtensionName('BHP Wordlist')
        callbacks.registerContextMenuFactory(self)

        return

    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Create Wordlist', actionPerformed = self.wordlist_menu))

        return menu_list


# Defines the menu-click handler
def wordlist_menu(self, event):
    # grab the details of what the user clicked
    http_traffic = self.context.getSelectedMessages()

    for traffic in http_traffic:
        http_service = traffic.getHttpService()
        host         = http_service.getHost()

        # saves the name of the responding host
        self.hosts.add(host)

        http_response = traffic.getResponse()

        if http_response:
            #retrieves the HTTP response and feeds it to get_words function
            self.get_words(http_response)

    self.display_wordlist()
    return


def get_words(self, http_response):
    # splits out the header from the message body
    headers, body = http_response.tostring().split('\r\n\r\n', 1)

    # skip the non-text responses
    if headers.lower().find('content-type: text') == -1:
        return

    # TagStripper class strips the HTML code from the rest of the page text
    tag_stripper = TagStripper()
    page_text    = tag_stripper.strip(body)
    # regular expression; find all words starting with an alphabetic character
    # followed by 2 or more 'word' characters
    words        = re.finall('[a-zA-Z]\w{2,}', page_text)

    for word in words:
        # filter out long strings
        if len(word) <= 12:
            # successful words are saved in lowercase to the wordlist
            self.wordlist.add(word.lower())

    return

# Mangles and displays captured words
# Takes a base word and turns it into a number of password guesses based on
# common password creation 'strategies'
def mangle(self, word):
    # create a list of suffixes to tack on the end of the base word (including current year)
    year     = datetime.now().year
    suffixes = ['', '1', '!', year]
    mangled = []

    # loop through attempt (with capital version of base word for good measure)
    for password in (word, word.capitalize()):
        for suffix in suffixes:
            mangled.append('%s%s' % (password, suffix))

    return mangled


def display_wordlist(self):
    # 'John the Ripper'-style comment to print which sites were used to generate this wordlist
    print '#!comment: BHP Wordlist for sites(s) %s' % ', '.join(self.hosts)

    # mangle each base word and print the results
    for word in sorted(self.wordlist):
        for password in self.mangle(word):
            print password

    return
