#!/usr/bin/env python3
from PIL import Image
import numpy as np
from collections import Counter

img = Image.open('assets/figures/study_ai_usage.png')
pixels = np.array(img)

# Get dominant colors (excluding whites and transparents)
flat = pixels.reshape(-1, 4)
colors = [tuple(c) for c in flat if c[3] > 200 and not all(c[:3] > 240)]
counter = Counter(colors)

print('Top 10 dominant colors in study_ai_usage.png:')
for i, (color, count) in enumerate(counter.most_common(10), 1):
    r, g, b = color[:3]
    print(f'{i}. RGB({r:3d}, {g:3d}, {b:3d}) = #{r:02x}{g:02x}{b:02x} - count: {count}')
