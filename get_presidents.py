import BeautifulSoup
import urllib
import re

url = 'http://www.presidentsusa.net/presvplist.html'
soup = BeautifulSoup.BeautifulSoup(urllib.urlopen(url))
td_list = [str(x) for x in soup.findAll('td')]
matcher = re.compile('<td>([0-9]*)\. <a href="[a-z\.]*">([\w \.]*) \(([0-9]*)-?([0-9a-z]*)?\).*')
for td in td_list:
    matches = matcher.match(td)
    if matches:
        num_pres, name, begin, end = matches.groups()
        print '#{}: {}, {}-{}'.format(num_pres, name, begin, end)
    elif '9.' in td or '20.' in td:
        print td
