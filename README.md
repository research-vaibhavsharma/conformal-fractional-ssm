# Conformal Fractional Symplectic State-Space Model
Official implementation of the Conformal Fractional Symplectic State-Space Model (CFS-SSM) for forecasting complex nonlinear dynamics and strange attractors.




## 📂 Repository Structure
```text
conformal-fractional-ssm/
├── README.md                 # Project documentation and usage instructions
├── requirements.txt          # Python dependencies
├── setup.py                  # Installation script for the package
├── src/                      # Core architectural modules
│   ├── __init__.py
│   ├── config.py             # Hyperparameter configurations (omega bounds, K poles)
│   ├── ema_filter.py         # Phase 1: Exogenous Sequence Embedding 
│   ├── symplectic_core.py    # Phase 2: Symplectic Hamiltonian Generator (Darboux transitions)
│   ├── m_ora.py              # Phase 3: Modified Oustaloup Recursive Approximation Filter Bank
│   └── cfs_ssm.py            # Phase 4: Macroscopic Fractional Superposition & Full Model
├── examples/                 # Empirical evaluation scripts
│   ├── solar_pv_forecasting.py # Training script for high-frequency photovoltaic data
│   └── strange_attractor.py    # Autonomous generation of Fractional Lorenz-Lü-Chen attractors
└── tests/                    # Rigorous mathematical bound validations
    ├── test_symplectic_bounds.py # Validation of phase-space volume contraction 
    └── test_fractional_decay.py  # Validation of heavy-tailed power-law memory
