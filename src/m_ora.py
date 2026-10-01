import torch
import torch.nn as nn

class MORAFilterBank(nn.Module):
    """
    Phase 3: Modified Oustaloup Recursive Approximation (M-ORA) Filter Bank.
    Distributes the continuous fractional flow across K parallel, dynamically independent sub-states.
    """
    def __init__(self, alpha: float, K: int, omega_min: float, omega_max: float):
        super().__init__()
        self.K = K
        self.alpha = alpha
        
        # Boundary frequencies structurally defined in relation to the operational spectrum
        omega_b = omega_min * (10 ** (-alpha / 2))
        omega_h = omega_max * (10 ** (alpha / 2))
        
        # Logarithmic pole fetch constraint mapping to s = -\lambda_k
        k_indices = torch.arange(1, K + 1, dtype=torch.float32)
        exponent = (2 * k_indices - 1 + alpha) / (2 * K)
        poles = omega_b * ((omega_h / omega_b) ** exponent)
        self.register_buffer('poles', poles)
        
        # Deterministic macroscopic recombination weights w_k derived directly from partial fraction residues
        # (Simplified baseline representation representing amplitude normalization)
        weights = torch.ones(K) / K
        self.register_buffer('weights', weights)
        
    def get_poles_and_weights(self):
        return self.poles, self.weights
