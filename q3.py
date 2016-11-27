import sympy
print sum([sympy.isprime(i) and str(i) == str(i)[::-1] for i in range(2016)])
