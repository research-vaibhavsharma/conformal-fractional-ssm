# Conformal Fractional Symplectic State-Space Model
Official implementation of the Conformal Fractional Symplectic State-Space Model (CFS-SSM) for forecasting complex nonlinear dynamics and strange attractors.

* **Fractional Continuous-Time Latent Dynamics:** The architecture completely substitutes conventional integer-order derivatives with the Caputo fractional derivative within the continuous-depth differential equations governing the latent space. This native integration structurally accommodates complex fractional phase-space geometries, ensuring the retention of heavy-tailed anomalous diffusion and eradicating Markovian historical amnesia.


* **Hard Symplectic Lie Algebra Constraints:** By utilizing a Darboux block-diagonal indefinite parameterization, the internal transition matrices are strictly confined to the symplectic Lie algebra. This eliminates the reliance on soft, heuristic external loss penalties and inherently preserves localized exact Hamiltonian energy conservation, which permanently prevents numerical dissipation and Euclidean attractor collapse.


* **Hardware-Aware Multiscale Fractional Relaxation:** The methodology introduces a Modified Oustaloup Recursive Approximation (M-ORA) filter bank to bridge continuous anomalous diffusion with discrete execution. This hardware-aware approach translates infinite-horizon memory kernels into finite parallelizable sub-states, bypassing the computational intractability of traditional $\mathcal{O}(L^2)$ fractional integration to achieve strict $\mathcal{O}(L \log L)$ parallel scalability.


* **Resolution of the Symplectic-Dissipative Paradox:** The framework provides rigorous mathematical proofs of absolute topological stability for non-equilibrium systems. By decoupling reversible symplectic routing from macroscopic fractional dissipation, the model permanently bounds global phase-space variance over infinite horizons and enforces exact phase-space volume contraction.

## Architecture Overview
The Conformal Fractional Symplectic State-Space Model (CFS-SSM) is structurally partitioned into four distinct operational stages to map raw exogenous sequences to the global macroscopic state:   
* **Stage 1: Exogenous Sequence Embedding:** Raw empirical sequences possessing unbounded temporal variation are routed through a continuous Exponential Moving Average (EMA) low-pass filter. This explicitly bounds the temporal variation, forcing the embedded sequence into a globally Lipschitz continuous subspace.
* **Stage 2: Symplectic Hamiltonian Generator Core:** The network synthesizes a non-autonomous vector field utilizing a Darboux indefinite parameterization to ensure the transition matrices strictly inhabit the symplectic Lie algebra. A Symplectic Orthogonal Cascade, a Hyperbolic Boost, and a Block-Diagonal Saddle are synthesized into the core Hamiltonian $H_{\theta}$, enforcing a strict spectral clamp to govern the network's topological state.
* **Stage 3: M-ORA Filter Bank:** To bypass the historical $\mathcal{O}(L^2)$ matrix memory bottlenecks of true fractional integration, the continuous flow is distributed across $K$ parallel, dynamically independent sub-states. Utilizing a logarithmic pole fetch via the Modified Oustaloup Recursive Approximation (M-ORA), the hardware-accelerated conformal mapping transitions the flow while mathematically guaranteeing localized volume contraction.
* **Stage 4: Macroscopic Fractional Superposition:** The final stage maps amplitude-matched Pad'{e} residue weights $w_k$ to linearly superimpose the independent branches. This successfully reconstructs the macroscopic fractional envelope $\mathcal{K}_K(t)$, capturing the global heavy-tailed fractal topology within a secure error limit without violating non-equilibrium thermodynamic bounds. 

![Conformal Fractional Symplectic State-Space Model Architecture](csfssm_arch.pdf)



## 📂 Repository Structure
```text
conformal-fractional-ssm/
├── README.md                 # Project documentation and usage instructions
├── src/                      # Core architectural modules
│   ├── __init__.py
│   ├── config.py             # Hyperparameter configurations (omega bounds, K poles)
│   ├── ema_filter.py         # Phase 1: Exogenous Sequence Embedding 
│   ├── symplectic_core.py    # Phase 2: Symplectic Hamiltonian Generator (Darboux transitions)
│   ├── m_ora.py              # Phase 3: Modified Oustaloup Recursive Approximation Filter Bank
│   └── cfs_ssm.py            # Phase 4: Macroscopic Fractional Superposition & Full Model
(Comming soon)
├── examples/                 # Empirical evaluation scripts
│   ├── solar_pv_forecasting.py # Training script for high-frequency photovoltaic data
│   └── strange_attractor.py    # Autonomous generation of Fractional Lorenz-Lü-Chen attractors
└── tests/                    # Rigorous mathematical bound validations
    ├── test_symplectic_bounds.py # Validation of phase-space volume contraction 
    └── test_fractional_decay.py  # Validation of heavy-tailed power-law memory
