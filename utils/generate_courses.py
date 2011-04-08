import json
import re
import urllib2

from BeautifulSoup import BeautifulSoup

url = "http://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12"

soup = BeautifulSoup(urllib2.urlopen(url).read())


i = 0

for li in soup.find('div', 'subnav').findAll('li'):
    href = li.find('a')['href']
    subsoup = BeautifulSoup(urllib2.urlopen(url + href[1:]).read())
    for course in subsoup.findAll('div', 'course'):

        title = re.search(r'(\S+)\*(\S+) ([A-Za-z0-9-,/.&#;\': ]+) (?![FWS](,[FWS])*)', course.find('tr', 'title').find('a').string)
        code = title.groups(0)[0] + title.groups(0)[1]
        title = title.groups(0)[2].rpartition(' ')[0].replace(':', '').replace('&', '')
        
        print '- model: cv.course'        
        print '  pk: %d' % i
        print '  fields:'
        print '    code: %s' % code
        print '    name: %s' % title
        print '    info: '
        i += 1


#(?![FWS](,[FWS]))

# Outputs the data in a YAML fixture that can be used to import into the
# database

#for i, dept in enumerate(lis[9:]):
#    print '- model: cv.departmentchoice'
#    print '  pk: %d' % (int(i) + 1)
#    print '  fields:'
#    print '    name: %s' % dept
