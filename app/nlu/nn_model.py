import torch
from torch import nn
from transformers import AutoModel


class NLUMultiHeadModel(nn.Module):
    """
    Modelo NLU multi-head:
    - Encoder Transformer
    - Head de intent
    - Head de period_type
    - Head de category_hint
    """

    def __init__(
        self,
        model_name: str,
        num_intents: int,
        num_periods: int,
        num_categories: int,
        dropout: float = 0.2,
    ):
        super().__init__()

        # Encoder base
        self.encoder = AutoModel.from_pretrained(model_name)

        hidden_size = self.encoder.config.hidden_size

        self.dropout = nn.Dropout(dropout)

        # Heads
        self.intent_head = nn.Linear(hidden_size, num_intents)
        self.period_head = nn.Linear(hidden_size, num_periods)
        self.category_head = nn.Linear(hidden_size, num_categories)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )

        # Usamos el token [CLS]
        pooled = outputs.last_hidden_state[:, 0]
        pooled = self.dropout(pooled)

        return {
            "intent_logits": self.intent_head(pooled),
            "period_logits": self.period_head(pooled),
            "category_logits": self.category_head(pooled),
        }
