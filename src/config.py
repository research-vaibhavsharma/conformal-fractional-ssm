from dataclasses import dataclass

@dataclass
class CFSSSMConfig:
    """
    Hyperparameter configurations for the CFS-SSM architecture.
    """
    input_dim: int = 64
    n_dim: int = 32           # The latent state decomposes into q and p coordinates of size n
    alpha: float = 0.8        # Fractional order in (0, 1)
    K: int = 16               # Number of dynamically independent parallel sub-states
    omega_min: float = 1e-4   # Lowest frequency boundary
    omega_max: float = 10.0   # Highest frequency boundary
    delta_t: float = 1.0      # Hardware-aware discretization interval
    ema_beta: float = 0.9     # EMA filter constant for exogenous sequence embedding
