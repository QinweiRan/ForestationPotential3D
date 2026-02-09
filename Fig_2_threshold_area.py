"""
This script generates Fig. 2 in Ran et al., showing forestation area distributions
across different climate zones as a function of:
- Panel A: Potential canopy height (m)
- Panel B: Potential tree cover (%)

Requirements:
    - Python >= 3.8
    - pandas >= 1.3
    - matplotlib >= 3.5

Author: QINWEI
Email: qwran@pku.edu.cn
Date: Jan. 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

#  SETTINGS
CONFIG = {
    # Input data paths
    "height_area_csv": "data/Fig2_H_AREA.csv",  
    "cover_area_csv": "data/Fig2_C_AREA.csv",  
    
    # Output settings
    "output_dir": "output/",
    "output_filename": "Fig2_forestation_area_curve.png",
    "output_dpi": 300,
    
    # Plot settings
    "figure_size": (16, 6),
    "line_width": 3.5,
    "font_size_label": 24,
    "font_size_tick": 24,
    "font_size_legend": 22,
    "font_size_panel_label": 28,
    
    # Threshold lines (dashed vertical lines)
    "height_threshold": 5,  
    "cover_threshold": 10,  
}

# Climate zone colors and labels
CLIMATE_ZONES = {
    "colors": ["#2BBAA3", "#CF756B", "#6A5DBE", "#F676B8"],
    "labels": ["Trop.", "Arid", "Temp.", "Conti."]
}

plt.rcParams['font.family'] = 'Arial'


# PLOTTING FUNCTIONS
def plot_area_curve(ax, df, xlabel, xticks, threshold, panel_label):
   
    colors = CLIMATE_ZONES["colors"]
    labels = CLIMATE_ZONES["labels"]
    
    # Plot each climate zone
    for i, (label, color) in enumerate(zip(labels, colors)):
        x_data = df.iloc[:, 0]
        y_data = df.iloc[:, i + 1]
        ax.plot(x_data, y_data, 
                label=label, 
                linewidth=CONFIG["line_width"], 
                color=color)
    
    # Axis labels and formatting
    ax.set_xlabel(xlabel, fontsize=CONFIG["font_size_label"])
    ax.set_ylabel('Forestation area (Mha)', fontsize=CONFIG["font_size_label"])
    ax.tick_params(axis='both', labelsize=CONFIG["font_size_tick"])
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)
    
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    
    ax.legend(bbox_to_anchor=(0.55, 0.5), 
              frameon=False, 
              fontsize=CONFIG["font_size_legend"])
    
    # Panel label
    ax.text(-0.16, 1.01, panel_label, 
            transform=ax.transAxes,
            fontsize=CONFIG["font_size_panel_label"], 
            fontweight='bold', 
            va='center', 
            ha='center')
    
    # Threshold line
    ax.axvline(x=threshold, color='gray', linestyle='--', linewidth=2)


def main():
  
    required_files = [
        CONFIG["height_area_csv"],
        CONFIG["cover_area_csv"]
    ]
    
    for filepath in required_files:
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Input file not found: {filepath}\n"
                f"Please update the CONFIG paths at the top of this script."
            )
    
    # Create output directory if it doesn't exist
    output_dir = Path(CONFIG["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading data...")
    df_height = pd.read_csv(CONFIG["height_area_csv"])
    df_cover = pd.read_csv(CONFIG["cover_area_csv"])
    
    fig, axes = plt.subplots(1, 2, figsize=CONFIG["figure_size"])
    fig.subplots_adjust(wspace=0.3)
    
    # Panel A: Height vs Area
    plot_area_curve(
        ax=axes[0],
        df=df_height,
        xlabel='Potential canopy height (m)',
        xticks=[0, 5, 10, 20],
        threshold=CONFIG["height_threshold"],
        panel_label='A'
    )
    
    # Panel B: Cover vs Area
    plot_area_curve(
        ax=axes[1],
        df=df_cover,
        xlabel='Potential tree cover (%)',
        xticks=[0, 10, 30, 60],
        threshold=CONFIG["cover_threshold"],
        panel_label='B'
    )
    
    output_path = output_dir / CONFIG["output_filename"]
    print(f"Saving figure to: {output_path}")
    plt.savefig(output_path, dpi=CONFIG["output_dpi"], bbox_inches='tight')
    
    print("Figure generation complete!")
    plt.show()


if __name__ == "__main__":

    main()

