import torch
import torch.nn as nn

class SymplecticHamiltonianGenerator(nn.Module):
    """
    Phase 2: Symplectic Hamiltonian Generator Core.
    Synthesizes the non-autonomous vector field utilizing a Darboux indefinite 
    parameterization to ensure the transition matrices strictly inhabit the symplectic Lie algebra.
    """
    def __init__(self, input_dim: int, n_dim: int):
        super().__init__()
        self.n_dim = n_dim
        self.hidden_dim = 2 * n_dim
        
        # Canonical Symplectic Tensor J
        J_block = torch.tensor([[0.0, 1.0], [-1.0, 0.0]])
        self.register_buffer('J', torch.block_diag(*[J_block for _ in range(n_dim)]))
        
        # Neural parameterization for the Hamiltonian H_theta
        self.param_net = nn.Linear(input_dim, self.hidden_dim * self.hidden_dim)

    def forward(self, x_t: torch.Tensor) -> torch.Tensor:
        batch_size = x_t.size(0)
        # Synthesize Hamiltonian core H_theta
        H_theta = self.param_net(x_t).view(batch_size, self.hidden_dim, self.hidden_dim)
        
        # Parameterize as a symmetric matrix to natively ensure J H_theta remains in sp(2n, R)
        H_theta = torch.bmm(H_theta, H_theta.transpose(1, 2))
        
        # Form the conservative generator J H_theta
        JH_theta = torch.matmul(self.J.unsqueeze(0), H_theta)
        return JH_theta
