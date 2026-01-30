# HPL Final Presentation & Report - Roadmap to Excellence
## Deadline: ~3 weeks | Goal: Make something you're proud of

---

# WHAT WILL MAKE YOU STAND OUT

| What Others Did | What You Will Do |
|-----------------|------------------|
| Laptop/WSL | **Real HPC cluster (Grid'5000)** |
| Just ran HPL | **Strong + Weak scaling analysis** |
| Basic results | **Comparison with published TOP500 data** |
| No sources | **Cite research papers** |
| Read slides | **Understand deeply, explain confidently** |
| Basic graphs | **Professional visualizations** |

---

# 3-WEEK TIMELINE

## Week 1: Research & Access (Days 1-7)

### Day 1-2: Get HPC Access
- [ ] Register for **Grid'5000** (free for French academics): https://www.grid5000.fr/w/Grid5000:Get_an_account
- [ ] Alternative: Ask professor about university cluster access
- [ ] Test SSH access, understand job submission (OAR)

### Day 3-4: Read Research Papers
- [ ] Read HPL original paper (Petitet et al.)
- [ ] Read TOP500 methodology
- [ ] Read 2-3 papers on HPL optimization
- [ ] Take notes on key insights

### Day 5-7: Understand Deeply
- [ ] Understand LU factorization mathematically
- [ ] Understand 2D block-cyclic distribution in detail
- [ ] Understand communication patterns (panel broadcast, row swaps)
- [ ] Understand what limits performance (compute vs memory vs network)

---

## Week 2: Experiments (Days 8-14)

### Strong Scaling Experiments
- [ ] Fix N (large, e.g., 100,000)
- [ ] Vary processes: 16, 32, 64, 128, 256
- [ ] Measure time and GFLOPS
- [ ] Calculate speedup and efficiency

### Weak Scaling Experiments
- [ ] Scale N proportionally with processes
- [ ] Keep memory per process constant
- [ ] Measure if time stays constant

### Parameter Tuning
- [ ] Test multiple NB values (64, 128, 192, 256)
- [ ] Test different P×Q configurations
- [ ] Test different broadcast algorithms (BCAST parameter)
- [ ] Find optimal configuration

### Collect Data
- [ ] Record all results systematically
- [ ] Document platform specs (CPU model, network, memory)
- [ ] Save raw HPL outputs

---

## Week 3: Report & Presentation (Days 15-21)

### Days 15-17: Write Report
- [ ] Introduction & objectives
- [ ] Algorithm explanation (with math)
- [ ] Experimental methodology
- [ ] Results & analysis
- [ ] Comparison with literature
- [ ] Conclusions

### Days 18-19: Create Presentation
- [ ] Professional slide design
- [ ] Clear graphs with proper labels
- [ ] Key insights highlighted
- [ ] Practice transitions

### Days 20-21: Practice
- [ ] Full rehearsal with teammate
- [ ] Time management (15 min strict)
- [ ] Anticipate Q&A
- [ ] Final polish

---

# GRID'5000: YOUR SECRET WEAPON

## What is Grid'5000?
- French national HPC testbed
- **FREE** for researchers and students
- Real HPC hardware (thousands of cores)
- Perfect for scaling experiments

## How to Get Access
1. Go to: https://www.grid5000.fr/w/Grid5000:Get_an_account
2. Register with your university email
3. Get supervisor approval (your professor)
4. Access granted within days

## Basic Usage
```bash
# Connect
ssh username@access.grid5000.fr
ssh lyon  # or nancy, rennes, etc.

# Reserve nodes
oarsub -I -l nodes=4,walltime=2:00:00

# Load HPL module
module load hpl

# Run
mpirun -np 64 ./xhpl
```

---

# RESEARCH PAPERS TO READ

## Essential (Must Read)
1. **HPL Original Documentation**
   - https://www.netlib.org/benchmark/hpl/
   - The official algorithm description

2. **"The LINPACK Benchmark: Past, Present, and Future"**
   - Dongarra, J. et al.
   - https://doi.org/10.1002/cpe.3039
   - History and methodology of LINPACK/HPL

3. **TOP500 Methodology**
   - https://www.top500.org/project/linpack/
   - How TOP500 uses HPL

## Recommended (For Depth)
4. **"Performance Optimization of the HPL Benchmark"**
   - Various authors - search on Google Scholar
   - Tuning techniques

5. **"Anatomy of High-Performance Matrix Multiplication"**
   - Goto, K. & van de Geijn, R.
   - Understanding DGEMM (the core of HPL)

## How to Find More
```
Google Scholar searches:
- "HPL benchmark optimization"
- "High Performance Linpack scaling"
- "LU factorization parallel performance"
```

---

# EXPERIMENTS TO RUN

## 1. Strong Scaling (MUST DO)

**Setup:**
- Fixed N = 100,000 (or largest that fits)
- Vary P×Q: 4×4, 4×8, 8×8, 8×16, 16×16...
- Total processes: 16 → 32 → 64 → 128 → 256

**What to Measure:**
```
Speedup = T(16 procs) / T(P procs)
Efficiency = Speedup / (P / 16) × 100%
```

**Expected Result:**
- Speedup increases but not linearly
- Efficiency decreases (Amdahl's law)

## 2. Weak Scaling (MUST DO)

**Setup:**
- Scale N so that N²/P stays constant
- Example: N=50K for 16 procs, N=70K for 32 procs, N=100K for 64 procs

**What to Measure:**
- Time should stay roughly constant
- GFLOPS should scale linearly

## 3. Parameter Tuning

**NB Sweep:**
```
NB = 64, 96, 128, 160, 192, 224, 256
```

**P×Q Configurations:**
```
For 64 processes: 1×64, 2×32, 4×16, 8×8
```

**BCAST Algorithms:**
```
0=1-ring, 1=1-ring-M, 2=2-ring, 3=2-ring-M, 4=Long, 5=Long-M
```

## 4. Comparison with TOP500

- Find a similar machine on TOP500
- Compare your efficiency with theirs
- Explain differences

---

# REPORT STRUCTURE (10-15 pages)

## 1. Introduction (1 page)
- Context: HPC benchmarking
- Why HPL matters (TOP500)
- Objectives of this study

## 2. Background (2-3 pages)
- Mathematical problem: Ax = b
- LU decomposition algorithm
- Parallel implementation (2D block-cyclic)
- Key parameters (N, NB, P, Q)

## 3. Methodology (2 pages)
- Platform description (Grid'5000 specs)
- Software stack (HPL version, MPI, BLAS)
- Experimental design
  - Strong scaling setup
  - Weak scaling setup
  - Tuning methodology

## 4. Results (3-4 pages)
- Strong scaling results + graphs
- Weak scaling results + graphs
- Parameter tuning results
- Best configuration found

## 5. Analysis (2-3 pages)
- Performance analysis
- Efficiency discussion
- Comparison with published results
- Bottleneck identification

## 6. Conclusion (1 page)
- Summary of findings
- Lessons learned
- Future work suggestions

## 7. References
- All papers cited
- HPL documentation
- Grid'5000 documentation

---

# PRESENTATION STRUCTURE (15 min)

## Part 1: Theory (Your Teammate) - 6 min
1. Title + Plan (1 min)
2. What is HPL & why it matters (2 min)
3. Algorithm: LU decomposition (2 min)
4. Parallelization: 2D block-cyclic (1 min)

## Part 2: Experiments & Results (You) - 7 min
5. Methodology & Platform (1 min)
6. Strong Scaling Results (2 min)
7. Weak Scaling Results (1.5 min)
8. Parameter Tuning (1.5 min)
9. Comparison with Literature (1 min)

## Part 3: Conclusion - 2 min
10. Key Findings + Lessons Learned (1 min)
11. Questions (1 min buffer)

---

# VISUAL IMPROVEMENTS

## Graphs to Create

1. **Strong Scaling Graph**
   - X: Number of processes (log scale)
   - Y: Speedup
   - Include ideal linear speedup line

2. **Efficiency Graph**
   - X: Number of processes
   - Y: Efficiency (%)
   - Show how efficiency drops

3. **Weak Scaling Graph**
   - X: Number of processes
   - Y: Time (should be flat) or GFLOPS (should increase)

4. **NB Tuning Heatmap**
   - X: NB values
   - Y: GFLOPS
   - Highlight optimal

5. **Comparison Bar Chart**
   - Your results vs TOP500 reference
   - Or vs published papers

## Design Tips
- Use consistent colors
- Label axes clearly
- Include units
- Add trend lines where appropriate
- Use professional fonts (no Comic Sans!)

---

# WHAT WILL IMPRESS THE PROFESSOR

1. **Real HPC Results** - Not just laptop
2. **Proper Scaling Analysis** - Strong + Weak
3. **Citations** - Show you read papers
4. **Understanding** - Explain WHY, not just WHAT
5. **Comparison** - Context with published results
6. **Professional Visuals** - Clean, clear graphs
7. **Confidence** - Don't read slides, explain

---

# IMMEDIATE NEXT STEPS

## This Week
1. [ ] Apply for Grid'5000 account TODAY
2. [ ] Download and read the Dongarra HPL paper
3. [ ] Plan experiments with your teammate
4. [ ] Divide work: who does what

## Communication with Teammate
Tell them:
> "Pour la présentation finale, je propose qu'on utilise Grid'5000 pour faire du vrai scaling sur un cluster. On fait du strong scaling et weak scaling, on cite des papiers de recherche, et on compare avec le TOP500. Ça va être beaucoup plus impressionnant."

---

# RESOURCES

## Grid'5000
- Main site: https://www.grid5000.fr/
- Getting started: https://www.grid5000.fr/w/Getting_Started
- Hardware: https://www.grid5000.fr/w/Hardware

## HPL
- Official: https://www.netlib.org/benchmark/hpl/
- Tuning guide: https://www.netlib.org/benchmark/hpl/tuning.html

## TOP500
- List: https://www.top500.org/lists/top500/
- Methodology: https://www.top500.org/project/linpack/

## Research Papers
- Google Scholar: https://scholar.google.com/
- Search: "HPL benchmark" OR "High Performance Linpack"

---

*Roadmap created: January 28, 2026*
*Goal: Deliver an impressive final presentation that you're proud of*
