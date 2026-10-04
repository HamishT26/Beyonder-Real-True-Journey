# Saelin run (2), x2: analytic and structural comparisons

Prepared before execution on 4 October 2026. The x1 source at commit
23831364ca31e6f8a185c3a30261767c814f172a remains unchanged. These are fifteen
refinements of its mathematical families, not fifteen newly discovered physical
laws. Default integration is RK4, duration 3.25 and 640 steps. Auxiliary
equilibrium and symmetry trajectories are recorded as additional executions of
the same family. The batch uses one local Node process and standard-library
dependencies. No cloud execution or independent scientific reproduction is
claimed for it.

1. **S01, flat null ray:** apply a Lorentz boost with beta 0.3 and verify the
   interval; test the same transform on a non-null event. An omitted-gamma
   transform must violate the relevant invariant. Units set c=1.
2. **S02, linear oscillator:** compare all six state components with independently
   evaluated trigonometric solutions at frequencies 1, sqrt(2), sqrt(3).
3. **S03, central quartic flow:** check the angular-momentum vector, time reversal
   and equivariance under a rotation about the z axis. RK4 is not asserted to be
   exactly reversible or symplectic.
4. **S04, damping:** compare with the exact underdamped solution, require monotone
   energy on sampled states, and integrate dissipated heat as a seventh variable
   to check the open-system energy balance.
5. **S05, driving:** use the nonresonant forced-oscillator solution. For the first
   coordinate, the particular coefficient is 0.4/(1-2^2). The homogeneous sine
   coefficient compensates for the particular solution's initial velocity.
   Compare integrated work with the analytic energy difference.
6. **S06, gyromotion:** compare position and velocity with integrated sine/cosine
   rotation at frequency 0.8, including the unaffected z motion. A sign-reversed
   magnetic force is a deliberately wrong control.
7. **S07, Kepler:** compare the specified unit-radius circular orbit to its exact
   sine/cosine solution and preserve the Runge-Lenz vector. This does not validate
   a collision integrator or every eccentric orbit.
8. **S08, diffusion:** the two positive eigenvalues are 1.1 +/- sqrt(0.07).
   Compare with the spectral polynomial on the zero-mean subspace and bound
   squared deviations using exp(-2 lambda t). A sign-reversed diffusion operator
   is an unstable control, not an admissible physical model.
9. **S09, lattice wave:** the uniform mode has frequency sqrt(0.4), while both
   zero-mean modes have frequency sqrt(3.4). Compare the full six-component state
   with this normal-mode decomposition.
10. **S10, reaction-gradient flow:** compare a uniform positive trajectory with
    u(t)=[1+(u0^-2-1) exp(-2t)]^-1/2. Check the gradient against a centered finite
    difference of the declared potential and verify its descent on sampled
    states. The chosen finite-difference tolerance is 2e-8.
11. **S11, Markov chain:** the stationary vector is (10,13,24)/47. Verify the
    stationary generator residual and fixed trajectory, plus contraction of the
    L1 distance between two distributions and approach to stationarity over a
    separately identified duration-20 trajectory.
12. **S12, logistic patches:** compare sampled minima and maxima with scalar
    logistic solutions initialized at the initial extrema. Verify a uniform
    trajectory against the exact scalar solution.
13. **S13, replicator:** check the equal-frequency fixed point and the independently
    linearized tangent-plane motion with frequency 1/sqrt(3). Perturbation is
    1e-6, duration one; the nonlinear-versus-linear error allowance is 1e-10.
    A dissipative linear approximation is an explicit wrong control.
14. **S14, mass action:** use the conserved A-B=0.6 and total=1.4 to reduce the
    initial trajectory to A'=2A^2-5.68A+3.2. Its two roots give an exact Riccati
    solution; only the smaller root lies in the admissible concentration region.
    Compare all species and check equilibrium flux.
15. **S15, spherical pendulum:** check vertical angular momentum, manifold and
    tangent residuals, and rotational equivariance. A free-fall system lacking
    the constraint reaction must leave the sphere. No exact pendulum trajectory
    or constraint-preserving integrator is claimed.

Unless overridden explicitly above, analytic vector comparisons allow absolute
error 2e-8 and invariant residuals 2e-8. Nonlinear time reversal allows 2e-7.
Every assertion stores the measured value, limit and outcome. Original failing
receipts must remain; repairs create a new attempt file. Expected faulty controls
are separately counted from failures of the intended model. Validation will not
rerun the old x1 test suite.

These comparisons support P01-P13, P16, P42, P46, P49 and P50 where the existing
model relationships apply. Mapping is not completion of those grand projects.
The companion learning disciplines are numerical analysis, differential
equations, analytical mechanics, probability, chemical kinetics, software
testing, systems engineering and research-methodology study. Four next studies:
interval numerics, symplectic integration, measurement-model identification and
resource-aware distributed execution. These are study topics, not qualifications.
