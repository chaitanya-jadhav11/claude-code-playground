---
description: Profiles, finds bottlenecks, and optimizes raw Python code performance.
argument-hint:  
allowed-tools: [Read, Write, Grep, Glob]
---
Analyze and profile the performance of the following target Python file: $ARGUMENTS

Step 1 — Mental Profiling: Analyze the code for loop inefficiencies, memory allocation issues, or slow I/O bindings.
Step 2 — Optimization Action: Rewrite the code using optimized vectorization (e.g., NumPy), built-in generators, or efficient local data structures.
Step 3 — Output: Return the fully updated file with a markdown diagnostics summary highlighting the speed gains.
