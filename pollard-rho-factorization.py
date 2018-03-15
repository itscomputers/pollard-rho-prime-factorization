##  Python3 implementation of the Pollard rho method for
##  factorization into primes.  



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
        r = a % b
        if r > b/2:
            r -= b
        a = b
        b = abs(r)
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
##  smallprimes function                                        ##
##  input:      upper bound X                                   ##
##  output:     list of primes < X                              ##
##  method:     sieve of eratosthanes                           ##
##  warning:    the method is slow/inefficient if X > 10000     ##
##################################################################

def smallprimes(X):
    prime_list = []
    number_list = [ j for j in range(2,X) ]
    while len(number_list) > 0:
        p = number_list[0]
        if p ** 2 >= X:
            for n in number_list:
                number_list.remove(n)
                prime_list.append(n)
        else:
            for n in number_list:
                if n % p == 0:
                    number_list.remove(n)
            prime_list.append(p)
    return prime_list

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
##  probabilistic primality test (Rubin)                        ##
##  input:      integer a, number of witnesses n                ##
##  output:     'prime' or 'composite'                          ##
##  note:       for n < a-3, it is only deciding whether a is   ##
##              probably prime or composite.  for n > a-4,      ##
##              it is determining with certainty its primality. ##
##              for simplicity, i have it returning 'prime'     ##
##              in both cases, although usually this means      ##
##              probably prime.                                 ##
##  note:       the probability is provably > 1 - (1/4)^n       ##
##              but actually much better.  in practice,         ##
##              for large n, 5 witnesses seems to give accurate ##
##              results nearly all of the time, so i have       ##
##              opted for 10 witnesses to be safe.              ##
##################################################################

def probprime(a,n):
    if n > a-4:
        witnesses = [ j for j in range(2,a-1) ]
    else:
        witnesses = []
        while len(witnesses) < n:
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

SP = smallprimes(1000)

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
    if probprime(a,10) == 'prime':
        prime_factors.append( a )
        unfactored = []
    else:
        unfactored = [ a ]
    while len(unfactored) > 0:
        b = unfactored[0]
        if probprime(b,10) == 'prime':
            unfactored.remove(b)
            prime_factors.append(b)
        else:
            d = find_factor(b)
            if d == 'error: no factor found':
                return 'error: no factor found for', b
            else:
                unfactored.remove(b)
                for c in [ d, b // d ]:
                    if probprime(c,10) == 'prime':
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
    z = input()
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
