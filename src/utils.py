"""
"""

import os
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

from py_agata.time_in_ranges import time_in_target, time_in_hyperglycemia, time_in_hypoglycemia
from py_agata.risk import gri
from py_agata.variability import mean_glucose, cv_glucose, std_glucose, std_glucose_roc

def load_example_data(name):
    data_path = os.path.join("data", f"Tidepool_{name}.csv")
    df = pd.read_csv(data_path)
    df['t'] = pd.to_datetime(df['t'])
    return df


def load_subject_info(name):
    data_path = os.path.join("data", f"Tidepool_{name}.csv")
    df = pd.read_csv(data_path)
    
    cf = df.bolus_cf.dropna().mean() if not None else 40
    gt = df.bolus_bg_target.dropna().mean() if not None else 120
    cr = df.bolus_cr.dropna().mean() if not None else 12
    
    bw = 70  # kg, assumed value
    
    u2ss = df.basal.mean() * 1000 / bw  # mU/kg/min
    
    return {'cf': cf, 'gt': gt, 'cr': cr, 'bw': bw, 'u2ss': u2ss}


def retrieve_t_pers(save_name, subject_info, save_folder, twinning_method='map'):
    if twinning_method == "map":
        data = pd.read_pickle(os.path.join(save_folder, "results", twinning_method, f"{twinning_method}_{save_name}.pkl"))
        model_parameters = data["draws"].copy()
    else:  # MCMC
        with open(os.path.join(save_folder, "results", twinning_method, f"{twinning_method}_{save_name}.pkl"), 'rb') as f:
            data_mcmc = pickle.load(f)
        data_mcmc = data_mcmc['draws']
        model_parameters = {
            outer_key: float(inner_dict['samples_1'][0]) 
            for outer_key, inner_dict in data_mcmc.items()
        }
        
    ka2 = model_parameters['ka2']
    ke  = 0.127
    kd  = model_parameters['kd']
    u2ss = subject_info['u2ss']  # basal steady-state input
    
    mP = {"ka2": ka2,
          "ke": ke,
          "kd": kd,
          "u2ss": u2ss}
    
    T_total = 1000
    x_mat = np.zeros((T_total, 3))
    insulin_input_delayed = np.ones(T_total) * u2ss
    insulin_input_delayed[:5] = u2ss + 1  # small bolus at the beginning
    
    x_mat[0,:] = np.array([u2ss/kd, u2ss/ka2, u2ss/ke])  # initial conditions: steady-state
    
    for k in range(1,T_total):
        x_mat[k,:] = replaybg_backward_euler_matlab_implementation(
                                            x_mat[k-1,:],
                                            insulin_input_delayed[k-1],
                                            mP)
        
    Ip = x_mat[:,2]
    t = np.arange(T_total)
    
    tmax = t[np.argmax(Ip)]
    
    # plt.plot(t, Ip)
    # plt.xlabel("Time")
    # plt.ylabel("Compartment 3")
    # plt.axvline(tmax, color='r', linestyle='--', label=f'Tmax: {tmax:.2f} min')
    # plt.legend()
    # plt.show()
    
    return tmax*1.5 if tmax*1.5 > 60 else 60


def replaybg_backward_euler_matlab_implementation(xkm1, INS, mP):
    """
    ReplayBG backward euler integration step from matlab version.
    Args:
        xkm1:  (3,) array of state variables
            [Isc1, Isc2, Ip]
        INS: (1,) array of insulin input [mU/kg/min or model units]
        mP:  dict or object with parameters (attributes):
             kd, ka1, ka2, ke
    Returns:
        xk: (3,) tensor
    """
    xk = np.zeros_like(xkm1)

    Isc1  = xkm1[0]
    Isc2  = xkm1[1]
    Ip    = xkm1[2]

    # Subcutaneous and plasma insulin kinetics
    xk[0] = (Isc1 + INS)/(1+mP["kd"])
    xk[1] = (Isc2 + mP["kd"]*xk[0])/(1+mP["ka2"])
    xk[2] = (Ip+mP["ka2"]*xk[1])/(1+mP["ke"])
    
    return xk


def save_comparison(results, save_folder, trace_name):
    df = pd.DataFrame(columns=['Original data', 'Aleppo guidelines', 'drCORRECT algorithm'], 
                      index=['TIR (%)', 'TAR (%)', 'TBR (%)', 'GRI (-)', 'Mean Glucose (mg/dl)', 'CV of Glucose (%)', 'STD of Glucose (mg/dl)', 'STD of Glucose ROC (mg/dl/min)'])
    
    for key, result in results.items():
        tt = pd.date_range(start=result['rbg_data'].t_data.min(), end=result['rbg_data'].t_data.max()+pd.Timedelta("4min"),freq="1min")
        df_res = pd.DataFrame(pd.DataFrame({
                            't': tt,
                            'glucose': result['glucose']['median']
                        }))
        
        df.at['TIR (%)', key] = time_in_target(df_res)
        df.at['TAR (%)', key] = time_in_hyperglycemia(df_res)
        df.at['TBR (%)', key] = time_in_hypoglycemia(df_res)
        df.at['GRI (-)', key] = gri(df_res)
        df.at['Mean Glucose (mg/dl)', key] = mean_glucose(df_res)
        df.at['CV of Glucose (%)', key] = cv_glucose(df_res)
        df.at['STD of Glucose (mg/dl)', key] = std_glucose(df_res)
        df.at['STD of Glucose ROC (mg/dl/min)', key] = std_glucose_roc(df_res)
    
    os.makedirs(save_folder, exist_ok=True)
    df.to_csv(os.path.join(save_folder, f"comparison_results_{trace_name}.csv"))
    
    return df
