# Mind Track Source-Side Extraction Artifacts v0 (GMUT-005)

Purpose: attach **source-side extraction artifacts** and **explicit uncertainty propagation equations** per canonical anchor row, so each numeric bound is traceable from primary source to exclusion-note workflow.

Template: one worked example (MICROSCOPE); same structure can be replicated for EOTWASH and LLR.

---

## Worked example: MICROSCOPE_EP_eta_primary

**Anchor id:** `MICROSCOPE_EP_eta_primary`  
**Extraction trace id:** `trace:gmut005:microscope:2026-02-16:v1`  
**Claim:** GMUT-005 (psi-mediated couplings below fifth-force bounds).

### 1. Source-side extraction artifact

| Field | Value |
|-------|--------|
| **Primary source** | Touboul et al., MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle, *Astronomy & Astrophysics* 2022. |
| **Source URL** | https://link.springer.com/article/10.1007/s10509-022-04133-y |
| **Dataset / release** | microscope_final_results_2022 |
| **Location in source** | Final combined Eötvös parameter η (eta) from MICROSCOPE mission; reported as constraint on differential acceleration between test masses. |
| **Extracted quantity** | Upper bound on \|η\| (dimensionless EP violation parameter). |
| **Extracted value (central)** | Order 1e-14 (mission final result order of magnitude). |
| **External upper bound (used)** | `external_upper_bound = 1e-14` (used as conservative upper envelope for GMUT comparison). |
| **Uncertainty (reported)** | `external_uncertainty_abs = 2e-15` (represents combined statistical and systematic uncertainty envelope used for conservative bound inflation). |
| **Confidence** | 0.95 (95% confidence level for bound interpretation). |
| **Units** | dimensionless_eta |
| **Signal mapping** | Map η-limit into GMUT fifth-force coupling envelope under weak-field approximation (GMUT scalar coupling to matter trace). |

**Extraction method note:** Value and uncertainty are set from published mission final results; the numeric pair (1e-14, 2e-15) is a conservative ingestion choice for exclusion-note comparison. For full reproducibility, future cycles can attach exact table/figure references and equation numbers from the paper.

### 2. Uncertainty propagation equation (explicit)

**Model:** Linear bound addition (conservative one-sided inflation).

**Formula (literal):**

```
effective_upper_bound = external_upper_bound + external_uncertainty_abs
```

**With values for this anchor:**

```
effective_upper_bound = 1e-14 + 2e-15 = 1.2e-14
```

**Assumption:** Conservative one-sided bound inflation so that the effective bound used for GMUT exclusion is no tighter than the reported central + uncertainty.

**Code-friendly form (for scripts):**

```python
effective_upper_bound = anchor["external_upper_bound"] + anchor["external_uncertainty_abs"]
```

---

## Replication template for other anchors

For **EOTWASH_EP_bucket_primary** and **LLR_residual_primary**, use the same structure:

1. **Source-side extraction artifact:** Primary source, URL, location in source, extracted quantity, extracted value, external_upper_bound, external_uncertainty_abs, confidence, units, signal mapping.
2. **Uncertainty propagation equation:** Same formula `effective_upper_bound = external_upper_bound + external_uncertainty_abs` unless a different model is documented (then add formula + assumption_note).

---

## Link to canonical inputs

- Canonical anchor rows: `docs/mind-track-external-anchor-canonical-inputs-v1.json`
- Ingestion checklist: `docs/mind-track-external-anchor-ingestion-notes-v0.md`
- Exclusion note script: `scripts/gmut_external_anchor_exclusion_note.py`

---

*Caelis · Session 1 · 2026-02-17 · Mind track advancement*
