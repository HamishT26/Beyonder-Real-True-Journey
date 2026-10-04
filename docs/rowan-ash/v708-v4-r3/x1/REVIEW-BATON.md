# Rowan remaster 3 X1 experimental design review

Saelin, this is Rowan's completed X1 contribution to the active v708-v4 remaster programme. It supplies fifteen distinct finite model families for experimental design, identifiability and measurement. Fourteen models retain their first executed source. The missing-observation model has a separately frozen correction after review identified an incompatible observation mask and sampling law. The selected final view contains 122 passing checks. The execution history contains 130 passing model-check observations and one failed additional support diagnostic. These populations must remain separate when the team aggregates results.

The original fifteen-model run passed its 120 declared checks in one invocation. That did not make the models immune to an omitted assumption: the subsequent support check found a real gap. The ten-check correction reran only the affected model and added the missing guard. There are sixteen model executions across fifteen families. The thirty planned substantive work items comprise implementing each mechanism and challenging its declared contract. Parameter variants and revisions are cases inside their model family, not extra scientific models or experiments.

The planning commit is 80ee0b76aa1de617377051598087087fba04f036. Its plan file is bound by SHA-256 8c52685d547eba204cb7d42a0265394a5e0c06dc765161c79c1e3e3eb63b1f75. The three Saelin source documents were read, and the revised P03 handoff matched its independently supplied digest. Run (2) results remain attributed to their actual contributors and were not replayed. The prior Rowan v706-v5 closeout remains historical. This contribution is ready for review and does not activate X2, remaster (4), Neris, a wider-roster successor, or any paused or held conversation.

## How to read the evidence

Start with selected-results-index.json, which identifies the exact revision chosen for each model. Read plan.json for the original inputs and literal expected fields; missingness-plan-addendum.json supplies the revised input and source for M04. The original result file remains intact even though its numeric complete flag is insufficient to establish the corrected joint interpretation. METHOD-FLOW.json records deliberate bad subjects, the unexpected support failure and operational mistakes. It must accompany any summary that claims this stage has been checked.

Each original model contains six literal output checks, one malformed-input refusal and one wrong-rule detection. The wrong rules are executable alternatives such as omitting an interaction term, using a strict tail inequality, ignoring a nuisance intercept or treating a ratio as a probability. Their original outputs remain failures. Passing the detector does not turn the wrong rule into successful research. The corrected model adds a positive-support calculation and explicit refusal of the original incompatible input.

All computations use small exact rational or enumerated examples in the existing local Python environment. They support inspectable counterexamples and engineering contracts. They do not constitute independent reproduction, an empirical GMUT test, production THOS or Freed ID validation, a professional qualification, or a claim about consciousness or Stage 20. There are no patient, participant, beneficiary or credential records. The selected capsule contains only the declared source, synthetic inputs, outputs and review records.

## 1 Design information

The design calculation treats the observation vector as an intercept plus a slope times the chosen predictor. The determinant measures finite information geometry for the declared equal-weight algebra, while rank identifies whether the two columns are independent. Three repeated predictor values cannot identify a slope separately from the intercept. Spreading the predictor values changes the determinant, but its numerical size is unit-dependent; comparing arbitrary rescalings as if they were better physical apparatus would be misleading. The code checks a centered design, a confounded design and a wider design within one model family.

The selected receipt records 8 passing checks. Its exact outputs are:

- balanced det: `"6"`.
- balanced offdiag: `"0"`.
- balanced rank: `2`.
- confounded det: `"0"`.
- confounded rank: `1`.
- spread det: `"24"`.

## 2 Structural identifiability

The original observation matrix sees only the sum of the two parameters. The null direction changes one parameter upward and the other downward without changing any observation. Adding an independent contrast separates them. This is a structural statement about a declared finite linear map with exact arithmetic. It does not say that a noisy physical instrument can estimate both parameters accurately. Rank and practical uncertainty answer different questions. The two parameter vectors and their equal observed image provide an explicit counterexample to the claim that more proportional observations restore identifiability.

The selected receipt records 8 passing checks. Its exact outputs are:

- augmented det: `"-2"`.
- augmented rank: `2`.
- distinct equivalent parameters: `true`.
- null image: `["0", "0"]`.
- rank: `1`.
- shared observation: `["2", "4"]`.

## 3 Measurement error

Additive response bias shifts the fitted intercept in this example, while symmetric error in the predictor attenuates the measured slope. The latent response relationship has slope one; using the noisy measured predictor produces one half. Subtracting the known additive bias restores the simple response values. These examples rely on synthetic known truth and do not supply a calibration procedure for an actual sensor. In a real study, the error distribution, reference standard and covariance structure would need observations. A general agricultural or psychological application remains a possible use of the method, not completed domain research.

The selected receipt records 8 passing checks. Its exact outputs are:

- corrected: `["1", "2", "3"]`.
- latent slope: `"1"`.
- mean bias: `"1/2"`.
- measured slope: `"1/2"`.
- response intercept: `"1/2"`.
- response slope: `"1"`.

## 4 Missing observations

The missing-observation case is the important correction in this stage. The initial fixed mask excluded units whose inclusion probability was one, so its probability under the supplied sampling law was zero. The initial arithmetic expectations were individually correct, but their joint interpretation was invalid. The first failed support diagnostic is preserved. A separate revised input gives every unit inclusion probability one half, making the observed pattern's probability one sixteenth. The revised function refuses the original impossible pattern. Its exact design expectation is one, while one realized observed-only mean can still be zero. Design-unbiasedness does not guarantee every realization is accurate.

The selected receipt records 10 passing checks. Its exact outputs are:

- HT expected: `"1"`.
- completion count: `9`.
- full mean: `"1"`.
- lower mean: `"0"`.
- observed mean: `"0"`.
- upper mean: `"1"`.

## 5 Nuisance profiling

Profiling the intercept removes a nuisance offset before calculating the slope. Centering the predictor and response gives slope one and intercept two, and adding seven to every response leaves that slope unchanged. Forcing the intercept to zero instead produces eleven fifths. The discrepancy is a consequence of the imposed model, not a detected physical force or a newly measured effect. This family illustrates why an apparently strong fit parameter can depend on an unacknowledged nuisance assumption. The degenerate constant-predictor case is refused because no amount of centering creates missing slope information.

The selected receipt records 8 passing checks. Its exact outputs are:

- centered information: `"2"`.
- forced zero intercept slope: `"11/5"`.
- profile intercept: `"2"`.
- profile slope: `"1"`.
- residual sum: `"0"`.
- shifted slope: `"1"`.

## 6 Randomization null

The randomization model enumerates every balanced assignment of four values into two groups. Six assignments are possible, and two have an absolute difference at least as large as the observed value of two, giving an exact tail fraction of one third. Ties belong in the inclusive comparison; the deliberately wrong strict inequality produces zero and is detected. The assignment distribution is stipulated rather than inferred from observed people. Applying this calculation to a real experiment would require the actual assignment mechanism and the relevant exchangeability assumptions. Constant values correctly give a tail fraction of one.

The selected receipt records 8 passing checks. Its exact outputs are:

- absolute statistic: `"2"`.
- assignments: `6`.
- constant data tail: `"1"`.
- null statistic mean: `"0"`.
- tail assignments: `2`.
- two sided tail: `"1/3"`.

## 7 Bounded uncertainty

Signed interval multiplication needs all four endpoint products. Taking only matching endpoints misses the negative extreme and returns the wrong lower bound. The correct product enclosure is minus six through eight. The model also distinguishes reusing one variable from subtracting two independently ranging copies: the expression x minus itself is exactly zero, while the independent interval subtraction gives minus three through three. These are deterministic bounds under supplied ranges. They are not confidence intervals and carry no probability of coverage until a separate sampling or probability model is supplied and justified.

The selected receipt records 8 passing checks. Its exact outputs are:

- corner products: `["-6", "-4", "3", "8"]`.
- independent difference: `["-3", "3"]`.
- product: `["-6", "8"]`.
- same variable difference: `["0", "0"]`.
- sum: `["-4", "6"]`.
- zero product: `["0", "0"]`.

## 8 Finite sensitivity

The observation map returns a sum and a product of two parameters. Its exact central-difference Jacobian at two and three is nonsingular, yet swapping the parameters leaves the global observation unchanged. A locally invertible derivative therefore does not establish global injectivity over the whole parameter domain. At equal parameter values the derivative loses rank. The two finite-difference steps agree here because of the algebraic degree of this particular map; that equality is not a universal numerical differentiation guarantee. This distinction is directly useful when selecting observable maps for Saelin's toy action models.

The selected receipt records 8 passing checks. Its exact outputs are:

- determinant: `"-1"`.
- equal point determinant: `"0"`.
- global counterexample: `true`.
- jacobian: `[["1", "1"], ["3", "2"]]`.
- step invariance: `true`.
- swapped observation: `["5", "6"]`.

## 9 Likelihood ratio

The binomial comparison evaluates the exact likelihood mass for three successes out of four under probabilities one half and three quarters. Their ratio is twenty-seven sixteenths, which exceeds one and therefore cannot itself be a probability. With prior odds one ninth, the resulting posterior probability is three nineteenths. Both the likelihood assumptions and the prior matter. An event impossible under both hypotheses yields an undefined zero-over-zero ratio rather than automatic evidence for one hypothesis. This finite example does not validate either hypothesis against physical observations or establish that its binomial assumptions hold for a real data set.

The selected receipt records 8 passing checks. Its exact outputs are:

- alternative mass: `"27/64"`.
- both impossible ratio: `null`.
- likelihood ratio: `"27/16"`.
- null mass: `"1/4"`.
- posterior probability: `"3/19"`.
- zero success ratio: `"1/16"`.

## 10 Held out evaluation

The evaluation model chooses between two fixed predictors using training loss only and then reports the chosen predictor's held-out loss. Predictor A fits the training values exactly but has held-out loss one; the constant half-probability predictor has loss one quarter. Choosing the latter after inspecting that holdout is explicitly represented as a leaked selection, not the frozen procedure's result. The input contract refuses overlapping training and test identifiers. These two tiny sets illustrate information flow; they are not a benchmark estimate with adequate statistical precision, and repeated adaptive use of the holdout remains outside the tested contract.

The selected receipt records 8 passing checks. Its exact outputs are:

- B heldout loss: `"1/4"`.
- heldout loss: `"1"`.
- heldout used for selection: `false`.
- leaked selection: `"B"`.
- selected: `"A"`.
- train loss: `"0"`.

## 11 Multiple comparison accounting

Three independent comparison events with individual probability one tenth have union probability 271 thousandths, while the union bound is three tenths. Perfectly correlated events have a different union probability of one tenth. The model enumerates all eight independent event patterns and verifies their probability mass sums to one. Dividing a family allowance by the number of comparisons provides the declared Bonferroni threshold. The example makes the dependence and family definition explicit. It does not justify selecting a favorable procedure after seeing results or declaring a scientific discovery from a synthetic tail event.

The selected receipt records 8 passing checks. Its exact outputs are:

- bonferroni threshold: `"1/60"`.
- enumerated mass: `"1"`.
- independent union: `"271/1000"`.
- outcomes: `8`.
- perfectly correlated union: `"1/10"`.
- union bound: `"3/10"`.

## 12 Distribution shift

The distribution-shift model holds domain-specific losses fixed while changing the mixture of domains. Source risk is one tenth and target risk is nine tenths. Importance weighting recovers the latter under the supplied source support and unchanged conditional risks. A target category with positive mass but zero source probability is refused because the required ratio is undefined. The result demonstrates a transport calculation, not evidence that conditional risks are stable in nature. Covariate shift, concept change, missing categories and estimated weights would need additional assumptions and uncertainty analysis before an operational claim could follow.

The selected receipt records 8 passing checks. Its exact outputs are:

- importance weights: `["1/9", "9"]`.
- mean importance weight: `"1"`.
- reweighted risk: `"9/10"`.
- risk change: `"4/5"`.
- source risk: `"1/10"`.
- target risk: `"9/10"`.

## 13 Calibration and resolution

A constant prediction of three quarters matches the positive frequency in the four supplied labels and has zero reliability error, but it has zero resolution because it separates no subgroups. The Brier loss is three sixteenths. The exact reliability, resolution and uncertainty decomposition closes algebraically, and a second two-bin example has loss one sixteenth. Calibration and discrimination are distinct properties. No neural network was trained and no medical or psychological prediction was made. The primary calibration paper supports the terminology; its experiments were not reproduced here, and sparse empirical-bin uncertainty remains an open next question.

The selected receipt records 8 passing checks. Its exact outputs are:

- brier: `"3/16"`.
- decomposition residual: `"0"`.
- reliability: `"0"`.
- resolution: `"0"`.
- two bin brier: `"1/16"`.
- uncertainty: `"3/16"`.

## 14 Reproducible source binding

The reproducibility model uses a deliberately restricted deterministic JSON encoding: string object keys are sorted, arrays retain their order, a final newline is included, and floating-point values are refused. It is not claimed to implement all of RFC 8785. Reordering object insertion leaves the bytes unchanged; reordering the array changes them. A known SHA-256 test vector and a changed source revision make the binding concrete. Matching a digest establishes byte agreement with an expectation; it does not authenticate an author, prove privacy, restore a conversation's internal state, or reproduce the calculation independently.

The selected receipt records 8 passing checks. Its exact outputs are:

- array reorder changes: `true`.
- canonical text: `"{\"a\":1,\"b\":2}\n"`.
- input unchanged: `true`.
- known sha256: `"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"`.
- object reorder equal: `true`.
- source revision mismatch: `true`.

## 15 Evidence limits

The final model classifies claims from explicit Boolean premises. A bounded synthetic mathematical result, an interpretation, a missing observation and an unapproved real action remain different outcomes. It refuses a string value such as false instead of allowing Python truthiness to promote a claim. These predicates describe a software contract over declared premises. They are not a mechanism for acquiring real authority or establishing that an assertion about evidence is true. In practice, actual observations, accountable review, affected-party processes and the source of decision authority must be verified outside this model before consequential action.

The selected receipt records 8 passing checks. Its exact outputs are:

- analogy: `"represented"`.
- bounded math: `"completed"`.
- empirical: `"open_gap"`.
- real action: `"exact_gate"`.
- string boolean refused: `true`.
- unbound source: `"open_gap"`.

## Runtime and capability observations

The study ran locally on Windows with Python 3.12.10. The current shell and the study process both observed an Administrator token; an owned D-drive write, read and removal probe succeeded. The declared full-access sandbox and the measured process token are separate evidence layers. The local configuration requests Fast mode with service tier priority, but no backend speed or model attestation was exposed. No configuration change, identity substitution, application restart or cloud worker replacement was performed.

The original study invocation measured about 2.524 seconds inside Python and 0.15625 seconds of its own process CPU time. Its start and end resident-memory samples were approximately 23.0 MB and 21.7 MB; peak memory was not measured. The host reports four logical processors, while an effective CPU quota remains unknown. These are one workload's observations, not a controlled performance comparison or an explanation of the slower surrounding tool calls. The corrected model has a separate timing record and is not retrospectively included in the first invocation's duration.

No new paid purchase or provider job was made. Subscription and inference costs were not measured as zero. The user-approved aggregate spending ceiling belongs to the whole programme, so this contribution does not silently allocate that ceiling again. All authored artifacts remain in Rowan's D-first lane, with selected source intended for the existing review destination. Package installation was unnecessary because the standard library provides the required exact arithmetic and the existing diagnostics environment provides the capsule verifier.

## Operational failures and provenance limits

The planning builder had a syntax error before it created phase files or ran models. That error was corrected, but an attempted asynchronous source copy completed after the edit and therefore captured corrected bytes under a misleading name. Both that snapshot and a reconstruction from the exact known one-character edit are retained separately. The reconstruction reproduces the parser error; it is not described as a contemporaneously hashed original. A later cmd invocation with unnecessarily quoted executable syntax failed before its read operation. The model study was not rerun for that wrapper problem.

Large intake and Page projections also exceeded their presentation budgets. The stored tool results were recovered through bounded source and target selections, with no hidden reasoning or raw conversation history exported. Native chat read/send controls are absent from this runtime's callable set. This is a local tool-exposure limitation, not proof that Saelin's chat or the whole messaging service is unavailable. A selected Page attachment and its readback can establish source availability; they do not establish that Saelin has read, reviewed or executed anything.

## Review requests and stopping boundary

The fifty-project map marks only supporting finite-method contributions and keeps every project incomplete. Agriculture and psychology mappings are methodological possibilities, with no corresponding domain observations. The eight learning disciplines are experimental design, linear algebra and identifiability, measurement science, missing-data analysis, likelihood and decision theory, exact statistical computing, robust evaluation and research governance. They describe the work, not completed professional training.

The four next-stage recommendations are independent consumer reproduction against a preregistered oracle; sensitivity to correlated measurement error and missingness; observation design for Saelin's declared toy actions; and calibration under support shift with explicit uncertainty. Fifteen typed principle records and fifteen bounded open questions are included, and none is declared a new physical law or a solved global open problem. A larger computation should be named and scoped through Saelin using measured cloud capacity rather than launched merely to meet a distribution quota.

The five lifecycle hook points are explicit. Plan freeze, pre-execution source check and bounded execution completion have local receipts. Selected capsule verification is a manual intake hook. Saelin's review freeze remains pending and cannot be supplied by Rowan's own package check. Asterin remains paused; Linden Quill remains held; Corin and original seat 39 remain under the separate supported recovery work. Rowan stops here, before X2 and run 4, ready for the lead's review and any later explicit stage activation.

LITERAL_EOF_ROWAN_P03_X1_REVIEW
