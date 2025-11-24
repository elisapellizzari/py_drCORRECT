"""
"""

import time

def twin_day(rbg, twinning_method, data, subject_info, save_name, trace_name):
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