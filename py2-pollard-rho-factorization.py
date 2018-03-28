
##  written for python2
##  Pollard's rho algorithm used for factorization into primes.  


from __future__ import print_function
from random import randint


##################################################################
##  a simple prompt to demonstrate the factoring algorithm

def menu():
    while 1 > 0:
        print()
        print( 'choose an option below:' )
        print( '   enter a positive integer you would like factored;' )
        print( '   enter 0 to factor 30 random integers;' )
        print( '   or anything else to quit.' )
        print()
        z = raw_input()
        print()
        try:
            Z = int(z)
            if Z == 0:
                for k in range(6,21):
                    for i in range(2):
                        n = randint(10**k,10**(k+1))
                        factor_print(n)
            else:
                factor_print( abs(Z) )
        except ValueError:
            break

##################################################################


##################################################################
##  greatest common divisor
##      input:  integers _a, _b
##      output: greatest common divisor of _a, _b

def gcd( _a, _b ):
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
##  p-adic representation
##      input:  integer a, local factor p
##      output: [ e, b ] with a = p^e * b

def padic( a, p ):
    e = 0
    while a % p == 0:
        e += 1
        a //= p
    return [ e, a ]

##################################################################


##################################################################
##  Rabin's witness of non-primality
##      input:  integer a, possible witness integer x
##      output: 'probably prime' or 'composite', according to x

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
##  probabilistic primality test (Rabin)
##      input:  integer a
##      output: 'prime' or 'composite'
##  note:   for small a, the test is deterministic.
##          for large a, i have chosen to test 10
##          random witnesses, which gives the right
##          answer with probability > 1 - (.25)^10.

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
##  Pollard's rho algorithm for finding a factor of a
##      input:  integer a, initial seed x0, constant term n
##      output: either a nontrivial factor of a or a itself

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
##  factor-finding algorithm using varying seeds/polynomials
##      input:  composite integer a
##      output: nontrivial factor of a or 'error'
##  note:   based on some experimentation, the choices
##          below seem to yield a factor every time.
##          i have yet to receive the error message.

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
##  a list of small primes < 1000.
##      the primality testing function above was used to produce
##      this list.

SP = [   
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
    59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 
    191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 
    257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 
    401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 
    563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 
    631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 
    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
    797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 
    877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 
    967, 971, 977, 983, 991, 997                                ]

##################################################################


##################################################################
##  factoring algorithm
##      input:  integer _a
##      output: sorted list of prime factors of _a

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
        unfactored.remove(b)
        if probprime(b) == 'prime':
            prime_factors.append(b)
        else:
            d = find_factor(b)
            if d == 'error: no factor found':
                print( 'error: no factor found for', b )
                prime_factors.append(b)
            else:
                for c in [ d, b // d ]:
                    if probprime(c) == 'prime':
                        prime_factors.append(c)
                    else:
                        unfactored.append(c)
    return sorted(prime_factors)

##################################################################


##################################################################
##  print factorization
##      input:  integer a
##      output: none, but prints factorization

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
##  call the menu                                               ##

menu()

##################################################################
