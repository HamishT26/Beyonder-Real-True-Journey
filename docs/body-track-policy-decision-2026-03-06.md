# Body Policy Decision (2026-03-06)

Decision: keep the current Body policy file unchanged.

## Evidence reviewed

- `docs/body-track-calibration-latest.md`
- `docs/body-track-policy-delta-latest.md`
- `docs/body-track-policy-stress-latest.md`
- `docs/body-profile-policy-v1.json`

## Reasoning

The current decision rule is stricter than "take the live recommendation." A policy change is accepted only if it improves false-alert behavior in both:

1. the live-window calibration evidence, and
2. the stress-window evidence.

The current evidence does not meet that bar.

| Candidate change | Live-window signal | Stress-window signal | Decision |
| --- | --- | --- | --- |
| Tighten duration and loosen health thresholds for benchmark profiles | Acceptable in calibration, but `docs/body-track-policy-delta-latest.md` reports `action=keep` for all benchmark profiles | Stress report shows false-alert deltas increase under stressed conditions for quick, standard, and strict profiles | Reject |
| Move regression window from `{'window_size': 5, 'max_regressions': 2}` to `{'window_size': 7, 'max_regressions': 0}` | Calibration shows zero false alerts but higher alert rate | Stress report shows false-alert delta rises sharply from `0.375` to `1.000` | Reject |

## Result

- `docs/body-profile-policy-v1.json` remains the operative policy.
- No benchmark profile was updated.
- No regression window change was accepted.

## Next Body step

The next Body uplift should only be proposed after a candidate profile reduces false-alert behavior under both live and stress conditions. Until then, the correct action is to preserve the current policy and record the rejection explicitly.
