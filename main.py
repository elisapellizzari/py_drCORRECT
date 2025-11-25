"""
Main script for running digital twin generation with and comparing corrective strategies on example CGM data. 
"""

import os

from py_replay_bg.py_replay_bg import ReplayBG

from src.visualization import plot_original_data, plot_twinned_data, plot_comparison
from src.twinning import twin_day
from src.utils import load_example_data, load_subject_info, retrieve_t_pers, save_comparison
from src.analysis import compare_corrective_strategies


def main(twin: bool = False, twinning_method: str = 'map', do_plot: bool = False):
    # 1. Load original data and set save_name
    trace_name = '0a1f30_05-07-2018'
    original_data = load_example_data(trace_name)
    subject_info = load_subject_info(trace_name)
    save_name = "cib_comparison_tidepool_" + trace_name
    save_folder=os.path.abspath("")

    if do_plot:
        plot_folder = os.path.abspath("plots")
        if not os.path.exists(plot_folder):
            os.makedirs(plot_folder)
        plot_original_data(original_data, plot_folder, trace_name)

    # 2. Instantiate ReplayBG digital twinning tool
    rbg = ReplayBG(
        blueprint="multi-meal", save_folder=save_folder,
        yts=5,
        seed=1,
        verbose=False, plot_mode=False
    )

    # 3. Optional twinning
    if twin:
        twin_day(rbg, twinning_method, original_data, subject_info, save_name, trace_name)
    if do_plot:
        plot_twinned_data(rbg, twinning_method, original_data, subject_info, save_name, plot_folder, trace_name)
        
    # 4. Retrieve personal parameters for drCORRECT
    t_pers = retrieve_t_pers(save_name, subject_info, save_folder, twinning_method)
    
    # 5. Compare corrective strategies
    results = compare_corrective_strategies(rbg, original_data, subject_info, t_pers, twinning_method, save_name, trace_name)
    save_comparison(results, os.path.join(save_folder, "results", "comparison_results"), trace_name, twinning_method)
    
    if do_plot:
        plot_comparison(results, plot_folder, trace_name, twinning_method)
    

if __name__ == "__main__":
    main(twin=False, do_plot=True)