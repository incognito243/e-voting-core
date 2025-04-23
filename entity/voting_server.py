from entity.elliptic_curve import EllipticCurve, ECCPoint
from entity.types import IntPair, EccPointPair, ProofOfWork
from utils.math import get_random_relatively_prime_value, hash_array_of_points, generate_tuple
from typing import List, Dict, Tuple, Optional
import os


def _verify_message(message: int, signed_message: int, public_key: IntPair) -> bool:
    """Verify a signed message using the public key."""
    n, e = public_key.x, public_key.y

    if pow(signed_message, e, n) != message:
        raise ValueError("Invalid signed message.")

class ElectionData:
    def __init__(self):
        self.voter_public_key: List[IntPair] = []
        self.voter_vote: List[EccPointPair] = []
        self.voter_signed_message: List[EccPointPair] = []
        self.voter_prove_of_work: List[ProofOfWork] = []
        self.encrypted_package: List[EccPointPair] = []
        self.decrypted_package: List[ECCPoint] = []
        self.result_package: List[List[int]] = []
        self.results: Optional[List[int]] = None

class VotingServer:
    def __init__(self, _number_of_candidate: int, maximum_number_of_voter: int, value_a: int, value_b: int, value_p: int, value_order: int):
        self.number_of_candidate = _number_of_candidate
        self.maximum_number_of_voters = maximum_number_of_voter
        self.number_of_voter = 0
        self.votes: List[EccPointPair] = []
        self.results: Optional[List[int]] = None
        self.election_data = ElectionData()
        self._set_up(value_a, value_b, value_p, value_order)

    def _set_up(self, _value_a: int, _value_b: int, _value_p: int, _value_order: int):
        """Initialize the elliptic curve and related parameters."""
        self.elliptic_curve = EllipticCurve(
            a=_value_a,
            b=_value_b,
            p=_value_p
        )
        self.order = _value_order
        self._d = get_random_relatively_prime_value(self.order)
        self.P = self.elliptic_curve.gens()
        self.Q = self.elliptic_curve.multiply(self._d, self.P)
        self.M = [
            self.elliptic_curve.multiply(
                pow(self.maximum_number_of_voters + 1, i, self.order), self.P
            ) for i in range(self.number_of_candidate)
        ]

    def get_public_key(self) -> Dict:
        """Return the public key of the voting server."""
        return {
            "P": self.P,
            "Q": self.Q,
            "order": self.order,
            "elliptic_curve": self.elliptic_curve,
            "M": self.M
        }

    def cast_vote(self, vote: Tuple[
        EccPointPair,
        EccPointPair,
        IntPair,
        ProofOfWork,
    ]):
        """Cast a vote after verifying its validity."""
        encrypted_message, signed_message, public_key, proof_of_work = vote

        for i in range(2):
            _verify_message(encrypted_message.first.x, signed_message.first.x, public_key)
            _verify_message(encrypted_message.second.y, signed_message.second.y, public_key)

        if self._verify_vote(encrypted_message, proof_of_work):
            self.number_of_voter += 1
            self.votes.append(encrypted_message)
            self.election_data.voter_vote.append(encrypted_message)
            self.election_data.voter_signed_message.append(signed_message)
            self.election_data.voter_public_key.append(public_key)
            self.election_data.voter_prove_of_work.append(proof_of_work)




    def _verify_vote(self, encrypted_message: EccPointPair, proof_of_work: ProofOfWork) -> bool:
        """Verify the validity of a vote."""
        A, B, u, w = proof_of_work.A, proof_of_work.B, proof_of_work.u, proof_of_work.w
        P, Q = self.P, self.Q
        Ap, Bp = encrypted_message.first, encrypted_message.second

        if not all(len(lst) == self.number_of_candidate for lst in [A, B, u, w]):
            raise ValueError("Invalid proof of work dimensions.")

        for i in range(self.number_of_candidate):
            if A[i] != self.elliptic_curve.add(
                self.elliptic_curve.multiply(w[i], P),
                self.elliptic_curve.multiply(u[i], Ap)
            ):
                return False
            if B[i] != self.elliptic_curve.add(
                self.elliptic_curve.multiply(w[i], Q),
                self.elliptic_curve.multiply(u[i], self.elliptic_curve.sub(Bp, self.M[i]))
            ):
                return False

        challenge = hash_array_of_points(A + B, self.elliptic_curve.p)
        return challenge == sum(u)

    def open_vote(self) -> List[int]:
        """Open the vote and calculate the results."""
        sum_A = ECCPoint(0, 0, True)
        sum_B = ECCPoint(0, 0, True)

        for _vote in self.votes:
            sum_A = self.elliptic_curve.add(sum_A, _vote.first)
            sum_B = self.elliptic_curve.add(sum_B, _vote.second)

        self.election_data.encrypted_package.append(EccPointPair(sum_A, sum_B))
        decrypted_S = self.elliptic_curve.sub(
            sum_B,
            self.elliptic_curve.multiply(self._d, sum_A)
        )
        self.election_data.decrypted_package.append(decrypted_S)

        self.results = self._solve(decrypted_S, self.M, self.number_of_voter)
        self.election_data.result_package.append(self.results)
        self.election_data.results = self.results
        return self.results

    def _solve(self, decrypted_S: ECCPoint, M: List[ECCPoint], n: int) -> List[int]:
        """Solve the vote decryption to determine the results."""
        elliptic_curve = self.elliptic_curve
        mid = len(M) // 2
        left_size, right_size = generate_tuple(n, mid), generate_tuple(n, len(M) - mid)
        data = [dict() for _ in range(n + 1)]

        for tuple_ in left_size:
            cur_sum = 0
            pt = ECCPoint(0, 0, True)
            for i, count in enumerate(tuple_):
                cur_sum += count
                pt = elliptic_curve.add(pt, elliptic_curve.multiply(count, M[i]))
            data[cur_sum][pt] = tuple_

        for tuple_ in right_size:
            cur_sum = 0
            pt = ECCPoint(0, 0, True)
            for i, count in enumerate(tuple_):
                cur_sum += count
                pt = elliptic_curve.add(pt, elliptic_curve.multiply(count, M[i + mid]))

            target = elliptic_curve.sub(decrypted_S, pt)
            if target in data[n - cur_sum]:
                return data[n - cur_sum][target] + tuple_

        raise ValueError("Failed to solve the vote decryption.")

    def public_result(self) -> ElectionData:
        """Return the public election data."""
        return self.election_data


if __name__ == '__main__':
    from random import randint
    from pprint import pprint
    from entity.user import User
    import time

    number_of_candidate = 4
    value_a = 1268133167195989090596625406312984755854486256116
    value_b = 386736940269827655214118852806596527602892573734
    value_p = 1461501637330902918203684832716283019655932542983
    value_order = 1461501637330902918203684149283858612734394057783


    voting_server = VotingServer(
        _number_of_candidate=4,
        maximum_number_of_voter=200,
        value_a=int(value_a),
        value_b=int(value_b),
        value_p=int(value_p),
        value_order=int(value_order),
    )
    cnt = [0 for i in range(number_of_candidate)]
    now = time.time()
    for i in range(5):
        user = User("user_name", "name", "id")
        vote = randint(0, number_of_candidate - 1)
        cnt[vote] += 1
        user_vote = user.vote(vote, voting_server.get_public_key())
        voting_server.cast_vote(user_vote)
        print(f"Vote time: {time.time() - now}")

    print(f"Preprocess time: {time.time() - now}")
    now = time.time()
    print(cnt)
    print(voting_server.open_vote() == cnt)
    print(f"Opening vote time: {time.time() - now}")
    pprint(voting_server.public_result().voter_vote)
    pprint(voting_server.public_result().results)