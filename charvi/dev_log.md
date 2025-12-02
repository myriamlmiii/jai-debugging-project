# Development Log – Jai Debug Feature (Charvi)

## 2025-12-02 – Fresh setup
- Created new folder `jai_debug_charvi`.
- Added files: registry.py, inspector.py, codegen.py, run_tests.py, run_benchmarks.py, dev_log.md.
- Goal: mimic Jai-style debugging features:
  - Type registry for runtime type info.
  - DFS object inspector to inspect Python objects.
  - Template-based code generator with memoization.

## 2025-12-02 – Core implementation
- Implemented FastRegistry (dict-based, average O(1) lookup).
- Implemented SlowRegistry (list-based, O(n) lookup for comparison).
- Implemented DFS-based inspector with circular reference detection and max depth.
- Implemented template expansion (O(n)) and memoized generate_code (first call O(n), later calls O(1) cache lookup).
## 2025-12-02 – Benchmark Results

### Registry Lookup Times
Format: n, FastRegistry time (s), SlowRegistry time (s)

```
100, 0.00000021, 0.00000112
1000, 0.00000038, 0.00001017
5000, 0.00000079, 0.00004271
```

```
 Memoized vs Non-memoized Code Generation
Non-memoized: 0.29785 s
Memoized: 0.00509 s
```