"""Generate transformative-process figures + tables for the E.M.E.R.G.E+ manuscript."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from emerge_core import TransformativeParams, TransformativeConfig, simulate_transformative, sample_at_times


def _ensure_outdir(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)


def main(outdir: str = "outputs") -> None:
    out = Path(outdir)
    _ensure_outdir(out)

    params = TransformativeParams()
    cfg = TransformativeConfig()

    res = simulate_transformative(params, cfg)

    t = res["t_h"]
    D = res["D"]
    H_e = res["H_e"]
    E = res["E"]
    C = res["C"]
    M_t = res["M_t"]
    t_peak = float(res["t_peak_h"][0])

    # Figure 5: perturbation profile
    plt.figure()
    plt.plot(t, D, label="D(t) (stylized perturbation)")
    plt.axvline(t_peak, linestyle="--", label=f"t_peak = {t_peak:.2f} h")
    plt.xlabel("Time (h)")
    plt.ylabel("Perturbation (arb.u.)")
    plt.title("Transformative perturbation profile (stylized)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "transformative_drug_profile.png", dpi=200)
    plt.close()

    # Figure 6: biphasic entropy trajectory
    plt.figure()
    plt.plot(t, H_e, label="H_e(t)")
    plt.axvline(t_peak, linestyle="--", label="t_peak")
    plt.axhline(0.0, linestyle=":", label="baseline (H_e=0)")
    plt.xlabel("Time (h)")
    plt.ylabel("Arbitrary units")
    plt.title("Transformative biphasic entropy trajectory (illustrative)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "transformative_entropy.png", dpi=200)
    plt.close()

    # Figure 7: meaning trajectory (cumulative)
    plt.figure()
    plt.plot(t, M_t, label="M_t (normalized cumulative)")
    plt.axvline(t_peak, linestyle="--", label="t_peak")
    plt.xlabel("Time (h)")
    plt.ylabel("Cumulative meaning (0–1)")
    plt.title("Transformative meaning trajectory (illustrative)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "transformative_meaning.png", dpi=200)
    plt.close()

    # Optional: inputs used (E and C)
    plt.figure()
    plt.plot(t, E, label="E (stylized)")
    plt.plot(t, C, label="C (stylized)")
    plt.xlabel("Time (h)")
    plt.ylabel("Normalized (0–1)")
    plt.title("Transformative input signals (stylized)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "transformative_inputs.png", dpi=200)
    plt.close()

    # Table: key timepoints (0,1,2,3,4,5,6,8 h)
    sample_times = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0], dtype=float)
    He_s = sample_at_times(t, H_e, sample_times)
    Mt_s = sample_at_times(t, M_t, sample_times)

    table_demo2 = pd.DataFrame({
        "time_h": sample_times,
        "H_e": He_s,
        "M_t": Mt_s,
    })
    table_demo2.to_csv(out / "table_demo2_transformative_timepoints.csv", index=False)

    # Full timeseries exports
    full = pd.DataFrame({
        "time_h": t,
        "D": D,
        "E": E,
        "C": C,
        "H_e": H_e,
        "M_t": M_t,
    })
    full.to_csv(out / "transformative_timeseries_full.csv", index=False)

    meta = pd.DataFrame([{
        "t_peak_h": t_peak,
        "dt_h": cfg.dt_h,
        "duration_h": cfg.duration_h,
        "seed": cfg.seed,
    }])
    meta.to_csv(out / "transformative_metadata.csv", index=False)

    print(f"Saved transformative outputs to: {out.resolve()}")


if __name__ == "__main__":
    main()
