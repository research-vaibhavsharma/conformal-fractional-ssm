import torch
import torch.nn as nn

class EMAFilter(nn.Module):
    """
    Phase 1: Exogenous Sequence Embedding.
    Enforces a globally Lipschitz continuous temporal total variation by routing 
    raw sequences through a continuous Exponential Moving Average (EMA) low-pass filter.
    """
    def __init__(self, beta: float = 0.9):
        super().__init__()
        self.beta = beta

    def forward(self, x_raw: torch.Tensor) -> torch.Tensor:
        # x_raw shape: (batch_size, seq_len, input_dim)
        x_filtered = torch.zeros_like(x_raw)
        x_filtered[:, 0, :] = x_raw[:, 0, :]
        for t in range(1, x_raw.size(1)):
            x_filtered[:, t, :] = self.beta * x_filtered[:, t-1, :] + (1 - self.beta) * x_raw[:, t, :]
        return x_filtered
