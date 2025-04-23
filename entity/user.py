from entity.elliptic_curve import EllipticCurve, ECCPoint
from entity.types import ProofOfWork, EccPointPair
from entity.voting_server import IntPair
from utils.math import get_random_relatively_prime_value, generate_random_rsa_key, hash_array_of_points
from typing import Tuple, List, Dict

class User:
    def __init__(self, user_name: str):
        self._p, self._q, self._e = generate_random_rsa_key()  # private keys
        self._n = self._p * self._q  # public key
        self._phi = (self._p - 1) * (self._q - 1)  # private
        self._d = pow(self._e, -1, self._phi)  # private
        self.user_name = user_name

    def sign(self, message: int) -> int:
        """Sign a message using the private key."""
        return pow(message, self._d, self._n)

    def vote(self, candidate: int, server_public_key: Dict) -> Tuple[
        EccPointPair,
        EccPointPair,
        IntPair,
        ProofOfWork
    ]:
        """Generate a vote for a candidate."""
        order = server_public_key["order"]
        elliptic_curve = server_public_key["elliptic_curve"]
        assert isinstance(elliptic_curve, EllipticCurve)
        P = server_public_key["P"]
        Q = server_public_key["Q"]
        r = get_random_relatively_prime_value(order)
        M = server_public_key["M"]

        if candidate < 0 or candidate >= len(M):
            raise ValueError(f"Invalid candidate id: {candidate}")

        candidate_key = M[candidate]
        encrypted_message = EccPointPair(
            elliptic_curve.multiply(r, P),
            elliptic_curve.add(candidate_key, elliptic_curve.multiply(r, Q))
        )
        signed_message = EccPointPair(
            ECCPoint(self.sign(encrypted_message.first.x), self.sign(encrypted_message.first.y)),
            ECCPoint(self.sign(encrypted_message.second.x), self.sign(encrypted_message.second.y))
        )
        proof_of_work = self._generate_proof_of_work(candidate, r, encrypted_message, server_public_key)

        return encrypted_message, signed_message, self.get_public_key(), proof_of_work

    def _generate_proof_of_work(
        self, candidate: int, r: int, encrypted_message: EccPointPair, server_public_key: Dict
    ) -> ProofOfWork:
        """Generate proof of work for the vote."""
        Ap, Bp = encrypted_message.first, encrypted_message.second
        order = server_public_key["order"]
        elliptic_curve = server_public_key["elliptic_curve"]
        assert isinstance(elliptic_curve, EllipticCurve)
        P = server_public_key["P"]
        Q = server_public_key["Q"]
        M = server_public_key["M"]

        w = [get_random_relatively_prime_value(order) for _ in range(len(M))]
        u = [get_random_relatively_prime_value(order) for _ in range(len(M))]
        s = get_random_relatively_prime_value(order)

        A = [
            elliptic_curve.add(
                elliptic_curve.multiply(w[k], P),
                elliptic_curve.multiply(u[k], Ap)
            ) if k != candidate else elliptic_curve.multiply(s, P)
            for k in range(len(M))
        ]
        B = [
            elliptic_curve.add(
                elliptic_curve.multiply(w[k], Q),
                elliptic_curve.multiply(u[k], elliptic_curve.sub(Bp, M[k]))
            ) if k != candidate else elliptic_curve.multiply(s, Q)
            for k in range(len(M))
        ]

        challenge = hash_array_of_points(A + B, elliptic_curve.p)
        u[candidate] += challenge - sum(u)
        w[candidate] = s - u[candidate] * r

        return ProofOfWork(A, B, u, w)

    def get_public_key(self) -> IntPair:
        """Return the public key."""
        return IntPair(self._n, self._e)