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

    # this function is triggered when user clicks the context menu that we defined
    def bing_menu(self, event):
        # grab the details of what the user clicked
        http_traffic = self.content.getSelectedMessages()

        print '%d requests highlighted' % len(http_traffic)

        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host         = http_service.getHost()

            print 'User selected host: %s' % host
            self.bing_search(host)

        return


    def bing_search(self, host):
        # check if we have an IP or hostname
        is_ip = re.match('[0-9]+(?:\.[0-9]+){3}', host)

        if is_ip:
            ip_address = host
            domain     = False
        else:
            ip_address = socket.gethostbyname(host)
            domain     = True

        bing_query_string = "'ip:%s'" % ip_address
        self.bing_query(bing_query_string)

        if domain:
            bing_query_string = "'domain:%s'" % host
            self.bing_query(bing_query_string)
