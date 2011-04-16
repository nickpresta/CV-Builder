import json
import re
import urllib2

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    print """
Please install BeautifulSoup module:
easy_install beautifulsoup"""
    import sys
    sys.exit()

url = "http://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12"

data = []

soup = BeautifulSoup(urllib2.urlopen(url).read())

i = 0

for li in soup.find('div', 'subnav').findAll('li'):
    href = li.find('a')['href']
    subsoup = BeautifulSoup(urllib2.urlopen(url + href[1:]).read())
    for course in subsoup.findAll('div', 'course'):

        title = re.search(r'(\S+)\*(\S+) ([A-Za-z0-9-,/.&#;\': ]+) (?![FWS](,[FWS])*)', course.find('tr', 'title').find('a').string)
        code = title.groups(0)[0] + title.groups(0)[1]
        title = title.groups(0)[2].rpartition(' ')[0].replace(':', '').replace('&', '')
        
        data.append({
            'model': 'cv.course',
            'pk': '%d' % i,
            'fields': {
                'code': code,
                'name': title,
                'info': ''
            }
        })
        
#       Replace data.append with following for yaml        
#        print '- model: cv.course'        
#        print '  pk: %d' % i
#        print '  fields:'
#        print '    code: %s' % code
#        print '    name: %s' % title
#        print '    info: '
#        i += 1

        
print json.dumps(data)
