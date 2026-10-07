# safety

The observer lane (Layer 3) of a layered, silicon-anchored AI-safety architecture, and the canonical home of the licensing for all of the author's repositories.

| Repo | Layer | Role |
|---|---|---|
| [Watermark](https://github.com/YobieBenjamin/Watermark) | L2 | provenance: a study of OpenAI's textGrain watermark, hardened detector, retrieval, signed registry, 13-attack harness |
| **safety** (this repo) | L3 | early-warning observers: signed verdicts about a specific request, consumed as witnesses by the control plane |
| [hardware-and-silicon](https://github.com/YobieBenjamin/hardware-and-silicon) | L0/L4/L5 | silicon root of trust, attestation, default-deny gate with one-time tickets, tamper-evident audit trail, NVIDIA OpenShell/Sentry adapter, 66-attack harness |

## Status

The observer interface is fixed and documented in [hardware-and-silicon/docs/LANES.md](https://github.com/YobieBenjamin/hardware-and-silicon/blob/main/docs/LANES.md): an observer issues a signed assertion `{type, observer, subject = request hash, risk, flags, issued_at, expires_at}` under a key the control plane anchors. The control plane ships with a stand-in observer (`obs-main`) so it can be tested without this repo; the observers themselves land here.

Why a watcher is a witness and never the lock, and why the lock is silicon, is argued in [A Multi-Layer Approach to AI Safety](https://github.com/YobieBenjamin/hardware-and-silicon/blob/main/blog/01-a-multi-layer-approach-to-ai-safety.md).

## License

Source-available, not open source. Copyright (c) 2026 Yobie Benjamin. Software is licensed under the PolyForm Noncommercial License 1.0.0 ([LICENSE.md](https://github.com/YobieBenjamin/safety/blob/main/LICENSE.md)); documentation, data and figures under CC BY-NC 4.0 ([LICENSE-DOCS.txt](https://github.com/YobieBenjamin/safety/blob/main/LICENSE-DOCS.txt)). Attribution is required for any use in whole or in part ([NOTICE](https://github.com/YobieBenjamin/safety/blob/main/NOTICE)); commercial use requires a separate license. See [LICENSING.md](https://github.com/YobieBenjamin/safety/blob/main/LICENSING.md) for scope and contact, and [CITATION.cff](https://github.com/YobieBenjamin/safety/blob/main/CITATION.cff) to cite this work.
