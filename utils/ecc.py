def square_root(a: int, p: int) -> int:
    """
    Compute the square root of `a` modulo `p` using the Tonelli–Shanks algorithm.
    Returns 0 if no square root exists.
    """
    if legendre_symbol(a, p) != 1:
        return 0
    if a == 0:
        return 0
    if p == 2:
        return 0
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Factor p-1 as s * 2^e
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find a non-residue `n` modulo `p`
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Initialize variables for the algorithm
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        # Update variables
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a: int, p: int) -> int:
    """
    Compute the Legendre symbol (a/p).
    Returns 1 if `a` is a quadratic residue modulo `p`, -1 if it is a non-residue, and 0 if `a` is divisible by `p`.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls