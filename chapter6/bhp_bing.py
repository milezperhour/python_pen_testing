from burp import IBurpExtender # import the IBurpExtender class (required)
from burp import IIntruderPayloadGeneratorFactory

from javax.swing impport JMenuItem
from java.util import List, ArrayList
from java.net import URL

import socket
import urllib
import json
import re
import base64
bing_api_key = 'YOURKEY'

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderClassbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers()
        self._context   = None

        # set up the extension
        callbacks.setExtensionName('BHP Bing')
        callbacks.registerContextMenuFactory(self)

        return


    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem('Send to Bing', actionPerformed=self.bing_menu))
        return menu_list
