"""
Utility for performing a single-day digital twinning run.
"""

import time

def twin_day(rbg: object, twinning_method: str, data: object, subject_info: dict, save_name: str, trace_name: str) -> None:
    """
    Perform single-day digital twinning using ReplayBG.
    Args:
        rbg: ReplayBG object, instantiated ReplayBG digital twin tool
        twinning_method: str, method for twinning ('map' or 'mcmc')
        data: pd.DataFrame, original data
        subject_info: dict, subject information including bw and u2ss
        save_name: str, name to save the twin
        trace_name: str, name of the trace for logging
    Returns:
        None
    """
    print("Twinning Tidepool " + trace_name + " data using " + twinning_method + " method.")
    
    # Run twinning procedure
    tic = time.perf_counter()
    rbg.twin(data=data, bw=subject_info['bw'], save_name=save_name,
             twinning_method=twinning_method,
             n_steps=50000, # ignored if twinning_method='map'
             parallelize=True, 
             u2ss=subject_info['u2ss'])
    toc = time.perf_counter()
    
    print(f"Single-day twinning with {twinning_method} for {trace_name} data completed in {toc - tic:0.3f} seconds.\n")
    return