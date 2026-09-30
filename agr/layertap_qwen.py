'''Layer telemetry for the second patient (Qwen3-VL-30B-A3B text model: mlx_lm qwen3_moe decoder, 48 layers, 128 experts).
Same five vitals per layer as agr/layertap.py: [0] ||attention update|| [1] ||expert (MoE) update|| [2] ||residual out||
[3] cos(residual in, out) [4] router entropy over experts. Computes exactly the original output (extra reads only).'''
import numpy as np
import mlx.core as mx
from mlx_lm.models import qwen3_moe
_REC = []; _ORIG = qwen3_moe.Qwen3MoeDecoderLayer.__call__; N_LAYERS = 48

def _tapped(self, x, mask=None, cache=None):
    a = self.self_attn(self.input_layernorm(x), mask, cache)
    h = x + a
    hn = self.post_attention_layernorm(h)
    m = self.mlp(hn)
    out = h + m
    f = lambda t: t[:, -1, :].astype(mx.float32)
    xi, xo = f(x), f(out)
    p = mx.softmax(f(self.mlp.gate(hn)), axis=-1); ent = -(p * mx.log(p + 1e-12)).sum(-1)
    cos = (xi * xo).sum(-1) / (mx.linalg.norm(xi, axis=-1) * mx.linalg.norm(xo, axis=-1) + 1e-9)
    _REC.append(mx.concatenate([mx.linalg.norm(f(a), axis=-1), mx.linalg.norm(f(m), axis=-1), mx.linalg.norm(xo, axis=-1), cos, ent]))
    return out

def install(): qwen3_moe.Qwen3MoeDecoderLayer.__call__ = _tapped
def uninstall(): qwen3_moe.Qwen3MoeDecoderLayer.__call__ = _ORIG
def reset(): _REC.clear()
def pop():
    '''Oldest computed step (N_LAYERS, 5); mlx_lm pre-computes one step ahead, so take the oldest N_LAYERS records.'''
    if len(_REC) < N_LAYERS: return None
    step = _REC[:N_LAYERS]; del _REC[:N_LAYERS]; mx.eval(step); return np.array(mx.stack(step)).reshape(N_LAYERS, 5)
