"""
Analysis utilities to compare corrective insulin bolus strategies using replay simulations.
"""

from src.handlers import drCORRECT, standard_cib, aleppo

import pandas as pd
import numpy as np

from py_agata.variability import median_glucose
from py_agata.time_in_ranges import time_in_hyperglycemia


def compare_corrective_strategies(rbg: object, data: pd.DataFrame, subject_info: dict, t_pers: float, save_name: str, trace_name: str) -> dict:
    
    data_no_cib = data.copy()
    B_idx = np.where(data_no_cib['bolus_label'] == 'B')[0]
    C_idx = np.where(data_no_cib['bolus_label'] == 'C')[0]
    data_no_cib['bolus'][C_idx[C_idx > B_idx]] = 0  # remove correction boluses after breakfast from original data
    data_no_cib['bolus_label'][C_idx[C_idx > B_idx]] = ''
    
    print("Replaying Tidepool " + trace_name + " data with original CIB.")
    original_replay = rbg.replay(data=data_no_cib, bw=subject_info['bw'], save_name=save_name,
                                 n_replay=1,
                                 twinning_method='map',
                                 save_workspace=False
    )
    tt = pd.date_range(start=original_replay['rbg_data'].t_data.min(), end=original_replay['rbg_data'].t_data.max()+pd.Timedelta("4min"),freq="1min")
    df_res = pd.DataFrame(pd.DataFrame({
                            't': tt,
                            'glucose': original_replay['glucose']['median']
                        }))
    print('Mean glucose: %.2f mg/dl' % median_glucose(df_res))
    print('TAR: %.2f %% \n' % time_in_hyperglycemia(df_res))
    
    print("Replaying Tidepool " + trace_name + " data using Aleppo's guidelines.")
    aleppo_replay = rbg.replay(data=data_no_cib, bw=subject_info['bw'], save_name=save_name,
                                enable_correction_boluses=True,
                                correction_boluses_handler=aleppo,
                                correction_boluses_handler_params={'gt': subject_info['gt'], 'cf': subject_info['cf']},
                                save_suffix='_aleppo_replay',
                                n_replay=1,
                                twinning_method='map',
                                save_workspace=True
    )
    df_res = pd.DataFrame(pd.DataFrame({
                            't': tt,
                            'glucose': aleppo_replay['glucose']['median']
                        }))
    print('Mean glucose: %.2f mg/dl' % median_glucose(df_res))
    print('TAR: %.2f %% \n' % time_in_hyperglycemia(df_res))
    
    print("Replaying Tidepool " + trace_name + " data using drCORRECT algorithm...")
    drcorrect_replay = rbg.replay(data=data_no_cib, bw=subject_info['bw'], save_name=save_name,
                                enable_correction_boluses=True,
                                correction_boluses_handler=drCORRECT,
                                correction_boluses_handler_params={'gt': subject_info['gt'], 'cf': subject_info['cf'], 't_pers': t_pers},
                                save_suffix='_drcorrect_replay',
                                n_replay=1,
                                twinning_method='map',
                                save_workspace=True
    )
    df_res = pd.DataFrame(pd.DataFrame({
                            't': tt,
                            'glucose': drcorrect_replay['glucose']['median']
                        }))
    print('Mean glucose: %.2f mg/dl' % median_glucose(df_res))
    print('TAR: %.2f %% \n' % time_in_hyperglycemia(df_res))
    
    return {
        'Original data': original_replay,
        'Aleppo guidelines': aleppo_replay,
        'drCORRECT algorithm': drcorrect_replay}