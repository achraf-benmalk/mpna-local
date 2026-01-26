# HPL Project - Colleague Handoff Document
## Presentation: January 28, 2026 (15 minutes)

---

## What's Been Done (Day 1)

### Theory & Understanding
- Learned HPL algorithm (LU decomposition with partial pivoting)
- Understood parallelization (2D block-cyclic distribution)
- Learned key parameters: N (problem size), NB (block size), P×Q (process grid)

### HPL Setup & First Results
- Built HPL on WSL (Ubuntu) with OpenBLAS
- Ran baseline experiments

**Results so far:**
| Run | N | NB | P×Q | Time(s) | GFLOPS | Status |
|-----|---|----|-----|---------|--------|--------|
| 1 | 10000 | 192 | 2×4 | 42.5 | 15.7 | PASSED |
| 2 | 20000 | 192 | 2×4 | 130.0 | 41.0 | PASSED |

---

## Work Split for Presentation

### Achraf (Slides 1-8, ~8 min speaking)
- Slide 1: Title
- Slide 2: Agenda
- Slides 3-4: What is HPL? (purpose, TOP500)
- Slides 5-6: Algorithm (LU decomposition)
- Slides 7-8: Parallelization (2D block-cyclic)

### You (Slides 9-14, ~7 min speaking)
- Slide 9: Experimental setup (platform specs)
- Slides 10-12: Results (graphs, tables)
- Slide 13: Analysis (efficiency, observations)
- Slide 14: Conclusions

---

## What You Need To Do

### Option A: Run More Experiments (if you have time/machine)

**Remaining experiments needed:**

| Priority | N | NB | Why |
|----------|---|----|-----|
| 1 | 30000 | 192 | Scaling test |
| 2 | 40000 | 192 | Larger = better efficiency |
| 3 | 30000 | 128 | Block size comparison |
| 4 | 30000 | 256 | Block size comparison |

**Commands (if you set up HPL yourself):**
```bash
# Change N in HPL.dat
sed -i 's/^[0-9]*        Ns/30000        Ns/' HPL.dat
mpirun -np 8 ./xhpl | tee result_N30000.txt
grep "WR" result_N30000.txt
```

### Option B: Just Make the Slides (if I run experiments)

I can finish experiments tonight/tomorrow and send you:
- Final results table
- Raw data for graphs

You focus on:
1. Creating slides 9-14
2. Making graphs (GFLOPS vs N, etc.)
3. Documenting platform specs

---

## Platform Specs to Document (for Slide 9)

Fill this in for our setup:
```
Platform: ASUS Zephyrus G14 (2020) via WSL2
CPU: AMD Ryzen 9 4900HS (8 cores, 16 threads)
RAM: 32 GB
OS: Ubuntu on WSL2
MPI: OpenMPI (apt package)
BLAS: OpenBLAS (apt package)
```

---

## Key Concepts You Should Know (for Q&A)

### What is HPL?
- Solves Ax = b (dense linear system)
- Measures GFLOPS (billions of floating-point operations per second)
- Used to rank TOP500 supercomputers

### How does it work?
1. **LU Decomposition**: Split matrix A into L (lower triangular) × U (upper triangular)
2. **Partial Pivoting**: Swap rows to use largest values (numerical stability)
3. **Parallel**: Matrix distributed across processes in 2D block-cyclic pattern

### Key Parameters
- **N**: Matrix size (bigger = better efficiency, more RAM needed)
- **NB**: Block size (sweet spot 128-256)
- **P×Q**: Process grid (P ≤ Q recommended)

### Performance Formula
```
Efficiency = Achieved GFLOPS / Theoretical Peak GFLOPS × 100%

Memory needed = N² × 8 bytes
FLOPS count = (2/3) × N³
```

---

## Presentation Flow

```
[0:00-0:30]  Slide 1-2: Title + Agenda (Achraf)
[0:30-2:30]  Slide 3-4: What is HPL (Achraf)
[2:30-5:30]  Slide 5-6: Algorithm - LU decomposition (Achraf)
[5:30-8:00]  Slide 7-8: Parallelization (Achraf)
[8:00-9:00]  Slide 9: Experimental setup (You)
[9:00-12:00] Slide 10-12: Results + graphs (You)
[12:00-14:00] Slide 13: Analysis (You)
[14:00-15:00] Slide 14: Conclusions (You)
[15:00+]     Q&A (Both)
```

---

## Files in the Repo

- `project/HPL_PRESENTATION_GUIDE.md` - Full detailed guide
- `project/COLLEAGUE_HANDOFF.md` - This document
- `project/projet.md` - Original project requirements

---

## Questions?

Let me know:
1. Do you want to run experiments or should I finish them?
2. What tool for slides? (PowerPoint, Google Slides, Beamer?)
3. When can we sync tomorrow to rehearse?

---

*Generated: January 26, 2026*
