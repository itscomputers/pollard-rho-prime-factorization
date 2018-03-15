##  Python2 implementation of the Pollard rho method for
##  factorization into primes.  





from __future__ import print_function
from random import randint





##################################################################
##  greatest common divisor                                     ##
##  input:      integers _a, _b                                 ##
##  output:     the greatest common divisor                     ##
##################################################################

def gcd(_a,_b):
    a = abs(_a)
    b = abs(_b)
    if a % b == 0:
        return b
    while b != 0:
        r = min( a % b, b - a % b )
        a = b
        b = r
    return a

##################################################################





##################################################################
##  p-adic representation                                       ##
##  input:      integer _a and prime p                          ##
##  output:     [ e, b ] where _a = p^e * b                     ##
##################################################################

def padic(a,p):
    if p < 2:
        return 'error: requires second argument >1'
    e = 0
    while a % p == 0:
        e += 1
        a //= p
    return [ e, a ]

##################################################################





##################################################################
##  Rubin's witness of non-primality                            ##
##  input:      integer a, possible witness integer x           ##
##  output:     'probably prime' or 'composite', according to x ##
##################################################################

def witness(a,x):
    l, m = padic( a-1, 2 )
    X = pow( x, m, a )
    if X % a in [ 1, a-1 ]:
        return 'probably prime'
    for i in range( 1, l+1 ):
        Y = pow( X, 2, a )
        if Y % a == a-1:
            return 'probably prime'
            break
        if Y % a == 1:
            return 'composite'
        X = Y
    return 'composite'

##################################################################





##################################################################
##  Generate a list of primes up to X                           ##
##  input:      X (must be less than 10**10)                    ##
##  output:     list of primes < X                              ##
##  note:       uses Rabin's witness function with              ##
##              pre-specified bases that determine primality    ##
##  note:       still slow for X > 10^7, but still faster than  ##
##              with the sieve of Eratosthenes                  ##
##################################################################

def SmallPrimes(X):
    P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if X < 31:
        return P
    if 30 < X < 2047:
        B = [2]
    if 2046 < X < 1373653:
        B = [2, 3]
    if 1373652 < X < 25326001:
        B = [2, 3, 5]
    if 25326000 < X < 10**10:
        B = [2, 3, 5, 7]
    if X > 10**10:
        return 'error: input too large'
    S = [1, 7, 11, 13, 17, 19, 23, 29]
    for r in range(30,X,30):
        for s in S:
            if r + s < X:
                count = 0
                for x in B:
                    if witness(r+s,x) == 'composite':
                        count += 1
                        break
                if count == 0:
                    P.append(r+s)
    return P

##################################################################





##################################################################
##  probabilistic primality test (Rubin)                        ##
##  input:      integer a                                       ##
##  output:     'prime' or 'composite'                          ##
##  note:       for large n, it is only deciding whether a is   ##
##              probably prime or composite using 10 witnesses. ##
##              for small n, it is is determining its primality ##
##              with certainty.                                 ##
##  note:       the probability is provably > 1 - (1/4)^n       ##
##################################################################

def probprime(a):
    if a < 2047:
        witnesses = [2]
    if 2046 < a < 1373653:
        witnesses = [2, 3]
    if 1373652 < a < 25326001:
        witnesses = [2, 3, 5]
    if 25326000 < a < 3215031751:
        witnesses = [2, 3, 5, 7]
    if 3215031750 < a < 2152302898747:
        witnesses = [2, 3, 5, 7, 11]
    if 2152302898746 < a < 3474749660383:
        witnesses = [2, 3, 5, 7, 11, 13]
    if 3474749660383 < a < 341550071728321:
        witnesses = [2, 3, 5, 7, 11, 13, 17]
    if a > 341550071728321:
        witnesses = []
        while len(witnesses) < 10:
            x = randint( 2, a-1 )
            if x not in witnesses:
                witnesses.append(x)
    for x in witnesses:
        if witness(a,x) == 'composite':
            return 'composite'
            break
    return 'prime'

##################################################################




##################################################################
##  Pollard-rho factor-finding algorithm                        ##
##      with polynomial x^2 + n                                 ##
##  input:      integer a, initial seed x0                      ##
##              and constant term n                             ##
##  output:     either a nontrivial factor d of a or a itself   ##
##################################################################

def pollard(a,x0,n):
    def f(x):
        return (x**2 + n) % a
    r = f( x0 % a )
    R = f(r)
    d = gcd( r-R , a )
    while d == 1:
        r = f(r)
        R = f( f(R) )
        d = gcd( r-R, a )
    return d

##################################################################




##################################################################
##  factor-finding algorithm using varying seeds/polynomials    ##
##  input:      composite integer a                             ##
##  output:     nontrivial factor or 'error: no factor found'   ##
##  note:       based on some experimenting with simple         ##
##              seeds and constant terms, the combination       ##
##              below seems to be both fast and complete.       ##
##              i have yet to receive the error message.        ##
##################################################################

def find_factor(a):
    for n in [1, 2, -1]:
        for x0 in [2, 3, 5, 6, 8]:
            d = pollard( a, x0, n )
            if d != a:
                return d
                break
                break
    return 'error: no factor found'

##################################################################





##################################################################
##  for primality testing, we need to make some list of small   ##
##  primes and to pick a number of witnesses for primality      ##
##  testing.  i have chosen primes <1000 and 10 witnesses.      ##
##################################################################

SP = SmallPrimes(1000)

##################################################################





##################################################################
##  factoring algorithm                                         ##
##  input:      integer _a                                      ##
##  output:     sorted list of prime factors of _a              ##
##################################################################

def factor(_a):
    a = abs(_a)
    if a == 1:
        return [ 1 ]
    prime_factors = []
    for p in SP:
        if a % p == 0:
            z = padic(a,p)
            for j in range(z[0]):
                prime_factors.append(p)
            a = z[1]
            if a == 1:
                return prime_factors
    if probprime(a) == 'prime':
        prime_factors.append( a )
        unfactored = []
    else:
        unfactored = [ a ]
    while len(unfactored) > 0:
        b = unfactored[0]
        if probprime(b) == 'prime':
            unfactored.remove(b)
            prime_factors.append(b)
        else:
            d = find_factor(b)
            if d == 'error: no factor found':
                return 'error: no factor found for', b
            else:
                unfactored.remove(b)
                for c in [ d, b // d ]:
                    if probprime(c) == 'prime':
                        prime_factors.append(c)
                    else:
                        unfactored.append(c)
    return sorted(prime_factors)

##################################################################





##################################################################
##  print factorization                                         ##
##  input:      integer a                                       ##
##  output:     none, but prints factorization                  ##
##################################################################

def factor_print(a):
    F = factor(a)
    Fexp = []
    for p in sorted(set(F)):
        e = F.count(p)
        if e == 1:
            Fexp.append( str(p) )
        else:
            Fexp.append( str(p) + '^' + str(e) )
    print( a, '=', end = ' ' )
    print( *Fexp, sep = ' * ' )

##################################################################




##################################################################
##  a simple prompt to factor a desired integer or to factor    ##
##  a list of random integers.                                  ##
##################################################################

while 1 > 0:
    print()
    print( 'choose an option below:' )
    print( '   enter an integer you would like factored;' )
    print( '   "r" to factor 30 random integers;' )
    print( '   "q" to quit.' )
    print()
    z = raw_input()
    print()
    if z == 'r':
        for k in range(6,21):
            for i in range(2):
                n = randint(10**k,10**(k+1))
                factor_print(n)
    if z == 'q':
        break
    try:
        Z = int(z)
        factor_print(Z)
    except ValueError:
        print()
##################################################################




##################################################################
##################################################################
##################################################################
##################################################################
