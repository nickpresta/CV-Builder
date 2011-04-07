import json
import re
import urllib2

from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(urllib2.urlopen("http://www.uoguelph.ca/academics/departments/").read())
lis = [re.sub("\s{2,}", " ", e.text).replace("&amp;", "&") for e in soup.findAll("li")]

# Outputs the data in a YAML fixture that can be used to import into the
# database

for i, dept in enumerate(lis[9:]):
    print '- model: cv.departmentchoice'
    print '  pk: %d' % (int(i) + 1)
    print '  fields:'
    print '    name: %s' % dept
