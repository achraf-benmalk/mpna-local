# HPL Presentation Preparation Guide
## 15-Minute Intermediate Presentation - January 28, 2026

---

## 🎯 Objective
Prepare and deliver a 15-minute presentation covering:
1. HPL benchmark algorithm explanation
2. Objectives and purpose of HPL
3. Results obtained on an HPC platform
4. Be ready to answer technical questions

---

# ⚡ 2-DAY INTENSIVE PLAN WITH WORK SPLIT

## Team Split Overview

| Task Area | YOU (with Claude) | COLLEAGUE |
|-----------|-------------------|-----------|
| **Algorithm & Theory** | ✅ Main owner | Support |
| **Slides: Intro + Algorithm** | ✅ Create | Review |
| **HPC Experiments** | Support | ✅ Main owner |
| **Slides: Setup + Results** | Review | ✅ Create |
| **Q&A Preparation** | ✅ Main owner | Support |
| **Presentation Speaking** | ~8 min (theory) | ~7 min (results) |

### Why This Split Works For You:
- **Algorithm part**: Claude can explain every detail, quiz you, help you understand
- **Q&A prep**: Claude can simulate questions and refine your answers
- **Your colleague**: Handles the hands-on HPC work (needs platform access, running jobs)

---

## DAY 1 SCHEDULE

### YOU - Morning (3-4h): Algorithm Mastery
| Time | Task |
|------|------|
| 0:00-0:30 | Read Section 1.1 below (prerequisites) |
| 0:30-1:30 | Read Section 2 (HPL algorithm) - ask Claude questions |
| 1:30-2:30 | Create slides 1-8 (intro + algorithm) |
| 2:30-3:30 | Practice explaining algorithm out loud to Claude |

### COLLEAGUE - Morning (3-4h): HPC Setup
| Time | Task |
|------|------|
| 0:00-1:00 | Access HPC platform, locate/install HPL |
| 1:00-2:00 | Run first test with small N (~10000) |
| 2:00-3:30 | Run scaling experiments (see Section 4) |

### SYNC MEETING - End of Day 1 (30 min)
- Share results (colleague → you)
- Review slides together
- Identify gaps

### YOU - Evening (2h): Slides + Understanding
- Integrate colleague's preliminary results
- Refine algorithm explanations
- Start Q&A preparation with Claude

### COLLEAGUE - Evening (2h): More Experiments
- Run remaining experiments
- Export data, create graphs
- Document platform specs

---

## DAY 2 SCHEDULE

### Morning (3h): Finalize Content
| YOU | COLLEAGUE |
|-----|-----------|
| Finalize algorithm slides | Create results slides (10-12) |
| Q&A deep preparation | Create setup slide (9) |
| Review colleague's slides | Review your slides |

### Afternoon (2-3h): Rehearsal
| Time | Activity |
|------|----------|
| 0:00-0:30 | Full run-through #1 (time it!) |
| 0:30-1:00 | Fix timing issues, adjust content |
| 1:00-1:30 | Full run-through #2 |
| 1:30-2:00 | Q&A practice (quiz each other) |
| 2:00-2:30 | Final polish |

### Presentation (15 min)
- **YOU**: Slides 1-8 (~8 min) - Intro, What is HPL, Algorithm, Parallelization
- **COLLEAGUE**: Slides 9-14 (~7 min) - Setup, Results, Analysis, Conclusion

---

# PHASE 1: Essential Background Knowledge (Day 1)
*Minimal prerequisites - only what's necessary*

## 1.1 What You MUST Understand

### Linear Algebra Basics (30 min)
- **Linear system**: Ax = b where A is a matrix, x and b are vectors
- **LU Decomposition**: Factorizing matrix A = L × U (Lower × Upper triangular matrices)
- Why? Solving Ax = b becomes: Ly = b (forward substitution), then Ux = y (backward substitution)

### HPC Context (20 min)
- **FLOPS**: Floating-point Operations Per Second (measure of computational speed)
- **GFLOPS/TFLOPS/PFLOPS**: Giga/Tera/Peta FLOPS (10^9, 10^12, 10^15)
- **Why benchmarks?**: To compare and rank supercomputers (TOP500 list uses HPL)
- **Distributed memory**: Multiple nodes with separate memory communicating via network (MPI)

---

# PHASE 2: Deep Dive into HPL (Day 1-2)

## 2.1 What is HPL?

### Official Definition
HPL = High Performance Linpack
- Solves a **dense linear system** Ax = b
- Matrix A is random, dense, of size N×N (double precision)
- Measures the **maximum sustained FLOPS** the system can achieve

### Why HPL Matters
1. **TOP500 Ranking**: Used to rank world's fastest supercomputers since 1993
2. **Theoretical vs Practical**: Tests how close a machine gets to its theoretical peak
3. **Industry Standard**: Universal metric for comparing HPC systems

## 2.2 HPL Algorithm (CRITICAL - You must explain this)

### Core Algorithm: LU Factorization with Partial Pivoting

```
Algorithm: PA = LU Decomposition

Input: N×N matrix A
Output: Permutation P, Lower triangular L, Upper triangular U

For k = 1 to N-1:
    1. PIVOTING: Find row with largest |A[i,k]| for i >= k
       - Swap rows if needed (numerical stability)

    2. PANEL FACTORIZATION:
       - Compute column k of L: L[i,k] = A[i,k] / A[k,k]

    3. TRAILING MATRIX UPDATE:
       - Update remaining submatrix: A[i,j] -= L[i,k] * U[k,j]
```

### Parallelization Strategy (2D Block-Cyclic Distribution)

```
┌─────────────────────────────────────┐
│  Matrix A distributed across       │
│  P×Q process grid                  │
│                                     │
│  ┌───┬───┬───┬───┐                 │
│  │P00│P01│P00│P01│  ← Row cycling  │
│  ├───┼───┼───┼───┤                 │
│  │P10│P11│P10│P11│                 │
│  ├───┼───┼───┼───┤                 │
│  │P00│P01│P00│P01│                 │
│  └───┴───┴───┴───┘                 │
│        ↑                           │
│   Column cycling                   │
└─────────────────────────────────────┘
```

**Key Parameters:**
- **N**: Problem size (matrix dimension)
- **NB**: Block size (affects granularity)
- **P × Q**: Process grid (P rows × Q columns of processes)

### Algorithm Phases in Parallel

1. **Panel Factorization** (on one column of processes)
   - Factor NB columns
   - Broadcast panel to all process columns

2. **Row Swap / Pivoting**
   - Exchange rows according to pivot selection
   - Communication-intensive step

3. **Trailing Matrix Update** (DGEMM - most compute-intensive)
   - Update (N-k) × (N-k) submatrix
   - Uses highly optimized BLAS library
   - This is where 90%+ of FLOPS occur

## 2.3 Complexity Analysis

```
Theoretical FLOPS count:
- LU factorization: (2/3)N³ + O(N²) operations
- Solve phase: 2N² operations

Total ≈ (2/3)N³ floating-point operations
```

**Efficiency Metric:**
```
Efficiency = (Achieved GFLOPS / Theoretical Peak GFLOPS) × 100%

Good efficiency: > 70-80%
Excellent efficiency: > 90%
```

---

# PHASE 3: HPL Configuration & Execution (Day 2-3)

## 3.1 HPL.dat Configuration File

```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
29184        Ns  ← PROBLEM SIZE (tune this!)
1            # of NBs
192          NBs ← BLOCK SIZE (typically 64-256)
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
2            Ps  ← PROCESS GRID ROWS
4            Qs  ← PROCESS GRID COLUMNS
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
```

## 3.2 Tuning Guidelines

### Problem Size N
```
Memory available ≈ N² × 8 bytes (double precision)

Example: 128 GB RAM
N_max ≈ sqrt(128 × 10⁹ / 8) ≈ 126,000

Use ~80% of available memory for best performance
```

### Block Size NB
- Too small: Communication overhead dominates
- Too large: Poor load balancing
- Sweet spot: Usually 64-256 (test multiple values)

### Process Grid P × Q
- Total processes = P × Q
- For HPL: P ≤ Q is recommended
- Squarish grids often work best

## 3.3 Running HPL

```bash
# Typical execution
mpirun -np 8 ./xhpl

# With hostfile for multiple nodes
mpirun -np 64 --hostfile hosts.txt ./xhpl

# Output includes:
# - Problem configuration
# - Time to solution
# - GFLOPS achieved
# - Residual check (PASSED/FAILED)
```

## 3.4 QUICK START FOR COLLEAGUE (Copy-Paste Commands)

```bash
# 1. Check if HPL is available (common HPC systems)
module avail hpl
module load hpl  # or similar

# 2. If not available, use pre-built container or compile
# Option A: Spack
spack install hpl
spack load hpl

# Option B: Manual (needs BLAS library)
wget https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
tar xzf hpl-2.3.tar.gz
cd hpl-2.3
# Follow INSTALL instructions

# 3. Create working directory
mkdir ~/hpl_experiments && cd ~/hpl_experiments
cp /path/to/xhpl .
cp /path/to/HPL.dat .  # or create from template above

# 4. Edit HPL.dat for your test
# Change N, NB, P, Q values

# 5. Run (example with SLURM)
srun -N 2 -n 16 ./xhpl > results_N50000_NB192.txt

# 6. Extract key result
grep -E "WR|PASSED|FAILED" results_N50000_NB192.txt
```

### What Colleague Needs to Document
```
Platform: [cluster name]
Nodes used: [X]
Cores per node: [Y]
Memory per node: [Z GB]
MPI: [OpenMPI/MPICH/Intel MPI version]
BLAS: [MKL/OpenBLAS/BLIS version]
```

---

# PHASE 4: Experimentation on HPC Platform (Day 3-4)

## 4.1 Experimental Plan (MINIMAL - 2 days)

### MUST-DO Experiments (for colleague)

| Priority | Experiment | What to vary | Runs needed |
|----------|------------|--------------|-------------|
| **1** | Baseline | N = 10000 | 1 run (verify setup) |
| **2** | Scale N | N = 20K, 50K, 80K | 3 runs |
| **3** | Block size | NB = 128, 192, 256 | 3 runs (pick best N) |

### NICE-TO-HAVE (if time permits)

| Experiment | Variable | Fixed Parameters | Goal |
|------------|----------|------------------|------|
| 4. Process grid | Various P×Q for same total | N, NB fixed | Communication impact |
| 5. Strong scaling | Fixed N, increase P×Q | NB fixed | Speedup limits |

### Metrics to Collect

1. **GFLOPS achieved** (from HPL output)
2. **Execution time** (Wall clock seconds)
3. **Efficiency**: GFLOPS / Peak GFLOPS
4. **Residual norm** (correctness verification)

## 4.2 Results Template

```markdown
| Config | N | NB | P×Q | Nodes | Time(s) | GFLOPS | Efficiency(%) |
|--------|---|----|-----|-------|---------|--------|---------------|
| Run 1  | 50000 | 192 | 2×4 | 2 | 234.5 | 145.2 | 72.3 |
| Run 2  | 50000 | 192 | 4×4 | 4 | 125.3 | 270.1 | 67.5 |
| ...    |   |    |     |   |     |        |       |
```

---

# PHASE 5: Presentation Structure (Day 4-5)

## 5.1 Slide Outline (15 minutes)

### Slide 1: Title (30 sec)
- "HPL Benchmark: High Performance Linpack"
- Your names, date, course

### Slide 2: Agenda (30 sec)
- What is HPL?
- Algorithm overview
- Experimental setup
- Results
- Conclusions

### Slide 3-4: What is HPL? (2 min)
- Purpose: Measure maximum FLOPS
- Use case: TOP500 supercomputer ranking
- Mathematical problem: Solve Ax = b

### Slide 5-6: The Algorithm (3 min)
- LU Decomposition with partial pivoting
- Diagram of the 3 phases
- Why partial pivoting? (numerical stability)

### Slide 7-8: Parallel Implementation (3 min)
- 2D Block-cyclic distribution diagram
- Communication patterns
- Key parameters: N, NB, P×Q

### Slide 9: Experimental Setup (1 min)
- HPC platform used (name, specs)
- Number of nodes, cores, memory
- Software stack (MPI implementation, BLAS library)

### Slide 10-12: Results (3 min)
- Scaling graphs (GFLOPS vs N, vs nodes)
- Efficiency analysis
- Optimal configuration found

### Slide 13: Analysis & Observations (1 min)
- Key findings
- Performance bottlenecks identified
- Comparison with theoretical peak

### Slide 14: Conclusions (30 sec)
- Summary of HPL characteristics
- Lessons learned

### Slide 15: Questions? (remaining time)
- Backup slides with additional data

---

# PHASE 6: Q&A Preparation (Day 5)

## 6.1 Likely Questions & Answers

### Algorithm Questions

**Q: Why use LU decomposition instead of other methods?**
> LU is efficient for dense systems, O(n³) complexity, and parallelizes well. Other methods (Jacobi, Gauss-Seidel) are for sparse systems.

**Q: What is partial pivoting and why is it needed?**
> Selecting the largest element in the column as pivot ensures numerical stability. Without it, small pivots cause division by near-zero, amplifying errors.

**Q: What is the computational complexity?**
> (2/3)N³ FLOPS for LU factorization. Doubling N means 8× more computation.

### Implementation Questions

**Q: What is 2D block-cyclic distribution?**
> Matrix blocks are distributed in a round-robin fashion across a 2D grid of processes. Ensures load balancing - each process gets similar work.

**Q: Why P ≤ Q?**
> Panel factorization is on a column of processes. Smaller P means less communication during this critical path.

**Q: What does NB affect?**
> Block size NB affects granularity: too small = communication overhead, too large = poor load balance and cache usage.

### Performance Questions

**Q: What limits efficiency?**
> 1) Communication overhead (row swaps, panel broadcasts)
> 2) Load imbalance (at matrix edges)
> 3) Memory bandwidth (trailing update phase)

**Q: How does HPL compare to real applications?**
> HPL is compute-bound (lots of DGEMM). Real applications often memory-bound. That's why HPCG was introduced as complementary benchmark.

**Q: What is a good efficiency?**
> 70-80% is good, >90% is excellent. TOP500 machines typically achieve 70-85%.

### Practical Questions

**Q: How did you choose N?**
> Based on available memory: N² × 8 bytes ≤ 80% of RAM. Larger N generally gives better efficiency.

**Q: What BLAS library did you use?**
> [Answer based on your platform: Intel MKL, OpenBLAS, AMD BLIS, etc.]

**Q: How do you verify correctness?**
> HPL computes residual ||Ax - b|| / (||A|| × ||x|| × N × ε). Must be < 16.0 to PASS.

---

# PHASE 7: 2-DAY Action Checklist

## DAY 1 Checklist

### YOU (Algorithm + Theory)
- [ ] Read Phase 1 (30 min) - Essential background
- [ ] Read Phase 2 (1h) - HPL algorithm deep dive
- [ ] Ask Claude to explain anything unclear
- [ ] Create slides 1-4: Title, Agenda, What is HPL
- [ ] Create slides 5-8: Algorithm, Parallelization
- [ ] Practice explaining LU decomposition out loud
- [ ] Practice explaining 2D block-cyclic distribution
- [ ] Evening: Start Q&A prep (Phase 6)

### COLLEAGUE (HPC + Experiments)
- [ ] Access HPC platform
- [ ] Locate or install HPL
- [ ] Run test with N=10000 (verify it works)
- [ ] Run 3-5 scaling experiments (vary N)
- [ ] Run 2-3 block size experiments (vary NB)
- [ ] Document: platform name, nodes, cores, memory
- [ ] Export results to table format
- [ ] Share results with you by end of day

## DAY 2 Checklist

### YOU
- [ ] Integrate colleague's results into understanding
- [ ] Finalize your slides (1-8)
- [ ] Deep Q&A preparation with Claude
- [ ] Review colleague's slides (9-14)

### COLLEAGUE
- [ ] Create slide 9: Experimental setup
- [ ] Create slides 10-12: Results with graphs
- [ ] Create slide 13: Analysis
- [ ] Create slide 14: Conclusions
- [ ] Review your slides (1-8)

### TOGETHER
- [ ] Full rehearsal #1 (time it - must be ≤15 min)
- [ ] Adjust content if over time
- [ ] Full rehearsal #2
- [ ] Q&A practice (quiz each other)
- [ ] PRESENT!

---

# Quick Reference Card

## Key Numbers to Remember
- **Complexity**: (2/3)N³ FLOPS
- **Memory**: N² × 8 bytes
- **Typical NB**: 64-256
- **Good efficiency**: >70%

## Key Terms
- **FLOPS**: Floating-point Operations Per Second
- **BLAS**: Basic Linear Algebra Subprograms
- **DGEMM**: Double-precision General Matrix Multiply
- **MPI**: Message Passing Interface

## HPL Output Example
```
================================================================================
T/V    N    NB   P   Q         Time       Gflops
--------------------------------------------------------------------------------
WR11C2R4   50000  192   2   4         234.56   3.5432e+02
--------------------------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   0.0012345 ...... PASSED
================================================================================
```

---

# Resources

## Essential Reading
1. HPL Official Site: https://www.netlib.org/benchmark/hpl/
2. HPL Tuning: https://www.netlib.org/benchmark/hpl/tuning.html
3. TOP500 Methodology: https://www.top500.org/project/linpack/

## Videos (if needed)
- Search: "LU decomposition explained"
- Search: "HPL benchmark tutorial"

---

*Document created for MPNA Project - HPL Presentation Preparation*
*Last updated: January 26, 2026*
