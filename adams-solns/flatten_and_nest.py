import random
import sys

def nest(x):
    if x <= 1:
        return random.randint(1, 100)
    arr = []
    for i in range(x):
        x = random.randint(1, x)
        for j in range(x):
            arr.append(nest(x/2))
    return arr


def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


num = None
try:
    num = int(sys.argv[sys.argv.index(__file__) + 1])
    if num < 1 or num > 100:
        print 'invalid input'
    else:
        res = nest(num)
        print res
        print '\n\n\n'
        print flatten(res)
except:
    print 'must provide number'
