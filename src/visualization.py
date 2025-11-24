"""
Visualization utilities for original, twinned, and comparative glucose-insulin data.
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_original_data(data: pd.DataFrame, output_folder: str, trace_name: str) -> tuple[plt.Figure, plt.Axes]:
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True,
                gridspec_kw={'height_ratios': [3, 1, 1]})

    ##### CGM #####
    axs[0].plot(data.t, data['glucose'], label='CGM', color='black', linestyle='-', marker='.', markersize=5)
    axs[0].set_ylabel('Glucose [mg/dL]')
    axs[0].set_title(f'Example original data')
    axs[0].legend(loc='upper right')
    axs[0].grid(True)
    axs[0].axhline(y=180, color='gold', alpha=0.5, linestyle='--')
    axs[0].axhline(y=70, color='darkred', alpha=0.5, linestyle='--')
    
    ##### CHO #####
    axs[1].bar(data.t, data['cho'].fillna(0), color='deepskyblue', width=0.01, label='CHO')
    axs[1].set_ylabel('CHO [g]')
    axs[1].legend(loc='upper right')
    axs[1].grid(True)
    
    # Annotate cho_label
    labeled = data[data['cho_label'].notna()][['cho_label','t']].copy()
    labeled['ts'] = labeled.index

    for idx, row in data.iterrows():
        if row['cho'] > 0:
            # Find the nearest labeled point in time
            time_diff = abs(labeled['ts'] - idx)
            nearest_idx = time_diff.idxmin()
            label = labeled.loc[nearest_idx, 'cho_label']
            axs[1].text(data.t[idx], row['cho'] + 1, label, ha='center', va='bottom', fontsize=10, color='black')
    axs[1].set_ylim(0, data['cho'].max() + 3)

    ##### Insulin #####
    # Bolus insulin
    axs[2].bar(data.t, data['bolus'].fillna(0), color='limegreen', width=0.01)
    axs[2].set_ylabel('Bolus [U]')
    axs[2].legend(['Bolus'], loc='upper left')
    axs[2].grid(True)
    axs[2].set_ylim(0, data['bolus'].max() + 3)
    
    # Basal insulin
    ax2 = axs[2].twinx()
    ax2.plot(data.t, data['basal'], color='lime', linestyle='--', label='Basal Insulin')
    ax2.set_ylabel('Basal [U]')
    ax2.tick_params(axis='y')
    ax2.legend(['Basal Insulin'], loc='upper right')

    # Final plot adjustments and saving
    plt.xlabel('Time')
    plt.tight_layout()

    save_name = f"original_data_plot_{trace_name}"
    plt.savefig(os.path.join(output_folder, f"{save_name}.png"))
    
    return fig, axs


def plot_twinned_data(rbg: object, twinning_method: str, original_data: pd.DataFrame, subject_info: dict, save_name: str, output_folder: str, trace_name: str) -> None:

    fig, axs = plot_original_data(original_data, output_folder, trace_name)

    # do some other plot in the same figure
    replay_results = rbg.replay(data=original_data, bw=subject_info['bw'], save_name=save_name,
                                n_replay=1,
                                twinning_method=twinning_method,
                                save_workspace=True,
                                save_suffix='_replay_twin')
    
    twinned_glucose = replay_results['glucose']['median']

    tt = pd.date_range(start=original_data['t'].min(), end=original_data['t'].max()+pd.Timedelta("4min"),freq="1min")
    axs[0].plot(tt, twinned_glucose, color='red', linestyle='-', marker='o', markersize=2, mfc='none', label='Digital twin')

    axs[0].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, f"twinned_data_plot_{trace_name}.png"))
    plt.close('all')
    

def plot_comparison(results: dict, output_folder: str, trace_name: str) -> None:
    
    fig, axs = plt.subplots(4, 1, figsize=(14, 10), sharex=True,
                gridspec_kw={'height_ratios': [5, 1, 1, 1]})

    tt = pd.date_range(start=results['Original data']['rbg_data'].t_data.min(), end=results['Original data']['rbg_data'].t_data.max()+pd.Timedelta("4min"),freq="1min")
    
    ##### CGM #####
    axs[0].plot(tt, results['Original data']['glucose']['median'], label='Baseline', color='black', linestyle='--', markersize=1)
    axs[0].plot(tt, results['Aleppo guidelines']['glucose']['median'], label='Aleppo guidelines', color='red', linestyle='-', marker='o', markersize=1)
    axs[0].plot(tt, results['drCORRECT algorithm']['glucose']['median'], label='drCORRECT algorithm', color='green', linestyle='-', marker='o', markersize=1)
    axs[0].axhline(y=180, color='gold', alpha=0.5, linestyle='--')
    axs[0].axhline(y=70, color='darkred', alpha=0.5, linestyle='--')
    
    axs[0].set_ylabel('Glucose [mg/dL]')
    axs[0].legend(loc='upper left')
    axs[0].grid(True)
    axs[0].set_ylim([39, 350])
    
    ##### CHO ##### (with CGM)
    ax0 = axs[0].twinx()
    ax0.bar(tt, results['Original data']['cho']['realizations'][0, :], color='deepskyblue', width=0.005, label='CHO')
    ax0.set_ylabel('CHO [g]')
    ax0.legend(loc='upper right')
    ax0.set_ylim([0, 120])
    
    ##### Insulin #####
    # Original data
    axs[1].bar(tt, results['Original data']['insulin_bolus']['realizations'][0, :], color='black', label='Original bolus', width=0.008)
    axs[1].set_ylabel('Bolus [U]')
    axs[1].legend(loc='upper left')
    axs[1].set_title('Original data insulin')
    axs[1].grid(True)
    axs[1].set_ylim(0, 5)
    
    ax1 = axs[1].twinx()
    ax1.plot(tt, results['Original data']['insulin_basal']['realizations'][0, :], color='black', linestyle='--', linewidth=0.8)
    ax1.set_ylabel('Basal [U]')
    ax1.tick_params(axis='y')
    ax1.legend(['Original basal insulin'], loc='upper right')
    ax1.set_ylim([0, 0.1])
    
    # Aleppo guidelines
    axs[2].bar(tt, results['Aleppo guidelines']['insulin_bolus']['realizations'][0, :], color='black', label='Bolus from data', width=0.008)
    axs[2].bar(tt, results['Aleppo guidelines']['correction_bolus']['realizations'][0, :], color='red', label='CIB', width=0.008)
    axs[2].set_ylabel('Bolus [U]')
    axs[2].set_title('Aleppo guidelines insulin')
    axs[2].legend(loc='upper left')
    axs[2].grid(True)
    axs[2].set_ylim(0, 5)
    
    ax2 = axs[2].twinx()
    ax2.plot(tt, results['Original data']['insulin_basal']['realizations'][0, :], color='black', linestyle='--', linewidth=0.8)
    ax2.set_ylabel('Basal [U]')
    ax2.tick_params(axis='y')
    ax2.legend(['Original basal insulin'], loc='upper right')
    ax2.set_ylim([0, 0.1])
    
    # drCORRECT algorithm
    axs[3].bar(tt, results['drCORRECT algorithm']['insulin_bolus']['realizations'][0, :], color='black', label='Bolus from data', width=0.008)
    axs[3].bar(tt, results['drCORRECT algorithm']['correction_bolus']['realizations'][0, :], color='green', label='CIB', width=0.008)
    axs[3].set_ylabel('Bolus [U]')
    axs[3].legend(loc='upper left')
    axs[3].grid(True)
    axs[3].set_ylim(0, 5)
    
    ax3 = axs[3].twinx()
    ax3.plot(tt, results['Original data']['insulin_basal']['realizations'][0, :], color='black', linestyle='--', linewidth=0.8)
    ax3.set_ylabel('Basal [U]')
    axs[3].set_title('drCORRECT algorithm insulin')
    ax3.tick_params(axis='y')
    ax3.legend(['Original basal insulin'], loc='upper right')
    ax3.set_ylim([0, 0.1])
    
    # Final plot adjustments and saving
    plt.xlabel('Time')
    plt.tight_layout()

    save_name = f"cib_comparison_plot_{trace_name}"
    plt.savefig(os.path.join(output_folder, f"{save_name}.png"))