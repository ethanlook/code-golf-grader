import BeautifulSoup
import urllib
import re

url = 'http://www.xfront.com/us_states/'
soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(url))
td_list = [str(x) for x in soup.findAll('li')]
matcher = re.compile(r'<li>\n<p>Name: ([\w]*)</p>\n<p>Capital Name: ([\w]*)<p>\n<p>Capital Latitude: ([\d\.]*)</p>.*', re.MULTILINE)
for td in td_list:
    print matcher.match(td).groups()
