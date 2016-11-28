import BeautifulSoup
import urllib
import re
u = 'http://www.xfront.com/us_states/'
soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(u))
m = re.compile(r'<li>\n<p>Name: [\w ]*</p>\n<p>Capital Name: ([\w ]*)</p>\n<p>Capital Latitude: ([\d\.]*)</p>')
print sorted([m.match(str(x)).groups() for x in soup.findAll('li')], key= lambda x: x[1])
