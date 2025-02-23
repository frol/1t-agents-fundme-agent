This contract guards against double-spending by keeping track of the already funded profiles.

Build and deploy instructions:

```
pip install near-py-tool=0.1.21
near-py-tool build non-reproducible-wasm
near contract deploy use-file build/contract.wasm
```
