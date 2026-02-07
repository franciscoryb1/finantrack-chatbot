import torch.nn.functional as F


def softmax_confidence(logits, temperature: float = 1.0):
    probs = F.softmax(logits / temperature, dim=1)
    conf, pred = probs.max(dim=1)
    return pred.cpu().numpy(), conf.cpu().numpy()
