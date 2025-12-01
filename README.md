# drCORRECT: a proactive strategy to manage postprandial glycemia in type 1 diabetes
<p align="center">
<img src="drCORRECT_logo.png" height="350">
</p>

**drCORRECT** is an innovative, open-source Python implementation of a novel algorithm designed to **preventively administer corrective insulin boluses** after meals, offering a significant step forward in Type 1 Diabetes (T1D) management.

Stop chasing high blood sugar. Start **preventing it**.

## The problem — and how drCORRECT changes the game

| The challenge (standard care) | The **drCORRECT** advantage |
| :--- | :--- |
| **Reactive:** Correction boluses are given *after* hyperglycemia occurs. | **Proactive:** Calculates and suggests a corrective bolus *before* the spike gets out of range. |
| **Delayed Action:** Time-to-action is slowed, leading to prolonged high glucose levels. | **Timely Intervention:** Personalized timing ensures the insulin acts when it's needed most. |
| **Increased Burden:** Requires more frequent manual adjustments and stress for the user. | **Optimized Control:** A personalized, data-driven approach for smoother postprandial curves. |

---

## Quantifiable impact: data-driven results

In simulations using real patient data, the **drCORRECT** strategy lead to superior glycemic control compared to standard clinical practice and a baseline scenario, prioritizing **safety** while maximizing **efficacy**.

| Metric | Baseline | Aleppo Guidelines | **drCORRECT Algorithm** |
| :--- | :--- | :--- | :--- |
| **TIR (%)** (Time In Range) | 32.8 | 54.3 | 59.2 |
| **TAR (%)** (Time Above Range) | 67.2 | 45.7 | 40.8 |
| **TBR (%)** (Time Below Range) | 0.0 | 0.0 | 0.0 |
| **GRI (-)** (Glycemia Risk Index) | 86.5 | 51.0 | 40.3 |
| **Mean Glucose (mg/dl)** | 223.0 | 187.5 | 168.5 |

### Key takeaways:

* **Less hyperglycemia:** TAR reduced to **40.8%**, with a substantially lower mean glucose.
* **Improved safety:** Maintains **0% TBR**, while reducing **GRI** to 40.3.
* **Higher control:** TIR improved to **59.2%**, outperforming both baseline and guideline-based strategies.

---

## What’s inside the repository?

Everything you need to understand, reproduce, and extend the **drCORRECT** strategy:

* **Digital Twin Creation:** Build individualized metabolic models directly from CGM, insulin, and meal data using ReplayBG.  
* **Personalized Timing Extraction:** Retrieve subject-specific timing parameters that drive the proactive correction logic.
* **Replay Simulation:** Evaluate three scenarios side-by-side:  
  - Baseline (original data with corrections removed)  
  - Aleppo Guidelines  
  - **drCORRECT**  
* **Visualization Tools:** Easily plot and compare the outcomes of each strategy.


## Repository structure

```
data/                          # Example CGM, insulin, and meal data for demonstration.
results/                       # Output folder for results
│  └── mcmc/                   # Pre-generated digital twin parameters for the example.
│  └── comparison_results/     # Simulation comparison CSV.
plots/                         # Simulation comparison figures.
src/                           # Folder for supporting functions.
│
├── analysis.py                # Core logic for Replay Analysis and simulation comparison.
├── handlers.py                # Implementation of drCORRECT and other correction bolus strategies.
├── twinning.py                # Digital twin creation (using replayBG).
├── utils.py                   # Utility functions.
└── visualization.py           # Plotting functions.
main.py                        # Main script to run example workflows.
requiremnts.txt                # Project requirements.
```

---

## Getting started

### 1. Requirements
- Python 3.11+

### 2. Installation

```bash
git clone https://github.com/your-username/drCORRECT-algorithm.git
cd drCORRECT-algorithm

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
### **3. Run example workflow**

```bash
python main.py
```

---

## Reference & Citation

If you find this work valuable, please consider citing our original publication:

Pellizzari E. et al., [*drCORRECT: An algorithm for the preventive administration of postprandial corrective insulin boluses in type 1 diabetes management*](https://doi.org/10.1177/19322968231123456), J Diabetes Sci Technol, 2023.


## Contribute & Support

**This is an open-source project. Your contributions are welcome\!**

  * **Feedback:** Help us refine the algorithm's performance and accuracy.
  * **Documentation:** Improve clarity and usability for new users.
  * **New Features:** Suggest and implement new analysis or visualization tools.

