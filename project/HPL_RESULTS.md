# HPL Benchmark Results
## Platform: ASUS Zephyrus G14 (2020) via WSL2

### Configuration
- **CPU**: AMD Ryzen 9 4900HS (8 cores / 16 threads)
- **RAM**: 32 GB
- **OS**: Ubuntu (WSL2)
- **MPI**: OpenMPI
- **BLAS**: OpenBLAS
- **HPL Version**: 2.3

### Fixed Parameters
- **NB**: 192 (block size)
- **P × Q**: 2 × 4 (process grid)
- **Processes**: 8

---

## Results Table

| N | Time (s) | GFLOPS | Efficiency* | Status |
|-------|---------|--------|-------------|--------|
| 10000 | 42.5 | 15.7 | ~4% | PASSED |
| 20000 | 130.0 | 41.0 | ~10% | PASSED |
| 30000 | 471.2 | 38.2 | ~10% | PASSED |

*Efficiency estimated against theoretical peak of ~400 GFLOPS (rough estimate for Ryzen 9 4900HS)

---

## Raw Output Excerpts

### N = 10000
```
WR11C2R4       10000   192     2     4              42.47             1.5699e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   2.37915829e-03 ...... PASSED
```

### N = 20000
```
WR11C2R4       20000   192     2     4             130.04             4.1016e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.60720421e-03 ...... PASSED
```

### N = 30000
```
WR11C2R4       30000   192     2     4             471.19             3.8204e+01
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   1.74252722e-03 ...... PASSED
```

---

## Observations

1. **GFLOPS increased from N=10K to N=20K**: Expected behavior - larger problem size means better compute-to-communication ratio
2. **GFLOPS decreased slightly at N=30K**: Likely due to:
   - Thermal throttling on laptop
   - WSL2 overhead
   - Memory bandwidth limitations
   - Longer runtime = more thermal issues

---

*Results collected: January 27, 2026*
