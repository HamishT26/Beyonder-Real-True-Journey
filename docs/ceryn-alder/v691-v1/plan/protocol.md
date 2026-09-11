# Image-grid contracts

The reference values are frozen by direct finite enumeration or explicit rational formulas before a production implementation exists. Later executors must use independently written algorithms where feasible: prefix sums versus enumeration, traversal versus set merging, and streaming histograms versus bin filtering. A shared owner and language remain a limitation.

## Raster element layout

Derive planar element counts and row-major element strides; byte size and a real image format are deliberately unspecified. Session x1; body/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Pixel coordinate inverse

Map a finite row-major pixel address to its linear index and recover the exact coordinate. Session x1; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Half-open region intersection

Intersect two integer half-open rectangles, retaining empty intersections without negative area. Session x1; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Finite region union coverage

Enumerate the union of clipped integer cells once while retaining overlapping source coverage. Session x1; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Boolean mask run intervals

Encode true row spans as maximal half-open runs and retain exact foreground cardinality. Session x1; body/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Clipped grid neighborhood

Return only in-grid four or eight adjacent cells in row-major order, excluding the center. Session x1; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Summed-area rectangle query

Compare a prefix-table rectangle result with a frozen direct enumeration oracle. Session x1; mind/finite_sampling_and_intervals; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Center-based nearest sampling

Map destination cell centers to bounded source indices using an explicit floor convention. Session x1; mind/finite_sampling_and_intervals; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Quarter-cell bilinear weights

Keep four integer weight numerators over sixteen, preserving constants and convex support. Session x1; mind/finite_sampling_and_intervals; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Stencil support and padding

Distinguish refused missing stencil support from explicit zero padding; never invent an edge policy. Session x1; body/tiled_workload_and_release; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Partial-block sample means

Partition a finite plane into blocks and expose each sum and support count without fabricating edge samples. Session x2; body/tiled_workload_and_release; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Explicit histogram endpoints

Assign each finite value to left-closed bins, optionally closing the last edge, and retain excluded values. Session x2; mind/finite_sampling_and_intervals; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Four-connected mask regions

Separate orthogonally connected foreground components without joining diagonal contact. Session x2; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Exposed cell-face inventory

Count and identify exposed north east south west faces of a finite Boolean mask. Session x2; mind/image_grid_geometry; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Intensity tie ranks

Return dense or competition ranks while preserving original order and ties. Session x2; mind/finite_sampling_and_intervals; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Affine interval support

Propagate declared interval bounds through signed integer coefficients without claiming calibrated measurement uncertainty. Session x2; mind/finite_sampling_and_intervals; ceiling represented. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Declared grid-coordinate scale

Represent an explicitly declared dimensionless pixel scale while withholding physical calibration and measurement claims. Session x2; mind/finite_sampling_and_intervals; ceiling represented. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Text and symbol legend collisions

Expose empty labels and duplicate text or symbol cues so a color cue cannot silently become the sole distinction. Session x2; heart/uncertainty_communication; ceiling completed. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Visual uncertainty evaluation vacancies

Keep independent evaluation and affected-user evidence missing despite structurally complete synthetic review notes. Session x2; heart/uncertainty_communication; ceiling open_gap. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

## Image release obligation hold

Report missing provenance, license and review declarations while always withholding external publication authority. Session x2; heart/tiled_workload_and_release; ceiling exact_gate. Ten cases vary dimension, orientation, edge contact and support; exact requests and outputs are in definitions.json. Unknown fields are refused before calculation. Numeric inputs are safe bounded integers; fractional outputs use reduced numerator/denominator objects. A passing envelope does not promote the declared evidence ceiling.

Bounded same-owner synthetic software evidence only. No empirical GMUT, real THOS effectiveness, live Freed ID, professional, legal, cultural, affected-party or Maori authority, complete accessibility/privacy/security, independent reproduction, consciousness/personhood, AGI/ASI, Theory-of-Everything or Stage 20 claim. NOT_READY_FOR_STAGE_20.
