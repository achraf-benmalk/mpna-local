# Deliverable 2 - Action Plan
## Final Presentation (15 min oral) + Report | Deadline: 18 February 2026

---

## Understanding: What's Asked

From `projet.md`, the **second deliverable** requires:
1. **Final 15-minute oral presentation** — covering final results and conclusions
2. **Detailed written report** — covering every project stage
3. **Source code** of the implemented benchmarks

### What you have (Deliverable 1 = done):
- Intermediate presentation (Jan 28): HPL on your laptop (Ryzen 9 / WSL2), up to 44.2 GFLOPS
- Slides, script, graphs already in `project/presentation_fr/`

### What's new for Deliverable 2:
- **Toubkal HPC results** (from your colleague's work on the Toubkal supercomputer):
  - GPU-accelerated HPL using NVIDIA A100 and H100
  - Singularity containerized execution (hpc-benchmarks_23.10.sif)
  - Results across N=20K to N=100K, 1 GPU and 2 GPUs configurations
  - A100 peak: ~18,000 GFLOPS (1 GPU), ~35,000 GFLOPS (2 GPUs)
  - H100 peak: ~45,200 GFLOPS (1 GPU), ~82,000 GFLOPS (2 GPUs)
  - H100 vs A100 speedup: 2.51× at large N

### The core story for Deliverable 2:
**Laptop (CPU) → Toubkal A100 (GPU) → Toubkal H100 (GPU)** — showing how HPL performance scales from a consumer laptop to a real HPC platform with modern GPUs, analyzing the why behind each performance jump.

---

## Plan — 8 Tasks

### Task 1: Write the final report (main deliverable)

Structure (10-15 pages):

1. **Introduction** (1 page)
   - Context: HPC benchmarking, why HPL matters (TOP500)
   - Project objective: implement, run, and analyze HPL across platforms

2. **Background / Theory** (2-3 pages)
   - Mathematical problem: dense Ax=b
   - LU factorization with partial pivoting (algorithm + complexity (2/3)N³)
   - Parallel implementation: 2D block-cyclic distribution (use the diagram from `HPL Parameters [20].png`)
   - Key parameters: N, NB, P×Q, BCAST, PFACT

3. **Methodology** (2 pages)
   - **Platform 1 — Laptop**: Ryzen 9 4900HS, WSL2, OpenMPI, OpenBLAS, HPL 2.3
   - **Platform 2 — Toubkal HPC**: NVIDIA A100 & H100 GPUs, Singularity container, Lustre FS, GPU-accelerated HPL
   - Experimental design: problem sizes, parameter choices (NB=192/128 on CPU, NB=576 on GPU), process grids
   - Execution methodology (show the 4-step Singularity workflow)

4. **Results** (3-4 pages)
   - Laptop CPU results table (N=10K-30K, NB=128 vs 192)
   - Toubkal A100 results: 1 GPU vs 2 GPUs graph + table
   - Toubkal H100 results: 1 GPU vs 2 GPUs graph + table
   - A100 vs H100 comparison bar chart with speedup ratios
   - Cross-platform comparison: laptop 44 GFLOPS → A100 18,000 → H100 45,200 (1000× jump)

5. **Analysis** (2-3 pages)
   - Performance scaling with N (compute-to-communication ratio)
   - Multi-GPU scaling behavior (communication overhead at small N, near-linear at large N)
   - GPU generation comparison (measured 2.51× vs theoretical 2.6×)
   - NB tuning impact (NB=128 vs 192 on CPU, NB=576 on GPU — why different)
   - Efficiency discussion (laptop ~11% due to WSL2/thermal, GPU closer to theoretical peak)
   - Comparison with TOP500 reference numbers

6. **Conclusion** (1 page)
   - Summary of findings
   - Lessons learned (platform matters, tuning matters, HPL is compute-bound)
   - Perspectives / future work

7. **References**
   - HPL official documentation (netlib.org)
   - Dongarra et al., "The LINPACK Benchmark: Past, Present, and Future"
   - TOP500 methodology
   - NVIDIA HPC-Benchmarks documentation

---

### Task 2: Create the final presentation (15 slides)

**Part 1 — Theory recap (slides 1-5, ~4 min)**
- Slide 1: Title — "HPL Benchmark: Du Laptop au Supercalculateur"
- Slide 2: Agenda
- Slide 3: What is HPL? (Ax=b, TOP500, (2/3)N³)
- Slide 4: Algorithm — LU factorization with partial pivoting
- Slide 5: Parallelization — 2D block-cyclic (use the diagram figure)

**Part 2 — Platforms & methodology (slides 6-7, ~2 min)**
- Slide 6: Platform comparison table (Laptop vs Toubkal A100 vs Toubkal H100)
- Slide 7: Methodology — HPL.dat configs, execution steps, Singularity workflow

**Part 3 — Results (slides 8-12, ~6 min) — THE CORE**
- Slide 8: Laptop results (table + graph, best = 44.2 GFLOPS)
- Slide 9: A100 results (1 vs 2 GPUs graph)
- Slide 10: H100 results (1 vs 2 GPUs graph)
- Slide 11: A100 vs H100 comparison (bar chart with speedup annotations)
- Slide 12: Cross-platform synthesis — laptop (44 GFLOPS) vs A100 (18K) vs H100 (45K) — the "wow" slide

**Part 4 — Analysis & conclusion (slides 13-15, ~3 min)**
- Slide 13: Key observations (scaling with N, multi-GPU overhead, NB tuning)
- Slide 14: Conclusion + lessons learned
- Slide 15: Merci — Questions?

---

### Task 3: Generate professional comparison graphs

New graphs needed (Python/matplotlib):
1. **Cross-platform bar chart**: Laptop vs A100 vs H100 (peak GFLOPS, logarithmic scale)
2. **Multi-GPU scaling efficiency**: (GFLOPS with 2 GPUs) / (2 × GFLOPS with 1 GPU) vs N — for both A100 and H100
3. **NB tuning comparison**: NB=128 vs NB=192 on CPU, and how NB=576 is optimal for GPU
4. Reuse existing graphs from `figures/` directory for A100/H100 individual and comparison results

---

### Task 4: Prepare the oral script

- Write speaking notes for each slide (~1 min per slide)
- Key transitions to rehearse:
  - "On the laptop we reached 44 GFLOPS. Now let's see what happens on a real HPC platform..."
  - "The A100 gives us 18,000 GFLOPS — a 400× improvement over the laptop"
  - "Moving to H100, we see 2.5× over A100, which matches the theoretical peak ratio"
- Anticipate Q&A (reuse + extend from `HPL_PRESENTATION_GUIDE.md`)

---

### Task 5: Document the source code

- Ensure HPL.dat configs for both platforms are in the repo
- Add the Singularity execution scripts
- Document the local compilation/run steps (already partly done)

---

### Task 6: Prepare Q&A material

New questions to prepare for (beyond the intermediate ones):
- "Why is there a multi-GPU penalty at small N?" → Communication overhead exceeds compute benefit
- "Why NB=576 for GPU but NB=128 for CPU?" → GPU parallelism needs larger blocks; CPU needs cache-friendly sizes
- "How does your H100 result compare to TOP500?" → Context with published numbers
- "What is the efficiency on Toubkal?" → Calculate vs theoretical peaks (A100: 19.5 TFLOPS, H100: ~51 TFLOPS)
- "Could you have run on more GPUs? What would happen?" → Expected scaling behavior

---

### Task 7: Commit and organize the repo

Final repo structure:
```
project/
├── rapport/               # Final report (PDF + source)
├── presentation_finale/   # Final presentation (PPTX + graphs)
├── HPL_EXTRACTED_DATA.md  # All Toubkal data (done)
├── HPL_RESULTS.md         # Laptop data (done)
├── code/                  # HPL.dat configs + run scripts
└── ...existing files...
figures/                   # Toubkal graphs (done)
```

---

### Task 8: Final review and push

- Proofread report
- Verify all graphs are properly labeled
- Ensure presentation fits in 15 minutes
- Push everything to the branch

---

## Priority Order

| Priority | Task | Why |
|----------|------|-----|
| 1 | Task 2: Presentation slides | Oral is graded, deadline is close |
| 2 | Task 3: Graphs | Needed for both slides and report |
| 3 | Task 4: Oral script | You need to rehearse |
| 4 | Task 1: Written report | Can be done in parallel |
| 5 | Task 5-6: Code docs + Q&A | Supporting material |
| 6 | Task 7-8: Repo cleanup + push | Final step |
