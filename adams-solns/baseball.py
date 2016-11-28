from BeautifulSoup import BeautifulSoup as bs
import urllib, re
l = [str(x) for x in bs(urllib.urlopen('https://espn.go.com/mlb/worldseries/history/winners')).findAll('tr')][2:]
n = re.compile('.*<td>([0-9]*)</td><td>([\w \.]*)</td>.*')
u = re.compile('.*<td>([0-9]*)</td><td><a href="[a-z:\./_-]*">([\w \.]*)</a>.*')

def h(s):
    if not 'href' in s: return False
    if s.count('href') > 1: return True
    i = s.index('/td')
    return s.index('href') < (i + s[i+1:].index('/td'))

def parse(s):
    r = u if h(s) else n
    y, t = r.match(s).groups()
    return (y.strip(), ' '.join(t.split()))

for r in l:
    y, t = parse(r)
    print '{} -> {}'.format((y, t), len(t) * int(y))
