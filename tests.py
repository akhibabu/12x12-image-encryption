#TESTS.py

import numpy as np
from PIL import Image
import time
from paper_method import *
from encrypt import *

def load_image(path):
    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=np.uint16) * 16
    return arr.flatten(), arr.shape

def save(flat, shape, path):
    arr = (flat.reshape(shape) / 16).astype(np.uint8)
    Image.fromarray(arr).save(path)

def entropy(img):
    hist = np.histogram(img.flatten(), bins=4096)[0]
    p = hist / np.sum(hist)
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

P, shape = load_image("input.png")
N = len(P)

K1 = 0.56789
K2 = 0.73452

# PAPER
S1, S1_inv = generate_sbox(K1)
mask1, mask1f = generate_mask(K2, N)

t0 = time.time()
C_paper = encrypt_paper(P, S1, mask1, mask1f)
t_paper = time.time() - t0
save(C_paper, shape, "paper_cipher.png")

# PROPOSED
S2, S2_inv = generate_sbox(K1)
mask2, mask2f = generate_mask(K2, N)

t0 = time.time()
C_prop = encrypt_image(P, S2, mask2, mask2f)
t_prop = time.time() - t0
save(C_prop, shape, "proposed_cipher.png")

E_paper = entropy(C_paper)
E_prop = entropy(C_prop)

print("\n----- COMPARISON RESULTS -----")
print(f"Paper entropy:    {E_paper:.4f}")
print(f"Proposed entropy: {E_prop:.4f}")
print(f"Paper time:       {t_paper:.4f}s")
print(f"Proposed time:    {t_prop:.4f}s")
