from Crypto.Util.number import GCD, getPrime
from random import randint
from typing import List, Tuple
from entity.elliptic_curve import ECCPoint


def get_random_relatively_prime_value(q: int) -> int:
    """
    Generate a random integer that is relatively prime to `q`.
    """
    while True:
        rand = randint(1, q - 1)
        if GCD(rand, q) == 1:
            return rand


def generate_random_rsa_key() -> Tuple[int, int, int]:
    """
    Generate a random RSA key pair (p, q, e).
    """
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        e = 65537
        if (p - 1) * (q - 1) % e != 0:
            return p, q, e


def hash_array_of_points(arr: List[ECCPoint], p: int) -> int:
    """
    Compute a hash value for an array of ECC points modulo `p`.
    """
    return sum(pow(point.x, point.y, p) for point in arr) % p


def generate_tuple(total: int, n: int) -> List[List[int]]:
    """
    Generate all possible tuples of size `n` that sum up to `total`.
    """
    if n == 1:
        return [[i] for i in range(total + 1)]

    result = []
    for i in range(total + 1):
        for sub_tuple in generate_tuple(total - i, n - 1):
            result.append([i] + sub_tuple)
    return result

if __name__ == '__main__':
    print(generate_tuple(4, 1))