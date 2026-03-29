#CORRELATION.py

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# -------------------------------
# Load image as array
# -------------------------------
def load_image(path):
    img = Image.open(path).convert("L")
    return np.array(img, dtype=np.float32)


# -------------------------------
# Correlation function
# -------------------------------
def correlation(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    num = np.mean((x - x_mean) * (y - y_mean))
    den = np.sqrt(np.mean((x - x_mean)**2) * np.mean((y - y_mean)**2))

    return num / den


# -------------------------------
# Sample adjacent pixel pairs
# -------------------------------
def get_pairs(img, direction, samples=5000):

    h, w = img.shape

    xs = []
    ys = []

    for _ in range(samples):

        i = np.random.randint(0, h-1)
        j = np.random.randint(0, w-1)

        if direction == "horizontal":
            xs.append(img[i, j])
            ys.append(img[i, j+1])

        elif direction == "vertical":
            xs.append(img[i, j])
            ys.append(img[i+1, j])

        elif direction == "diagonal":
            xs.append(img[i, j])
            ys.append(img[i+1, j+1])

    return np.array(xs), np.array(ys)


# -------------------------------
# Plot scatter graph
# -------------------------------
def plot_scatter(x, y, title):

    plt.figure()
    plt.scatter(x, y, s=2)
    plt.title(title)
    plt.xlabel("Pixel value")
    plt.ylabel("Adjacent pixel value")
    plt.show()


# -------------------------------
# ANALYSIS FUNCTION
# -------------------------------
def analyze(path, name):

    img = load_image(path)

    print(f"\n--- {name} ---")

    for d in ["horizontal", "vertical", "diagonal"]:

        x, y = get_pairs(img, d)

        corr = correlation(x, y)

        print(f"{d.capitalize()} correlation: {corr:.6f}")

        plot_scatter(x, y, f"{name} - {d} correlation")


# -------------------------------
# RUN ANALYSIS
# -------------------------------
if __name__ == "__main__":

    analyze("input.png", "Original Image")
    analyze("encrypted.png", "Encrypted Image")
