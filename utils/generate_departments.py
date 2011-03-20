import re
import urllib2

from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(urllib2.urlopen("http://www.uoguelph.ca/academics/departments/").read())
lis = [re.sub("\s{2,}", " ", e.text).replace("&amp;", "&") for e in soup.findAll("li")]
print '\n'.join(lis[9:])
