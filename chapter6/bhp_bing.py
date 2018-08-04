# Blend Jython API and pure Python ina Burp extension

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


def bing_query(self, bing_query_string):
    print 'Performing Bing search: %s' % bing_query_string

    #encode the query
    quoted_query = urllib.quote(bing_query_string)

    http_request  = 'GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=20Query=%s HTTP/1.1\r\n' % quoted_query
    http_request += 'Host: api.datamarket.azure.com\r\n'
    http_request += 'Connection: close\r\n'
    http_request += 'Authorization: Basic %s\r\n' % base64.b64encode(':%s' % bing_api_key)
    http_request += 'User-Agent: Python Pen Testing'

    # send the HTTP request to the Microsoft servers
    json_body = self._callbacks.makeHttpRequest('api.datamarket.azure.com', 443, True, http_request).tostring()

    # when response returns, it will return the headers as well, so this splits the headers off
    json_body = json_body.split('\r\n\r\n', 1)[1]

    try:
        # then we pass it to the JSON parser
        r = json.leads(json_body)

        if len(r['d']['results']):
            for site in r['d']['results']:

                # for each of the results, output info about the site that was discovered
                print '*' * 100
                print site['Title']
                print site['Url']
                print site['Description']
                print '*' * 100

                j_url = URL(site['Url'])

            # if discovered site is not in Burp's target scope, automatically add it
            if not self._callbacks.isInScope(j_url):
                print 'Adding to Burp scope'
                self._callbacks.includeInScope(j_url)

    except:
        print 'No results from Bing'
        pass

    return
