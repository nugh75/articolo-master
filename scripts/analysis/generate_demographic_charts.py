#!/usr/bin/env python3
"""
Script per generare i 4 grafici demografici per l'articolo
con titoli semplificati (senza "across 4 groups")
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Aggiungi path per import
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup style
plt.style.use(['science', 'no-latex', 'grid'])
mpl.rcParams.update({
    'text.usetex': False,
    'mathtext.fontset': 'dejavusans',
    'font.family': 'DejaVu Sans',
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
})

# Paths
ROOT = Path(__file__).parent.parent
OUTPUT_DIR = ROOT / 'output' / 'exploratory'
ASSETS_DIR = ROOT / 'assets' / 'figures'
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Palette e ordine gruppi
ORDER = [
    'studenti - secondaria',
    'studenti - universitari',
    'insegnanti - non in servizio',
    'insegnanti - in servizio',
]

PALETTE = {
    'studenti - secondaria': 'red',
    'studenti - universitari': 'forestgreen',
    'insegnanti - in servizio': 'royalblue',
    'insegnanti - non in servizio': 'gold',
}

print("="*80)
print("GENERAZIONE GRAFICI DEMOGRAFICI PER ARTICOLO")
print("="*80)

# ===== 1. AGE DISTRIBUTION - BOX =====
print("\n1. Age distribution — box")

# Leggi dati età salvati
try:
    df_age = pd.read_csv(OUTPUT_DIR / 'violin_eta_data.csv')
    df_age['GruppoDettaglio'] = pd.Categorical(df_age['GruppoDettaglio'], categories=ORDER, ordered=True)
    
    # Calcola soglie outlier per gruppo
    stats = (
        df_age.groupby('GruppoDettaglio', observed=False)['Eta']
              .agg(q1=lambda s: s.quantile(0.25), q3=lambda s: s.quantile(0.75))
    )
    stats['iqr'] = stats['q3'] - stats['q1']
    stats['lower'] = stats['q1'] - 1.5 * stats['iqr']
    stats['upper'] = stats['q3'] + 1.5 * stats['iqr']
    thr = stats.reset_index()
    merged = df_age.merge(thr, on='GruppoDettaglio', how='left')
    outliers = merged[(merged['Eta'] < merged['lower']) | (merged['Eta'] > merged['upper'])][['GruppoDettaglio','Eta']]
    
    # Crea grafico
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    sns.boxplot(
        data=df_age, x='GruppoDettaglio', y='Eta', hue='GruppoDettaglio', dodge=False,
        showfliers=False, palette=PALETTE, order=ORDER, ax=ax
    )
    sns.stripplot(
        data=outliers, x='GruppoDettaglio', y='Eta', hue='GruppoDettaglio', dodge=False,
        order=ORDER, hue_order=ORDER, palette=PALETTE, jitter=0.08, size=2.6, marker='o', 
        alpha=0.7, linewidth=0, ax=ax
    )
    ax.set_xlabel('Gruppo')
    ax.set_ylabel('Età (anni)')
    ax.set_title('Age distribution — box')
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()
    ax.grid(True, axis='y', alpha=0.25)
    ax.set_axisbelow(True)
    plt.xticks(rotation=10, ha='right')
    sns.despine(ax=ax)
    plt.tight_layout()
    
    p_box_png = ASSETS_DIR / 'age_distribution_box.png'
    p_box_svg = ASSETS_DIR / 'age_distribution_box.svg'
    fig.savefig(p_box_png)
    fig.savefig(p_box_svg)
    plt.close(fig)
    print(f"   ✓ Salvato: {p_box_png}")
    
except Exception as e:
    print(f"   ✗ Errore: {e}")

# ===== 2. AGE DISTRIBUTION - VIOLIN =====
print("\n2. Age distribution — violin")

try:
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    sns.violinplot(
        data=df_age, x='GruppoDettaglio', y='Eta', hue='GruppoDettaglio', dodge=False,
        inner='quartile', cut=0, density_norm='width', palette=PALETTE, order=ORDER, ax=ax
    )
    ax.set_xlabel('Gruppo')
    ax.set_ylabel('Età (anni)')
    ax.set_title('Age distribution — violin')
    leg = ax.get_legend()
    if leg is not None:
        leg.remove()
    ax.grid(True, axis='y', alpha=0.25)
    ax.set_axisbelow(True)
    plt.xticks(rotation=10, ha='right')
    sns.despine(ax=ax)
    plt.tight_layout()
    
    p_violin_png = ASSETS_DIR / 'age_distribution_violin.png'
    p_violin_svg = ASSETS_DIR / 'age_distribution_violin.svg'
    fig.savefig(p_violin_png)
    fig.savefig(p_violin_svg)
    plt.close(fig)
    print(f"   ✓ Salvato: {p_violin_png}")
    
except Exception as e:
    print(f"   ✗ Errore: {e}")

# ===== 3. GENDER DISTRIBUTION =====
print("\n3. Gender distribution")

try:
    # Leggi conteggi salvati
    counts_gender = pd.read_csv(OUTPUT_DIR / 'counts_genere_per_gruppo.csv', index_col=0)
    
    # Crea stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Colori per genere
    colors_gender = {'Maschio': '#4575b4', 'Femmina': '#d73027', 'Non risponde': '#cccccc'}
    
    x_pos = np.arange(len(ORDER))
    width = 0.6
    bottom = np.zeros(len(ORDER))
    
    for gen in ['Maschio', 'Femmina', 'Non risponde']:
        if gen in counts_gender.columns:
            values = [counts_gender.loc[g, gen] if g in counts_gender.index else 0 for g in ORDER]
            ax.bar(x_pos, values, width, label=gen, bottom=bottom, color=colors_gender.get(gen, '#999'))
            bottom += values
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(ORDER, rotation=15, ha='right')
    ax.set_xlabel('Gruppo')
    ax.set_ylabel('Conteggio')
    ax.set_title('Gender distribution')
    ax.legend(loc='upper right', frameon=False)
    ax.grid(True, axis='y', alpha=0.25)
    ax.set_axisbelow(True)
    sns.despine(ax=ax)
    plt.tight_layout()
    
    p_gender_png = ASSETS_DIR / 'gender_distribution.png'
    p_gender_svg = ASSETS_DIR / 'gender_distribution.svg'
    fig.savefig(p_gender_png)
    fig.savefig(p_gender_svg)
    plt.close(fig)
    print(f"   ✓ Salvato: {p_gender_png}")
    
except Exception as e:
    print(f"   ✗ Errore: {e}")

# ===== 4. DISCIPLINARY AREA DISTRIBUTION =====
print("\n4. Disciplinary area distribution (STEM/Humanities)")

try:
    # Leggi conteggi salvati
    counts_area = pd.read_csv(OUTPUT_DIR / 'counts_area_per_gruppo.csv', index_col=0)
    
    # Crea stacked bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Colori per area
    colors_area = {'STEM': '#2ca02c', 'Umanistiche': '#ff7f0e', 'Non risponde': '#cccccc'}
    
    x_pos = np.arange(len(ORDER))
    width = 0.6
    bottom = np.zeros(len(ORDER))
    
    for area in ['STEM', 'Umanistiche', 'Non risponde']:
        if area in counts_area.columns:
            values = [counts_area.loc[g, area] if g in counts_area.index else 0 for g in ORDER]
            ax.bar(x_pos, values, width, label=area, bottom=bottom, color=colors_area.get(area, '#999'))
            bottom += values
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(ORDER, rotation=15, ha='right')
    ax.set_xlabel('Gruppo')
    ax.set_ylabel('Conteggio')
    ax.set_title('Disciplinary area distribution (STEM/Humanities)')
    ax.legend(loc='upper right', frameon=False)
    ax.grid(True, axis='y', alpha=0.25)
    ax.set_axisbelow(True)
    sns.despine(ax=ax)
    plt.tight_layout()
    
    p_area_png = ASSETS_DIR / 'area_distribution.png'
    p_area_svg = ASSETS_DIR / 'area_distribution.svg'
    fig.savefig(p_area_png)
    fig.savefig(p_area_svg)
    plt.close(fig)
    print(f"   ✓ Salvato: {p_area_png}")
    
except Exception as e:
    print(f"   ✗ Errore: {e}")

print("\n" + "="*80)
print("✓ COMPLETATO!")
print("="*80)
print(f"\nFile salvati in: {ASSETS_DIR}")
print("  1. age_distribution_box.png/.svg")
print("  2. age_distribution_violin.png/.svg")
print("  3. gender_distribution.png/.svg")
print("  4. area_distribution.png/.svg")
