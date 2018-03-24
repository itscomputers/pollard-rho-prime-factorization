import java.io.*;
import java.util.*;
import java.math.*;


public class PollardRhoFactorization {

    
    public static void main( String args[] ) throws IOException {
	
	PollardRhoFactorization prf = new PollardRhoFactorization();

	BufferedReader br = new BufferedReader( new InputStreamReader( System.in ) );

	String choice;
	
	while ( 1 > 0 ) {
	    System.out.println( );
	    System.out.println( "choose an option below:" );
	    System.out.println( "   enter a positive integer you would like factored;" );
	    System.out.println( "   enter 0 to factor 30 random integers;" );
	    System.out.println( "   or anything else to quit." );
	    System.out.println( );
	    choice = br.readLine();
	    System.out.println( );
	    
	    if ( prf.isBigInteger( choice ) ) {
		BigInteger c = new BigInteger( choice );
	
		if ( c.intValue() == 0 ) {
		    Random rnd = new Random();
		    BigInteger x;
		    BigInteger y = new BigInteger("2");
		    for( int j = 17; j < 62; j += 3 ) {
			for( int i = 0; i < 2; i++ ) {
			    x = new BigInteger( j, rnd );
			    y = y.add( x );
			    prf.factorPrint( y );
			}
		    }
		    System.out.println( );
		} else {
		    prf.factorPrint( c );
		    System.out.println( );
		}
	    } else {
		break;
	    }
	}
    }



    /* this is to test whether a string represents an integer
     */
    boolean isBigInteger( String s ) {
	int l = s.length();
	if ( l == 0 ) return false;
	for ( int j = 0; j < l; j++ ) {
	    char c = s.charAt(j);
	    if ( j == 0 && c == '-' ) {
		if ( l == 1 ) return false;
		else continue;
	    }
	    if ( Character.digit( c, 10 ) < 0 ) return false;
	}
	return true;
    }
    


    /* greatest common divisor function
     * input:	    integers a, b
     * output:	    gcd(a,b)				
     */
    BigInteger gcd( BigInteger a, BigInteger b ) {
	a = a.abs();
	b = b.abs();
	
	if ( b.equals(BigInteger.ZERO) ) {
	    return a;
	} else {
	    BigInteger r = a.mod(b);
	    r = r.min( b.subtract(r) );
	    return gcd( b, r );
	}
    }



    /* p-adic representation
     * input:	    integer a and prime p
     * output:	    {e, b} with a = p^e * b
     */
    ArrayList<BigInteger> padic( BigInteger a, BigInteger p ) {
	BigInteger e = new BigInteger("0");
	
	while ( ( a.mod(p) ).equals( BigInteger.ZERO ) ) {
	    e = e.add( BigInteger.ONE );
	    a = a.divide(p);
	}

	ArrayList<BigInteger> output = new ArrayList<BigInteger>( List.of(e,a) );
	return output;
    }



    /* Rabin's witness of non-primality
     * input:	    integer a, witness x
     * output:	    'probably prime' or 'composite',
     *		    according to a
     */
    String witness( BigInteger a, BigInteger x ) {
	BigInteger two = new BigInteger("2");
	BigInteger a1 = a.subtract(BigInteger.ONE);
	
	ArrayList<BigInteger> A = padic( a1, two );
	BigInteger m = A.get(1);
	int l = (A.get(0)).intValue();

	BigInteger X = x.modPow( m, a );
	
	if ( X.equals( BigInteger.ONE ) || X.equals( a1 ) ) {
	    return "probably prime";
	} else {
	    for ( int j = 0; j < l; j++ ) {
		X = X.modPow( two, a );
		if ( X.equals( a1 ) ) {
		    return "probably prime";
		} else if ( X.equals(BigInteger.ONE) ) {
		    return "composite";
		}
	    }
	}
	return "composite";
    }



    /* Probabilistic primality test
     *	    using Rabin's witness
     * input:	    integer a
     * output:	    'prime' or 'composite'
     * note:	    for small a, the test is deterministic
     *		    for large a, i have chosen to test
     *			10 random witnesses, which gives
     *			the right answer with probability
     *			greater than 1 - (.25)^10
     */
    String probPrime( BigInteger a ) {
	ArrayList<BigInteger> witnesses = new ArrayList<BigInteger>();

	BigInteger bd1, bd2, bd3, bd4, bd5, bd6, bd7;
	bd1 = new BigInteger( "2047" );
	bd2 = new BigInteger( "1373653" );
	bd3 = new BigInteger( "25326001" );
	bd4 = new BigInteger( "3215031751" );
	bd5 = new BigInteger( "2152302898747" );
	bd6 = new BigInteger( "3474749660383" );
	bd7 = new BigInteger( "341550071728321" );
	
	BigInteger two, three, five, seven, eleven, thirteen, seventeen;
	two	    = new BigInteger( "2" );
	three	    = new BigInteger( "3" );
	five	    = new BigInteger( "5" );
	seven	    = new BigInteger( "7" );
	eleven	    = new BigInteger( "11" );
	thirteen    = new BigInteger( "13" );
	seventeen   = new BigInteger( "17" );

	if ( a.compareTo(bd7) > 0 ) {
	    BigInteger v;
	    Random rnd = new Random();
	    while ( witnesses.size() < 10 ) {
		v = new BigInteger(a.bitLength(), rnd);
		if ( ( v.compareTo(a) < 0 ) && ( v.compareTo(two) >= 0 ) ) {
		    witnesses.add( v );
		}
	    }
	} else {
	    witnesses.add(two);
	    if ( a.compareTo( bd1 ) > 0 ) witnesses.add(three);
	    if ( a.compareTo( bd2 ) > 0 ) witnesses.add(five);
	    if ( a.compareTo( bd3 ) > 0 ) witnesses.add(seven);
	    if ( a.compareTo( bd4 ) > 0 ) witnesses.add(eleven);
	    if ( a.compareTo( bd5 ) > 0 ) witnesses.add(thirteen);
	    if ( a.compareTo( bd6 ) > 0 ) witnesses.add(seventeen);
	}
	for( BigInteger x : witnesses ) {
	    if ( witness(a, x) == "composite" ) {
		return "composite";
	    }
	}
	return "prime";
    }
    

    /* a list of small primes < 1000.  the primality testing
     * function above was used to produce this list, but it
     * is more efficient to have the list explicitly defined
     * instead of generated each time the class is called.
     */
    int[] smallPrimes = { 
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
	967, 971, 977, 983, 991, 997 
    };


    /* the polynomial's we will use for finding factors will be
     * of the form x^2 + n for some n.
     * input:	    integers a, x, n
     * output:	    ( x^2 + n ) % a
     */
    BigInteger pollardFunction( BigInteger a, BigInteger x, BigInteger n ) {
	return ( ( x.multiply(x) ).add(n) ).mod(a);
    }



    /* Pollard's rho algorithm for finding a factor of a
     * input:	    integer a, initial seed n, constant term n
     * output:	    either a nontrivial factor of a or a itself 
     * note:	    1 < d <= a, so it might not give
     */
    BigInteger pollard( BigInteger a, int x, int n ) {
	BigInteger X = BigInteger.valueOf(x);
	BigInteger N = BigInteger.valueOf(n);

	BigInteger r = pollardFunction(a, X, N);
	BigInteger R = pollardFunction(a, r, N);
	BigInteger d = gcd( r.subtract(R), a );

	while ( d.equals(BigInteger.ONE) ) {
	    r = pollardFunction(a, r, N);
	    R = pollardFunction(a, pollardFunction(a, R, N), N);
	    d = gcd( r.subtract(R), a);
	}
	return d;
    }



    /* factor-finding algorithm using varying seeds/polynomials
     * input:	    composite integer a
     * output:	    nontrivial factor of a, or 'error'
     * note:	    based on some experimentation,
     *		    the choices below of seeds and constant
     *		    terms seem to be both fast and complete.
     *		    i have yet to receive the error message.
     */
    BigInteger findFactor( BigInteger a ) {
	int[] constantTerms = {1, 2, -1};
	int[] seeds = {2, 3, 5, 6, 8};
	for ( int n : constantTerms ) {
	    for ( int x : seeds ) {
		BigInteger d = pollard(a, x, n);
		if ( d.compareTo(a) < 0 ) {
		    return d;
		}
	    }
	}
	System.out.println("Error: no factor found of " + a);
	return a;
    }



    /* factoring algorithm
     * input:	    integer a
     * output:	    sorted list of prime factors of a
     */
    ArrayList<BigInteger> factor( BigInteger a ) {
	ArrayList<BigInteger> primeFactors = new ArrayList<BigInteger>();
	a = a.abs();
	if ( a.equals(BigInteger.ZERO) || a.equals(BigInteger.ONE) ) {
	    primeFactors.add(a);
	    return primeFactors;
	} else {
	    for ( int P : smallPrimes ) {
		BigInteger p = BigInteger.valueOf(P);
		if ( ( a.mod(p) ).equals(BigInteger.ZERO) ) {
		    ArrayList<BigInteger> z = padic( a, p );
		    
		    int e = ( z.get(0) ).intValue();
		    for ( int j = 0; j < e; j++ ) {
			primeFactors.add(p);
		    }
		    
		    a = z.get(1);
		    if ( a.equals(BigInteger.ONE) ) return primeFactors;
		}
	    }
	    ArrayList<BigInteger> unfactored = new ArrayList<BigInteger>();
	    if ( probPrime(a) == "prime" ) {
		primeFactors.add( a );
	    } else {
		unfactored.add( a );
	    }
	    while ( !( unfactored.isEmpty() ) ) {
		BigInteger b = unfactored.get(0);
		unfactored.remove(b);
		if ( probPrime(b) == "prime" ) {
		    primeFactors.add( b );
		} else {
		    BigInteger d = findFactor(b);
		    if ( d.equals(b) ) {
		       System.out.println("Error: not fully factored: " + b);
		       primeFactors.add( b );
		    } else {
			BigInteger D = b.divide(d);
			if ( probPrime( d ) == "prime" ) primeFactors.add( d );
			else unfactored.add( d );
			if ( probPrime( D ) == "prime" ) primeFactors.add( D );
			else unfactored.add( D );
		    }
		}
	    }
	    return primeFactors;
	    
	}
    }



    /* print factorization
     * input:	    integer a
     * output:	    none, but prints factorization
     */
    void factorPrint( BigInteger a ) {
	ArrayList<BigInteger> F = factor(a);
	Set<BigInteger> primeFactors = new HashSet<BigInteger>( F );
	ArrayList<String> Fexp = new ArrayList<String>();
	while ( !( primeFactors.isEmpty() ) ) {
	    BigInteger p = Collections.min( primeFactors );
	    int e = Collections.frequency( F, p );
	    if ( e == 1 ) Fexp.add( String.valueOf( p ) );
	    else Fexp.add( String.valueOf( p ) + "^" + String.valueOf( e ) );
	    primeFactors.remove( p );
	}
	System.out.print( a.abs() + " = " );
	int l = Fexp.size();
	for ( int j = 0; j < l-1; j++ ) {
	    System.out.print( Fexp.get(j) + " * " );
	}
	System.out.println( Fexp.get(l-1) );
    }
}



















