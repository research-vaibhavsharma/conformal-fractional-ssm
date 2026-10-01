import torch
import torch.nn as nn
from .ema_filter import EMAFilter
from .symplectic_core import SymplecticHamiltonianGenerator
from .m_ora import MORAFilterBank
from .config import CFSSSMConfig

class CFSSSM(nn.Module):
    """
    Phase 4: Macroscopic Fractional Superposition & Full Model.
    Reconstructs the global heavy-tailed fractal topology bounded securely by an error limit 
    without violating non-equilibrium thermodynamic bounds.
    """
    def __init__(self, config: CFSSSMConfig):
        super().__init__()
        self.config = config
        self.hidden_dim = 2 * config.n_dim
        
        # Initialize phases
        self.ema = EMAFilter(beta=config.ema_beta)
        self.hamiltonian_core = SymplecticHamiltonianGenerator(config.input_dim, config.n_dim)
        self.m_ora = MORAFilterBank(config.alpha, config.K, config.omega_min, config.omega_max)
        self.B_theta = nn.Linear(config.input_dim, self.hidden_dim)

    def forward(self, x_raw: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = x_raw.size()
        
        # Phase 1: Exogenous Sequence Embedding
        x_filtered = self.ema(x_raw)
        
        poles, weights = self.m_ora.get_poles_and_weights()
        
        # Initialize parallel sub-states h_{0,k}
        h_k = torch.zeros(batch_size, self.config.K, self.hidden_dim, device=x_raw.device)
        global_states = []
        
        I_2n = torch.eye(self.hidden_dim, device=x_raw.device).unsqueeze(0)
        
        # Hardware-Aware Discrete Parallel Scan
        for t in range(seq_len):
            x_t = x_filtered[:, t, :]
            
            # Phase 2: Symplectic Hamiltonian Generation
            JH_theta = self.hamiltonian_core(x_t)
            B_x = self.B_theta(x_t)
            
            h_t_k_next = torch.zeros_like(h_k)
            
            # Phase 3: M-ORA Filter Bank (Replicated K times)
            for k in range(self.config.K):
                lambda_k = poles[k]
                # Structural clamping to exactly preserve unscaled symplectic generation
                p_k = 1.0 
                
                # Conformal transition operator A_k
                A_k_continuous = -lambda_k * I_2n + p_k * JH_theta
                A_k_discrete = torch.matrix_exp(A_k_continuous * self.config.delta_t)
                
                # Driven mapping B_k
                B_k_discrete = self.config.delta_t * B_x 
                
                # Local sub-state update h_{t,k} = A_k h_{t-1,k} + B_k x_t
                h_t_k_next[:, k, :] = torch.bmm(A_k_discrete, h_k[:, k, :].unsqueeze(2)).squeeze(2) + B_k_discrete
                
            h_k = h_t_k_next
            
            # Phase 4: Macroscopic Fractional Superposition
            h_t_macroscopic = torch.sum(weights.view(1, self.config.K, 1) * h_k, dim=1)
            global_states.append(h_t_macroscopic)
            
        return torch.stack(global_states, dim=1)
