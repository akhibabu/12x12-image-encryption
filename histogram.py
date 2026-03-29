#HISTOGRAM.py

# ============================================================
# Histogram Plot
# ============================================================

def plot_hist(img, title):

    plt.figure()
    plt.hist(img.flatten(), bins=100)
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()


print("\n===== HISTOGRAM ANALYSIS =====")

plot_hist(orig, "Original Image Histogram")
plot_hist(C1_paper, "Paper Cipher Histogram")
plot_hist(C1_prop, "Proposed Cipher Histogram")
