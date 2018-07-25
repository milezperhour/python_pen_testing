import urllib2

url = 'https://www.google.com'

# define headers dictionary
# in this case, we make it look like a Googlebot
headers = {}
headers['User-Agent'] = 'Googlebot'

# create a Request object and pass in the url and the headers dictionary
request = urllib2.Request(url, headers=headers)
# then pass Request object to the urlopen function call
response = urllib2.urlopen(request)

print response.read()
response.close()
