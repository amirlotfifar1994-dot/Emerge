# E.M.E.R.G.E+ simulation package (theoretical demonstrations)

This folder contains a clean, fully reproducible implementation of the
simulations and figure/table generation described in the manuscript:

**THE E.M.E.R.G.E+ FRAMEWORK: A Theoretical Model for Meaning Emergence Through Dual Entropy Dynamics**

## What this code does

- Regenerates all **routine-process** figures:
  - `routine_entropy.png`
  - `routine_meaning.png`
  - `routine_inputs.png`
  - `routine_culture.png`
- Regenerates all **transformative-process** figures:
  - `transformative_drug_profile.png`
  - `transformative_entropy.png`
  - `transformative_meaning.png`
  - `transformative_inputs.png`
- Exports CSV tables that can be pasted into the manuscript:
  - `table_demo1_routine_timepoints.csv`
  - `table_demo2_transformative_timepoints.csv`
  - `table_demo3_culture.csv`
  - `table_demo4_parameter_sensitivity.csv`
- Exports full time series for transparency:
  - `routine_timeseries_full.csv`
  - `transformative_timeseries_full.csv`

## Important disclaimer

These outputs are **mathematical demonstrations** generated from
phenomenological equations with **hypothetical parameters**. They are **not**
empirical measurements from human participants.

## How to run

From this folder:

```bash
pip install -r requirements.txt
python generate_all.py
```

Outputs are written to `outputs/`.
