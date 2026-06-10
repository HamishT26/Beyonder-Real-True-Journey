# v466A GMUT v4 x2 Web Execution-Readiness Source Overlay

- Phase: `v466A_GMUT_v4_x2`
- Phase start NZ: `2026-06-01T03:44:47+12:00`
- Prepared NZ: `2026-06-01T03:47:06+12:00`
- Start head/upstream: `1fb0197887c7d742b958d7a60fdfe325d733f67a`
- Start drift: `0 0`
- Web searches: `20`
- Claim ceiling: `EXECUTION_READINESS_NOT_EXECUTION`

## Source Clusters

| Cluster | Sources | Readiness requirement |
|---|---|---|
| Schema/provenance | [JSON Schema](https://json-schema.org/specification), [JSON Schema release notes](https://json-schema.org/latest/release-notes), [Bowtie](https://docs.bowtie.report/), [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Closed row shape, structured errors, and separated entity/activity/agent provenance. |
| Fixture/data quality | [pytest fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html), [pytest parametrization](https://pytest.org/en/8.1.x/how-to/fixtures.html), [Great Expectations](https://docs.greatexpectations.io/docs/0.18/reference/learn/terms/expectation), [Frictionless](https://framework.frictionlessdata.io/docs/framework/package.html) | Fixture dependencies, axes, expected outcomes, and result objects before execution. |
| SI/metrology | [BIPM SI](https://www.bipm.org/en/publications/si-brochure), [NIST SP 811](https://www.nist.gov/publications/guide-use-international-system-units-si), [JCGM GUM](https://www.bipm.org/en/committees/jc/jcgm/wg/jcgm-wg1-gum), [VIM](https://www.iso.org/sites/JCGM/VIM/JCGM_200e_FILES/MAIN_JCGM_200e/02_e.html) | Quantity, unit, dimension vector, measurand, uncertainty, and detection-limit handling. |
| Metric/action and constraints | [GHY context](https://arxiv.org/abs/2304.06752), [MICROSCOPE](https://arxiv.org/abs/2209.15487), [CNES MICROSCOPE](https://cnes.fr/en/projects/microscope), [Eot-Wash](https://www.npl.washington.edu/eotwash/publications), [short-range gravity](https://arxiv.org/abs/2605.18212) | Boundary policy before variation and parameter-to-observable mapping before comparison. |
| Consciousness proxy controls | [COGITATE Nature](https://www.nature.com/articles/s41586-025-08888-1), [ARC-COGITATE](https://www.arc-cogitate.com/), [COGITATE data](https://cogitate-consortium.github.io/cogitate-data/), [OpenNeuro](https://docs.openneuro.org/git.html) | Task, modality, dataset/protocol route, false-positive controls, and non-proof boundary. |

This overlay establishes readiness requirements only. It does not run fixtures or close gates.
