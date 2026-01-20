# MPNA Course: Fast-Track Execution Plan

---

## SECTION 1 — Repository Analysis

### Structure Overview
```
mpna-local/
├── 01-matrix-matrix/      # Exercise 1 (C, skeleton provided)
├── 02-iterative-relaxation/  # Exercise 2 (C++, COMPLETE code given)
├── 03-sparse-matvec/      # Exercise 3 (MPI required, no code)
├── 04-nonlinear/          # Exercise 4 (hypre lib required, no code)
├── cg/                    # Conjugate Gradient notebook (reference)
├── project/               # Project specs (HPC benchmarks)
├── slides/                # 9 PDFs (unordered)
└── CMakeLists.txt         # Build config
```

### Key Files Identified

| Category | Files | Status |
|----------|-------|--------|
| **Exercises** | 4 directories | Ex1: skeleton, Ex2: complete, Ex3-4: specs only |
| **Project** | `project/projet.md` | Full specs (French) |
| **Slides** | 9 PDFs | Unordered, mixed relevance |
| **Code Given** | `CSRMatrix.h`, `Jacobi.h`, `GaussSeidel.h` | Working implementations |
| **Test Data** | `bcsstk03.mtx`, `cfd1.mtx` | For Exercise 3 |

---

## SECTION 2 — Course Reconstruction

### Logical Module Order

| # | Module | Files/Folders | Purpose |
|---|--------|--------------|---------|
| 1 | **Intro to Numerical Methods** | `slides/intro.pdf` | Course overview |
| 2 | **Dense Matrix Operations** | `01-matrix-matrix/`, `slides/MNPGT.pdf` | Basic matrix multiplication, cache effects |
| 3 | **Sparse Matrix Formats** | `slides/sparse.pdf`, `02-iterative-relaxation/CSRMatrix.h` | CSR format foundation |
| 4 | **Iterative Linear Solvers** | `slides/iterative-methods.pdf`, `02-iterative-relaxation/` | Jacobi, Gauss-Seidel methods |
| 5 | **Conjugate Gradient** | `cg/CG2D.ipynb` | CG method (critical for project) |
| 6 | **Distributed Computing** | `03-sparse-matvec/`, `slides/IS309-prcd.pdf` | MPI, distributed SpMV |
| 7 | **Nonlinear Solvers** | `04-nonlinear/`, `slides/lecture10.pdf`, `slides/lecture11.pdf` | Newton-Raphson, implicit schemes |
| 8 | **Advanced: Multigrid** | `slides/MueLu_tutorial.pdf` | AMG preconditioners (for Ex4) |
| 9 | **Spectral Methods** | `slides/spielman.pdf` | SKIP - theoretical, not needed |

---

## SECTION 3 — Essential Knowledge Filter

### MUST KNOW (for exercises + project)

| Concept | Why | Where to Learn |
|---------|-----|----------------|
| **Matrix memory layout** (row-major) | Ex1, understanding cache | `01-matrix-matrix/main.c` comments |
| **CSR sparse format** | Ex2, Ex3, Ex4, Project | `CSRMatrix.h` - READ THIS CODE |
| **Jacobi iteration** | Ex2 concept | `Jacobi.h` - STUDY THIS |
| **Gauss-Seidel** | Ex2 comparison | `GaussSeidel.h` |
| **SpMV (Sparse Matrix-Vector)** | Ex3, Project | `03-sparse-matvec/README.md` |
| **MPI basics** | Ex3 | `slides/IS309-prcd.pdf` (skim) |
| **Tridiagonal systems** | Ex4 | `04-nonlinear/README.md` |
| **Newton-Raphson** | Ex4 | `04-nonlinear/README.md` (formulas given) |
| **Conjugate Gradient** | Project (HPCG) | `cg/CG2D.ipynb` |
| **Power iteration** | Ex3 eigenvalues | `03-sparse-matvec/README.md` |

### CAN SKIP (for now)

- `spielman.pdf` - Advanced spectral graph theory
- `MueLu_tutorial.pdf` - Only if doing Ex4 fully, optional multigrid
- Deep theory in `iterative-methods.pdf` - Just understand Jacobi/GS converge, GS faster
- Detailed derivations in `04-nonlinear/README.md` - Use given formulas directly

---

## SECTION 4 — Exercises Execution Plan

### Exercise 1: Matrix-Matrix Multiplication
```
Priority: HIGH (warmup, builds confidence)
Time: 2-3 hours
Required concepts: Triple nested loop, cache awareness
```

**Tasks:**
1. Write basic `matrix_matrix_multiplication` (15 min)
2. Add transposed B variant (15 min)
3. Benchmark with n=100,500,1000,2000 (30 min)
4. Compare with BLAS `dgemm` (30 min)

**When:** DO FIRST - before project

---

### Exercise 2: Iterative Relaxation
```
Priority: MEDIUM (code already given)
Time: 1 hour
Required concepts: Read existing code, understand convergence
```

**Tasks:**
1. Read and understand `Jacobi.h` (20 min)
2. Read `GaussSeidel.h` (10 min)
3. Run benchmarks, observe iteration counts (15 min)
4. Write brief comparison (15 min)

**When:** PARALLEL with Ex1 or right after

---

### Exercise 3: Sparse Distributed SpMV
```
Priority: HIGH (critical for project understanding)
Time: 4-6 hours
Required concepts: CSR format, MPI, power iteration
```

**Tasks:**
1. Implement serial CSR SpMV (1 hour)
2. Read Matrix Market files (30 min)
3. Implement MPI distribution (2-3 hours)
4. Power iteration for eigenvalues (1 hour)

**When:** After Ex1, BEFORE heavy project work

---

### Exercise 4: Nonlinear Diffusion
```
Priority: LOW (complex, hypre dependency)
Time: 6-8 hours if done
Required concepts: Newton-Raphson, tridiagonal solvers, hypre API
```

**Tasks (if time permits):**
1. Setup hypre library
2. Implement linearized implicit scheme
3. Implement Newton method
4. Test with given parameters

**When:** SKIP unless project is done early

---

## SECTION 5 — Optimized Fast-Track Roadmap

### Block 1: Foundation (Day 1)
```
Morning:
- [ ] Read CSRMatrix.h completely (30 min)
- [ ] Read Jacobi.h completely (20 min)
- [ ] Skim intro.pdf + sparse.pdf (30 min)

Afternoon:
- [ ] Complete Exercise 1 fully (2-3 hours)
- [ ] Build and run Exercise 2 code (30 min)
```

### Block 2: Core Skills (Day 2)
```
Morning:
- [ ] Start Exercise 3: Serial CSR SpMV (2 hours)
- [ ] Read project specs thoroughly (30 min)

Afternoon:
- [ ] Choose project benchmark (decision point)
- [ ] Download/install chosen benchmark
- [ ] Run first benchmark execution
```

### Block 3: Project Launch (Day 3)
```
Morning:
- [ ] Continue Exercise 3: MPI part (2-3 hours)

Afternoon:
- [ ] PROJECT: Document benchmark algorithm
- [ ] PROJECT: Run initial experiments
- [ ] PROJECT: Start implementation skeleton
```

### Block 4: Project Deep Dive (Days 4-7)
```
- [ ] Exercise 3: Power iteration (1 hour)
- [ ] PROJECT: Core implementation
- [ ] PROJECT: Performance measurements
- [ ] PROJECT: Prepare intermediate presentation (Jan 28)
```

### Block 5: Finalization (Days 8+)
```
- [ ] PROJECT: Optimization pass
- [ ] PROJECT: Final presentation prep (Feb 18)
- [ ] PROJECT: Report writing
- [ ] Exercise 4: ONLY if time remains
```

---

## SECTION 6 — Project Acceleration Strategy

### Project Overview
Choose ONE HPC benchmark to analyze and implement:
- **HPL** - Dense linear algebra (if Ex1 went well)
- **HPCG** - Sparse CG solver (best fit with course material)
- **GRAPH500** - Graph algorithms (different skill set)
- **TeaLeaf** - Heat diffusion mini-app (relates to Ex4)

### RECOMMENDED: HPCG
**Why:** Directly uses CG method from course, sparse matrices, MPI - all covered in exercises.

### BEFORE starting project, MUST understand:
- CSR sparse format (from Ex2/Ex3)
- Basic MPI communication (from Ex3)
- Conjugate Gradient algorithm (from `cg/CG2D.ipynb`)
- How to measure FLOPS/time

### CAN learn WHILE doing project:
- HPCG-specific optimizations
- Advanced MPI patterns
- Report writing format
- Platform-specific tuning

### First Actions TODAY:

1. **Read project specs** (15 min)
   ```
   cat project/projet.md
   ```

2. **Download HPCG reference** (30 min)
   ```bash
   git clone https://github.com/hpcg-benchmark/hpcg.git
   cd hpcg && mkdir build && cd build
   # Follow install instructions
   ```

3. **Run reference implementation** (1 hour)
   - Get baseline numbers
   - Understand input/output format

4. **Study CG notebook** (30 min)
   ```
   jupyter notebook cg/CG2D.ipynb
   ```

### Project Deliverables Order:

| Order | Deliverable | Deadline | Strategy |
|-------|-------------|----------|----------|
| 1 | Choose benchmark | NOW | Pick HPCG |
| 2 | Understand algorithm | Day 2 | Use CG notebook + docs |
| 3 | Run reference impl | Day 3 | Get baseline metrics |
| 4 | **Intermediate presentation** | Jan 28 | Algorithm + initial results |
| 5 | Own implementation | Week 2-3 | Start simple, optimize later |
| 6 | Performance comparison | Week 3 | vs reference |
| 7 | **Final presentation** | Feb 18 | Full results |
| 8 | Report + code | Feb 18 | Document as you go |

---

## SECTION 7 — Risk Control

### Common Traps

| Trap | Why It Wastes Time | Solution |
|------|-------------------|----------|
| Perfecting Ex1 BLAS comparison | Diminishing returns | Stop at 80% of BLAS speed |
| Reading all theory in slides | Not needed for exercises | Read code first, theory if stuck |
| Trying to understand multigrid | Ex4 optional, complex | Skip MueLu_tutorial.pdf |
| Over-engineering MPI in Ex3 | Basic works fine | Use simple block distribution |
| Making Ex4 work perfectly | Low ROI, hypre issues | Skip or minimal effort |
| Delaying project start | Fatal for deadlines | Start project by Day 3 max |
| Writing report last | Rushed quality | Document while implementing |

### Stop-and-Move-On Points

| Task | Stop When |
|------|-----------|
| Ex1: Matrix multiply | Your code runs, benchmarks show O(n^3), BLAS is faster |
| Ex1: Optimizations | Transposed version is ~2x faster than naive |
| Ex2: Understanding | You can explain why GS converges in fewer iterations |
| Ex3: Serial SpMV | Correct output on test matrices |
| Ex3: MPI | Speedup > 1 with 2-4 processes |
| Ex4 | SKIP entirely unless ahead of schedule |
| Project: Impl | Runs and produces valid results |
| Project: Optimization | Within 50% of reference performance |

### Time Wasters - DO NOT:
- Read `spielman.pdf` (7MB of spectral theory)
- Try to match BLAS performance exactly
- Implement fancy preconditioners for Ex4
- Optimize MPI before correctness
- Write documentation before code works

---

## Quick Reference Card

### Build Commands
```bash
# Exercise 1 & 2
cmake -B build -DCMAKE_BUILD_TYPE=Release .
cmake --build build

# Run Ex1
./build/01-matrix-matrix/matrix_matrix 1000

# Run Ex2
./build/02-iterative-relaxation/iter_laplacian
```

### Key Files to Study (in order)
1. `02-iterative-relaxation/CSRMatrix.h` - Sparse matrix format
2. `02-iterative-relaxation/Jacobi.h` - Iterative solver pattern
3. `01-matrix-matrix/main.c` - Fill in the blank
4. `03-sparse-matvec/README.md` - MPI exercise spec
5. `cg/CG2D.ipynb` - CG algorithm for project
6. `project/projet.md` - Project requirements

### Critical Deadlines
- **Jan 28, 2026**: Intermediate presentation (15 min)
- **Feb 18, 2026**: Final presentation + report + code

---

*Generated for rapid course catch-up. Focus on execution, not perfection.*
