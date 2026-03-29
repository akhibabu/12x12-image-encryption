#PROPOSED METHOD.py

prop_code = r''
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# -------------------------------
# Logistic map generator
# -------------------------------
def logistic_sequence(seed, length, discard=500):
    r = 3.99
    x = seed % 1
    seq = []
    for _ in range(length + discard):
        x = r * x * (1 - x)
        seq.append(x)
    return seq[discard:]


# -------------------------------
# Dynamic 12-bit S-box generator
# -------------------------------
def generate_sbox(seed):

    chaos = logistic_sequence(seed, 6000)

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

    # Fisher–Yates shuffle using chaotic indices
    for i in range(4095, 0, -1):
        j = unique[i] % (i + 1)
        S[i], S[j] = S[j], S[i]

    S = np.array(S, dtype=np.uint16)

    # inverse S-box
    S_inv = np.zeros(4096, dtype=np.uint16)
    for i in range(4096):
        S_inv[S[i]] = i

    return S, S_inv


# -------------------------------
# Hybrid chaotic mask generator
# -------------------------------
def generate_mask(seed, N):

    seq = logistic_sequence(seed, N + 1000)

    # baker-like scrambling approximation
    seq = seq[::-1]

    mask = np.array([int(v * 4096) % 4096 for v in seq[:N]], dtype=np.uint16)

    return mask, mask[::-1]


# -------------------------------
# Encryption
# -------------------------------
def encrypt_image(P, S, mask, mask_flip, IV=1234):

    N = len(P)
    C = np.zeros(N, dtype=np.uint16)

    prev = IV

    for i in range(N):

        Pp = P[i] ^ prev

        S1 = S[Pp]
        X1 = S1 ^ mask[i]

        S2 = S[X1]
        X2 = S2 ^ mask_flip[i]

        Ci = S[X2]

        C[i] = Ci
        prev = Ci

    return C


# -------------------------------
# Decryption
# -------------------------------
def decrypt_image(C, S, S_inv, mask, mask_flip, IV=1234):

    N = len(C)
    P = np.zeros(N, dtype=np.uint16)

    prev = IV

    for i in range(N):

        X2 = S_inv[C[i]]
        S2 = X2 ^ mask_flip[i]

        X1 = S_inv[S2]
        S1 = X1 ^ mask[i]

        Pp = S_inv[S1]

        P[i] = Pp ^ prev

        prev = C[i]

    return P


# -------------------------------
# Load image as 12-bit
# -------------------------------
def load_image_12bit(path):

    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=np.uint16)

    # convert 8-bit → 12-bit
    arr = arr * 16

    shape = arr.shape
    flat = arr.flatten()

    return flat, shape


# -------------------------------
# Save 12-bit image back to 8-bit
# -------------------------------
def save_image_12bit(flat, shape, path):

    arr = flat.reshape(shape)

    # convert back to 8-bit
    arr = (arr / 16).astype(np.uint8)

    Image.fromarray(arr).save(path)


# -------------------------------
# MAIN TEST PIPELINE
# -------------------------------
if __name__ == "__main__":

    image_path = "input.png"

    # ---- load image ----
    P, shape = load_image_12bit(image_path)
    N = len(P)

    # ---- keys ----
    K1 = 0.56789
    K2 = 0.73452

    # ---- generate components ----
    S, S_inv = generate_sbox(K1)
    mask, mask_flip = generate_mask(K2, N)

    # ---- encrypt ----
    C = encrypt_image(P, S, mask, mask_flip)

    save_image_12bit(C, shape, "encrypted.png")

    # ---- decrypt ----
    P_dec = decrypt_image(C, S, S_inv, mask, mask_flip)

    save_image_12bit(P_dec, shape, "decrypted.png")

    print("Encryption + Decryption complete.")
with open("encrypt.py","w") as f:
    f.write(prop_code)
