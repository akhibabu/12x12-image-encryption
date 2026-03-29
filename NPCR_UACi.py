#NPCR AND UACI .py

import numpy as np
from PIL import Image


# ============================================================
# LOAD IMAGE AS 12-BIT
# ============================================================

def load_image_12bit(path):
    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=np.uint16) * 16
    return arr


# ============================================================
# 12×12 S-BOX (deterministic shuffle)
# ============================================================

def generate_sbox(seed):

    rng = np.random.default_rng(int(seed * 1e6) % (2**32))
    S = np.arange(4096, dtype=np.uint16)
    rng.shuffle(S)

    S_inv = np.zeros(4096, dtype=np.uint16)
    for i in range(4096):
        S_inv[S[i]] = i

    return S, S_inv


# ============================================================
# BAKER MAP MASK (Paper Recurrence)
# ============================================================

def generate_mask(seed, N):

    p = seed % 1
    if p <= 0 or p >= 1:
        p = 0.3

    x = 0.5
    y = 0.5

    # warmup 512
    for _ in range(512):
        if x < p:
            x = x / p
            y = p * y
        else:
            x = (x - p) / (1 - p)
            y = 1 - (1 - p) * y

    mask = []

    for _ in range(N):

        if x < p:
            x = x / p
            y = p * y
        else:
            x = (x - p) / (1 - p)
            y = 1 - (1 - p) * y

        Mi = int((2**24 * x)) % 4096
        mask.append(Mi)

    mask = np.array(mask, dtype=np.uint16)
    return mask, mask[::-1]


# ============================================================
# PAPER ENCRYPTION
# Ci = S( M'i XOR S( Mi XOR S(Ii) ) )
# ============================================================

def encrypt_paper(P, S, mask, mask_flip):

    N = len(P)
    C = np.zeros(N, dtype=np.uint16)

    for i in range(N):

        T1 = S[P[i]]
        T2 = (mask[i] ^ T1) & 0xFFF
        T3 = S[T2]
        T4 = (mask_flip[i] ^ T3) & 0xFFF
        C[i] = S[T4] & 0xFFF

    return C


# ============================================================
# PROPOSED ENCRYPTION (WITH CHAINING + 12-bit safe)
# ============================================================

def encrypt_proposed(P, S, mask, mask_flip):

    N = len(P)
    C = np.zeros(N, dtype=np.uint16)

    prev = 1234  # IV

    for i in range(N):

        Pp = (P[i] ^ prev) & 0xFFF

        S1 = S[Pp]
        X1 = (S1 ^ mask[i]) & 0xFFF

        S2 = S[X1]
        X2 = (S2 ^ mask_flip[i]) & 0xFFF

        Ci = S[X2] & 0xFFF

        C[i] = Ci
        prev = Ci

    return C


# ============================================================
# NPCR & UACI (12-bit correct)
# ============================================================

def npcr(img1, img2):
    diff = img1 != img2
    return np.sum(diff) / diff.size * 100


def uaci(img1, img2):
    return np.mean(np.abs(img1.astype(np.int32) - img2.astype(np.int32))) / 4096 * 100


# ============================================================
# RUN TEST
# ============================================================

orig = load_image_12bit("input.png")
shape = orig.shape
P = orig.flatten()
N = len(P)

# modify one pixel
mod = orig.copy()
mod[0,0] = (mod[0,0] + 1) % 4096
P_mod = mod.flatten()

K1 = 0.56789
K2 = 0.73452

# generate components
S, S_inv = generate_sbox(K1)
mask, mask_flip = generate_mask(K2, N)

# ============================================================
# FIXED-KEY DIFFERENTIAL TEST
# ============================================================

print("\n===== FIXED-KEY DIFFERENTIAL TEST =====")

C1_paper = encrypt_paper(P, S, mask, mask_flip)
C2_paper = encrypt_paper(P_mod, S, mask, mask_flip)

C1_prop = encrypt_proposed(P, S, mask, mask_flip)
C2_prop = encrypt_proposed(P_mod, S, mask, mask_flip)

C1_paper = C1_paper.reshape(shape)
C2_paper = C2_paper.reshape(shape)

C1_prop = C1_prop.reshape(shape)
C2_prop = C2_prop.reshape(shape)

print("\nPaper NPCR:", npcr(C1_paper, C2_paper))
print("Paper UACI:", uaci(C1_paper, C2_paper))

print("\nProposed NPCR:", npcr(C1_prop, C2_prop))
print("Proposed UACI:", uaci(C1_prop, C2_prop))


# ============================================================
# KEY-SENSITIVITY TEST
# ============================================================

print("\n===== KEY-SENSITIVITY TEST =====")

# Paper
S1a, _ = generate_sbox(0.56789)
mask1a, mask1a_flip = generate_mask(0.73452, N)
C1a = encrypt_paper(P, S1a, mask1a, mask1a_flip)

S1b, _ = generate_sbox(0.56790)
mask1b, mask1b_flip = generate_mask(0.73453, N)
C1b = encrypt_paper(P, S1b, mask1b, mask1b_flip)

C1a = C1a.reshape(shape)
C1b = C1b.reshape(shape)

print("\nPaper Key NPCR:", npcr(C1a, C1b))
print("Paper Key UACI:", uaci(C1a, C1b))

# Proposed
S2a, _ = generate_sbox(0.56789)
mask2a, mask2a_flip = generate_mask(0.73452, N)
C2a = encrypt_proposed(P, S2a, mask2a, mask2a_flip)

S2b, _ = generate_sbox(0.56790)
mask2b, mask2b_flip = generate_mask(0.73453, N)
C2b = encrypt_proposed(P, S2b, mask2b, mask2b_flip)

C2a = C2a.reshape(shape)
C2b = C2b.reshape(shape)

print("\nProposed Key NPCR:", npcr(C2a, C2b))
print("Proposed Key UACI:", uaci(C2a, C2b))
