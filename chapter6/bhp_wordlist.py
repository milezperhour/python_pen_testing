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
