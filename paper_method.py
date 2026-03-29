#PAPER METHOD.py

import numpy as np

def logistic(seed, n, discard=500):
    r = 3.99
    x = seed % 1
    seq = []
    for _ in range(n + discard):
        x = r * x * (1 - x)
        seq.append(x)
    return seq[discard:]


def generate_sbox(seed):
    chaos = logistic(seed, 6000)
    indices = [int(v * 4096) % 4096 for v in chaos]

    seen = set()
    unique = []

    for k in indices:
        if k not in seen:
            unique.append(k)
            seen.add(k)
        if len(unique) == 4096:
            break

    if len(unique) < 4096:
        missing = [i for i in range(4096) if i not in seen]
        unique.extend(missing)

    S = list(range(4096))

    for i in range(4095, 0, -1):
        j = unique[i] % (i + 1)
        S[i], S[j] = S[j], S[i]

    S = np.array(S, dtype=np.uint16)

    S_inv = np.zeros(4096, dtype=np.uint16)
    for i in range(4096):
        S_inv[S[i]] = i

    return S, S_inv


def generate_mask(seed, N):
    seq = logistic(seed, N + 1000)
    mask = np.array([int(v * 4096) % 4096 for v in seq[:N]], dtype=np.uint16)
    return mask, mask[::-1]


def encrypt_paper(P, S, mask, mask_flip):
    N = len(P)
    C = np.zeros(N, dtype=np.uint16)
    for i in range(N):
        Pp = S[P[i]]
        Ci = S[(Pp ^ mask[i]) ^ mask_flip[i]]
        C[i] = Ci
    return C


def decrypt_paper(C, S, S_inv, mask, mask_flip):
    N = len(C)
    P = np.zeros(N, dtype=np.uint16)
    for i in range(N):
        X = S_inv[C[i]]
        X ^= mask_flip[i]
        X ^= mask[i]
        P[i] = S_inv[X]
    return P
