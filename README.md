# drCORRECT algorithm

This repository contains Python scripts implementing **drCORRECT**, a novel algorithm for the preventive administration of postprandial corrective insulin boluses in type 1 diabetes management.

## Reference

Pellizzari E. et al., [*drCORRECT: An algorithm for the preventive administration of postprandial corrective insulin boluses in type 1 diabetes management*](https://doi.org/10.1177/19322968231123456), J Diabetes Sci Technol, 2023.


---

## Folder Structure
```
data/                       # Folder for data
src/                        # Folder fro upporting functions
│
├── analysis.py             # Replay analysis
├── handlers.py             # Correction bolus strategies
├── twinning.py             # Digital twin creation
├── utils.py                # Utility functions
└── visualization.py        # Plotting functions
main.py                     # Main script to run example workflows
```

---

## Overview

The main scripts allow you to:

- Load example CGM, insulin, and meal data along with subject information
- Create a digital twin of the patient
- Retrieve personalized timing parameters necessary for drCORRECT
- Compare baseline (original data with correction boluses removed) with Aleppo guidelines and drCORRECT algorithm

---


