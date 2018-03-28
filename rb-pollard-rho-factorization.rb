
#	written in ruby 2.4.1
#	Pollard's rho algorithm used for factorization into primes.


#	a simple prompt to demonstrate the factoring algorithm

def menu
	while 1 > 0
		puts
		puts "choose an option below:"
		puts "  enter a positive integer you would like factored;"
		puts "  enter 0 to factor 30 random integers;"
		puts "  or anything else to quit."
		puts
		z = gets
		z.chomp
		z = Integer(z) rescue false
		puts
		if z == false
			break
		else
			if z == 0
				for k in 6..20
					for i in 0..1
						a = 10**k + Random.rand( 10**(k+1) - 10**k + 1 )
						factorPrint( a )
					end
				end
			else
				factorPrint( z )
			end
		end
	end
end


#	greatest common divisor
#		input:	integers a, b
#		output:	greatest common divisor of a, b

def gcd( a, b )
	a = a.abs
	b = b.abs
	r = a % b
	if r == 0
		return b
	else 
		return gcd( b, [r, b-r].min ) 
	end
end


#	p-adic representation
#		input:	integer a, local factor p
#		output:	[ e, b ] with a = p^e + b

def padic( a, p )
	e = 0
	while a % p == 0
		e += 1
		a /= p
	end
	return [ e, a ]
end


#	modular exponentiation
#		input:	base a, exponent e, modulus m
#		output:	b = a^e mod m

def powmod( a, e, m )
	b = 1
	while e > 0
		if e % 2 == 1
			b = (b * a) % m
		end
		a = (a * a) % m 
		e /= 2
	end
	return b
end


#	Rabin's witness of non-primality
#		input:	integer a, possible witness integer x
#		output:	"probably prime" or "composite", according to x

def witness( a, x )
	l, m = padic( a-1, 2 )
	x = powmod( x, m, a )
	
	if x % a ==  1 || x % a == a-1
		return "probably prime"
	end
	
	for i in 1..l
		x = powmod( x, 2, a )
		
		if x % a == a - 1
			return "probably prime"
		elseif x % a == 1
			return "composite"
		end
	end
	
	return "composite"
end


#	probabilistic primality test (Rabin)
#		input:	integer a
#		output:	"prime" or "composite"
#	note:	for small a, the test is deterministic.
#			for large a, i have chosen to test 10
#			random witnesses, which gives the right
#			answer with probability > 1 - (.25)^10.

def probPrime(a)
	witnesses = case a
		when 0...2047 then [ 2 ]
		when 2047...1373653 then [ 2, 3 ]
		when 1373653...25326001 then [ 2, 3, 5 ]
		when 25326001...3215031751 then [ 2, 3, 5, 7 ]
		when 3215031751...2152302898747 then [ 2, 3, 5, 7, 11 ]
		when 2152302898747...3474749660383 then [ 2, 3, 5, 7, 11, 13 ]
		when 3474749660383...341550071728321 then [ 2, 3, 5, 7, 11, 13, 17 ]
		else 10.times.map{ 2 + Random.rand(a-3) }
	end
	
	witnesses.each do |x|
		if witness(a,x) == "composite"
			return "composite"
		end
	end

	return "prime"
end


#	the polynomials we will use for finding factors will be
#	of the form x^2 + n for some n.
#		input:	integers, a, x, n
#		output:	( x^2 + n ) % a

def pollardFunction( a, x, n )
	return ( x*x + n ) % a
end


#	Pollard's rho algorithm for finding a factor of a
#		input:	integer a, initial seed x, constant term n
#		output:	either a nontrivial factor of a or a itself

def pollard( a, x, n )
	r = pollardFunction( a, x, n )
	rr = pollardFunction( a, r, n )
	d = gcd( r - rr, a )

	while d == 1
		r = pollardFunction( a, r, n )
		rr = pollardFunction( a, pollardFunction(a, rr, n), n )
		d = gcd( r - rr, a )
	end

	return d
end


#	factor-finding algorithm using varying seeds/polynomials
#		input:	composite integer a
#		output:	nontrival factor of a or "error"
#	note:	based on some experimentation, the choices
#			below seem to yield a factor every time.
#			i have yet to receive the error message.

def findFactor( a )
	constantTerms = [ 1, 2, -1 ]
	seeds = [ 2, 3, 5, 6, 8 ]
	constantTerms.each do |n|
		seeds.each do |x|
			d = pollard( a, x, n )
			if d < a
				return d
			end
		end
	end
	print "error: no factor found of ", a
	return a
end


#	a list of small primes < 1000.  
#		the primality testing function above was used to 
#		produce this list.

SmallPrimes = [
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
	967, 971, 977, 983, 991, 997								]


#	factoring algorithm
#		input:	integer a
#		output:	sorted list of prime factors of a

def factor( a )
	a = a.abs
	if a == 0 || a == 1
		return [ a ]
	else
		primeFactors = []
		SmallPrimes.each do |p|
			if a % p == 0
				e, a = padic( a, p )
				for j in 1..e
					primeFactors << p
				end
			end
			if a == 1
				return primeFactors
			end
		end
		unfactored = []
		if probPrime( a ) == "prime"
			primeFactors << a
		else
			unfactored << a
		end
		while unfactored.length > 0
			b = unfactored[0]
			unfactored.delete_at(0)
			if probPrime( b ) == "prime"
				primeFactors << b
			else
				d = findFactor(b)
				if d == b
					print "error: no factor found for ", b
					primeFactors << b
				else
					[ d, b / d ].each do |z|
						if probPrime( z ) == "prime"
							primeFactors << z
						else
							unfactored << z
						end
					end
				end
			end
		end
		primeFactors.sort!
		return primeFactors
	end
end


#	print factorization
#		input: integer a
#		output: none, but prints factorization

def factorPrint( a )
	factors = factor( a )
	fexp = []
	while !( factors.empty? )
		p = factors[0]
		e = factors.count(p)
		if e == 1
			fexp << p.to_s
		else
			fexp << p.to_s + "^" + e.to_s
		end
		factors -= [p]
	end
	print a.abs, " = ", fexp.join(" * "), "\n"
end


#	call the menu

if __FILE__ == $0
	menu
end


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


