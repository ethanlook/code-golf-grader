import sympy
def p(x):
    for i in range(len(str(x))/2):
        if str(x)[i] != str(x)[-(1+i)]: return False
    return True
print sum([(p(x) and sympy.isprime(x)) for x in range(0, 2016)])
