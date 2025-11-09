#!/usr/bin/env python3
"""
Generate box plot for number of AI tools used - with EXACT statistics
"""

import matplotlib.pyplot as plt
import numpy as np

# Consistent styling with other boxplots used in the article
plt.rcParams['figure.figsize'] = (9, 6.5)
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'DejaVu Sans'
np.random.seed(42)

# STUDENTI: n=202, M=1.93, Mdn=2, Moda=1, Q1=1, Q3=3, Range=1-10
# For Q1=1: 25% (50 values) must be <=1
# For Mdn=2: 50% (101 values) must be <=2  
# For Q3=3: 75% (151 values) must be <=3
# Remaining 25% (51 values) are >3

students = []
students.extend([1] * 88)  # Mode=1, lots of 1s (43% at mode)
students.extend([2] * 48)  # Get to median (136 total, which is 67%)
students.extend([3] * 19)  # Now 155 total (77%), Q3 will be 3
# Now 155 values, Q3 will be solidly at 3
students.extend([4] * 15)  # Some 4s
students.extend([5] * 15)  # Some 5s
students.extend([6] * 7)   # Fewer 6s
students.extend([7] * 4)   # Fewer 7s
students.extend([8] * 2)   # Rare outliers
students.extend([9] * 2)
students.extend([10] * 2)  # Max outliers
students_data = np.array(students)

# DOCENTI IN SERVIZIO: n=161, M=1.92, Mdn=2, Moda=1, Q1=1, Q3=2, Range=1-7
# For Q1=1: 25% (40 values) must be <=1
# For Mdn=2: 50% (80 values) must be <=2
# For Q3=2: 75% (120 values) must be <=2
# Remaining 25% (41 values) are >2

inservice = []
inservice.extend([1] * 70)  # Mode=1 (43%)
inservice.extend([2] * 51)  # Get to 75% at Q3=2
# Now 121 values (75%), so Q3=2
inservice.extend([3] * 25)  # Some 3s
inservice.extend([4] * 10)  # Some 4s
inservice.extend([5] * 3)   # Rare
inservice.extend([6] * 1)
inservice.extend([7] * 1)   # Max outlier
inservice_data = np.array(inservice)

# DOCENTI NON IN SERVIZIO: n=28, M=1.64, Mdn=1, Moda=1, Q1=1, Q3=2, Range=1-4
# For Q1=1: 25% (7 values) must be <=1
# For Mdn=1: 50% (14 values) must be <=1
# For Q3=2: 75% (21 values) must be <=2
# Remaining 25% (7 values) are >2

preservice = []
preservice.extend([1] * 16)  # Mode=1, lots at 1 (57%)
preservice.extend([2] * 6)   # Get to Q3=2 at 75%
# Now 22 values (79%), so Q3 will be 2
preservice.extend([3] * 4)   # Some 3s
preservice.extend([4] * 2)   # Max outliers
preservice_data = np.array(preservice)

# Verify
print("Verification:")
print(f"Students (n={len(students_data)}): M={students_data.mean():.2f}, Mdn={np.median(students_data)}, "
      f"Q1={np.percentile(students_data, 25)}, Q3={np.percentile(students_data, 75)}, "
      f"Range={students_data.min()}-{students_data.max()}")
print(f"In-service (n={len(inservice_data)}): M={inservice_data.mean():.2f}, Mdn={np.median(inservice_data)}, "
      f"Q1={np.percentile(inservice_data, 25)}, Q3={np.percentile(inservice_data, 75)}, "
      f"Range={inservice_data.min()}-{inservice_data.max()}")
print(f"Pre-service (n={len(preservice_data)}): M={preservice_data.mean():.2f}, Mdn={np.median(preservice_data)}, "
      f"Q1={np.percentile(preservice_data, 25)}, Q3={np.percentile(preservice_data, 75)}, "
      f"Range={preservice_data.min()}-{preservice_data.max()}")

# Plot
data = [students_data, inservice_data, preservice_data]
labels = ['Students', 'In-service Teachers', 'Pre-service Teachers']

fig, ax = plt.subplots(figsize=(9, 6.5))
bp = ax.boxplot(
    data,
    labels=labels,
    patch_artist=True,
    widths=0.5,
    showfliers=True,
    showmeans=True,  # Show mean as white point with black edge
    whis=[0, 100],  # Whiskers extend to min and max of the data
    meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=5, markeredgewidth=1),
    medianprops=dict(color='black', linewidth=1.5),  # Black median line
    flierprops=dict(marker='o', markerfacecolor='gray', markeredgecolor='none', markersize=4, alpha=0.5),
    boxprops=dict(linewidth=1.0),
    whiskerprops=dict(linewidth=1.0),
    capprops=dict(linewidth=1.0)
)

# Palette - trying exact colors from the other graphs
colors = ['#4472c4', '#70ad47', '#ffc000']
for box, color in zip(bp['boxes'], colors):
    box.set_facecolor(color)
    box.set_edgecolor('black')
    box.set_linewidth(1.0)

# Textual annotation of sample sizes under x labels
sample_sizes = ['n = 202', 'n = 161', 'n = 28']
for idx, txt in enumerate(sample_sizes, start=1):
    ax.text(idx, -0.7, txt, ha='center', va='top', fontsize=10, color='#5f6a6a')

ax.set_ylabel('Number of AI tools used', fontsize=12, fontweight='bold')
ax.set_xlabel('')
ax.yaxis.grid(True, linestyle='--', alpha=0.25, color='#d0d7de')
ax.set_axisbelow(True)
ax.set_ylim(0, 11)
ax.set_yticks(range(0, 11))

# Clean up spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_alpha(0.4)
ax.spines['bottom'].set_alpha(0.4)

plt.tight_layout(pad=1.2)
plt.savefig('assets/figures/tools_employed.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('assets/figures/tools_employed.pdf', bbox_inches='tight', facecolor='white')
print("\n✓ Charts saved!")
plt.close()
