"""Generate routine-process figures + tables for the E.M.E.R.G.E+ manuscript."""

from __future__ import annotations

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from emerge_core import RoutineParams, RoutineConfig, simulate_routine, time_to_threshold, sample_at_times


def _ensure_outdir(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)


def main(outdir: str = "outputs") -> None:
    out = Path(outdir)
    _ensure_outdir(out)

    params = RoutineParams()
    cfg = RoutineConfig()

    res = simulate_routine(params, cfg)

    t = res["t_s"]
    H_e = res["H_e"]
    H_c = res["H_c"]
    E = res["E"]
    C = res["C"]
    Psi = res["Psi"]
    M = res["M_r"]

    # Figure 1: routine entropy trajectories
    plt.figure()
    plt.plot(t, H_e, label="H_e (emotional entropy proxy)")
    plt.plot(t, H_c, label="H_c (cognitive entropy proxy)")
    plt.xlabel("Time (s)")
    plt.ylabel("Arbitrary units")
    plt.title("Routine entropy trajectories (illustrative simulation)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "routine_entropy.png", dpi=200)
    plt.close()

    # Figure 2: routine meaning
    plt.figure()
    plt.plot(t, M, label="M_r (0–1)")
    plt.xlabel("Time (s)")
    plt.ylabel("Meaning (0–1)")
    plt.title("Routine meaning emergence (illustrative simulation)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "routine_meaning.png", dpi=200)
    plt.close()

    # Figure 3: routine inputs
    plt.figure()
    plt.plot(t, E, label="E (emotional energy input)")
    plt.plot(t, C, label="C (cognitive structure input)")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized input (0–1)")
    plt.title("Routine input signals (stylized)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "routine_inputs.png", dpi=200)
    plt.close()

    # Figure 4: cultural adaptation
    plt.figure()
    plt.plot(t, Psi, label="Ψ (cultural factor)")
    plt.xlabel("Time (s)")
    plt.ylabel("Ψ (0–1, arbitrary)")
    plt.title("Cultural adaptation in routine dynamics (stylized)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "routine_culture.png", dpi=200)
    plt.close()

    # Table: Demonstration 1 sampled points (0,2,5,10 s)
    sample_times = np.array([0.0, 2.0, 5.0, 10.0], dtype=float)
    He_s = sample_at_times(t, H_e, sample_times)
    Mr_s = sample_at_times(t, M, sample_times)

    table_demo1 = pd.DataFrame({
        "time_s": sample_times,
        "H_e": He_s,
        "M_r": Mr_s
    })
    table_demo1.to_csv(out / "table_demo1_routine_timepoints.csv", index=False)

    # Demonstration 3: cultural modulation (two group norms / baselines)
    # We keep everything identical except group norm and initial Ψ to mimic
    # 'restrained' vs 'expressive' conditions.
    def run_culture(psi0: float, S_group: float, seed_offset: int = 0):
        cfg2 = RoutineConfig(
            duration_s=cfg.duration_s,
            dt_s=cfg.dt_s,
            seed=cfg.seed + seed_offset,
            E_base=cfg.E_base,
            C_base=cfg.C_base,
            input_noise_sd=cfg.input_noise_sd,
            psi0=psi0,
            S_group=S_group,
            baseline_frac=cfg.baseline_frac,
        )
        r = simulate_routine(params, cfg2)
        t2 = r["t_s"]
        M2 = r["M_r"]
        return {
            "psi0": psi0,
            "S_group": S_group,
            "Psi_final": float(r["Psi"][-1]),
            "H_e_final": float(r["H_e"][-1]),
            "M_r_final": float(M2[-1]),
            "time_to_M_gt_0p35_s": float(time_to_threshold(t2, M2, 0.35)),
        }

    culture_rows = [
        run_culture(psi0=0.32, S_group=0.32, seed_offset=1),
        run_culture(psi0=0.68, S_group=0.68, seed_offset=2),
    ]
    table_culture = pd.DataFrame(culture_rows)
    table_culture.to_csv(out / "table_demo3_culture.csv", index=False)

    # Parameter sensitivity (vary alpha_E)
    alpha_values = [0.2, 0.4, 0.6]
    sens_rows = []
    for k, a in enumerate(alpha_values):
        p2 = RoutineParams(alpha_E=a)
        r2 = simulate_routine(p2, cfg)
        t2 = r2["t_s"]
        M2 = r2["M_r"]
        sens_rows.append({
            "alpha_E": a,
            "time_to_M_gt_0p40_s": float(time_to_threshold(t2, M2, 0.40)),
            "M_r_final": float(M2[-1]),
            "H_e_final": float(r2["H_e"][-1]),
        })
    table_sens = pd.DataFrame(sens_rows)
    table_sens.to_csv(out / "table_demo4_parameter_sensitivity.csv", index=False)

    # Full timeseries exports (for transparency)
    full = pd.DataFrame({
        "time_s": t,
        "E": E,
        "C": C,
        "Psi": Psi,
        "H_e": H_e,
        "H_c": H_c,
        "M_r": M,
    })
    full.to_csv(out / "routine_timeseries_full.csv", index=False)

    print(f"Saved routine outputs to: {out.resolve()}")


if __name__ == "__main__":
    main()
