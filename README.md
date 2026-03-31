# 12x12-image-encryption
# Enhanced 12-bit Chaotic Image Encryption

## Overview
This project implements an enhanced chaotic image encryption scheme designed for 12-bit medical images. The method improves upon an existing approach by introducing a chaining-based diffusion mechanism and a flipped mask strategy to enhance security.

---

## Objectives
- Support native 12-bit image encryption (4096 grayscale levels)
- Improve diffusion and avalanche effect
- Achieve high NPCR and UACI values
- Reduce pixel correlation in encrypted images

---

## Key Features
- Chaining-based diffusion (main contribution)
- Dynamic 12×12 S-box generation
- Chaotic mask generation using logistic map
- Flipped mask strategy
- Security analysis (NPCR, UACI, correlation, entropy)

---

## Methodology
1. Convert input image to 12-bit grayscale
2. Generate chaotic sequence using logistic map
3. Construct dynamic S-box
4. Generate mask and flipped mask
5. Apply substitution and masking
6. Apply chaining: # Enhanced 12-bit Chaotic Image Encryption

## Overview
This project implements an enhanced chaotic image encryption scheme designed for 12-bit medical images. The method improves upon an existing approach by introducing a chaining-based diffusion mechanism and a flipped mask strategy to enhance security.

---

## Objectives
- Support native 12-bit image encryption (4096 grayscale levels)
- Improve diffusion and avalanche effect
- Achieve high NPCR and UACI values
- Reduce pixel correlation in encrypted images

---

## Key Features
- Chaining-based diffusion (main contribution)
- Dynamic 12×12 S-box generation
- Chaotic mask generation using logistic map
- Flipped mask strategy
- Security analysis (NPCR, UACI, correlation, entropy)

---

## Methodology
1. Convert input image to 12-bit grayscale
2. Generate chaotic sequence using logistic map
3. Construct dynamic S-box
4. Generate mask and flipped mask
5. Apply substitution and masking
6. Apply chaining:Ci = S((Pi ⊕ Ci-1) ⊕ mask)
7. Produce cipher image

---

## Performance Metrics

| Metric       | Result |
|-------------|--------|
| Entropy     | ~11.94 |
| NPCR        | ~100%  |
| UACI        | ~33%   |
| Correlation | ~0     |

---

## Dataset
- 1 CT image
- 2 MRI images  
Source: https://www.dicomlibrary.com/

---

## Installation

```bash
pip install numpy pillow matplotlib
