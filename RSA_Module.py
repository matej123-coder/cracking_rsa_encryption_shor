
from math import sqrt, gcd
import random
from random import randint as rand

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def isprime(n):
    if n < 2:
        return False

    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True

def generate_keypair(keysize):
    # Desired range for n = p * q
    nMin = 1 << (keysize - 1)
    nMax = (1 << keysize) - 1

    # Generate all primes that could reasonably be factors of n
    limit = int(sqrt(nMax)) + 10
    primes = [i for i in range(2, limit + 1) if isprime(i)]

    valid_pairs = []

    # Find every pair of distinct primes whose product has the correct bit length
    for i in range(len(primes)):
        for j in range(i + 1, len(primes)):
            p = primes[i]
            q = primes[j]
            n = p * q

            if nMin <= n <= nMax:
                valid_pairs.append((p, q))

    if not valid_pairs:
        raise ValueError(f"No valid prime pairs found for keysize={keysize}")

    # Pick one pair randomly
    p, q = random.choice(valid_pairs)

    print(f"Chosen primes: p = {p}, q = {q}")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose a public exponent e
    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    # Compute private exponent
    d = pow(e, -1, phi)

    return ((e, n), (d, n))
    
def encrypt(msg_plaintext, package):
    e, n = package
    msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
    return ''.join(map(lambda x: str(x), msg_ciphertext)), msg_ciphertext

def decrypt(msg_ciphertext, package):
    d, n = package
    msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
    return (''.join(msg_plaintext))