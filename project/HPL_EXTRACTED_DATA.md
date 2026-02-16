# HPL Benchmark - Extracted Results & Technical Details

## 1. HPC Platform Setup (from figures)

### Infrastructure
- **Container**: NVIDIA HPC-Benchmarks 23.10 (Singularity image `hpc-benchmarks_23.10.sif`)
- **GPUs tested**: NVIDIA A100, NVIDIA H100
- **Filesystem**: Lustre (`/home/karim.bezine-ext/lustre/...`)
- **HPL binary path inside container**: `/workspace/hpl-linux-x86_64/`

### HPL.dat Configuration
```
N  (problem sizes):  20000  40000  60000  80000  100000
NB (block size):     576
PMAP:                1 (Column-major)
P × Q:              2 × 1
Threshold:           0.1
PFACT:               1 (Crout)
NBMIN:               64
NDIV:                2
RFACT:               0 (Left)
BCAST:               6 (MPI)
LOOKAHEAD:           3
Memory alignment:    8 doubles
Seed:                100
```

### Execution Steps (reproduced from screenshots)

**Step 1** - Create working directory and HPL.dat:
```bash
$ cd /path/to/working/directory
$ mkdir data
$ cd data/
$ touch HPL.dat
$ vim HPL.dat
```

**Step 2** - Verify HPL.dat via Singularity:
```bash
$ singularity exec --bind $(pwd):/mnt ./hpc-benchmarks_23.10.sif cat /mnt/HPL.dat
```

**Step 3** - Set Singularity bind path for data access:
```bash
$ echo export SINGULARITY_BINDPATH=/home/karim.bezine-ext/lustre/sw_stack-373lcd9r8io/users/karim.bezine-ext/src/data:/mnt >> ~/.bashrc
$ source ~/.bashrc
```

**Step 4** - Run GPU-accelerated HPL:
```bash
$ singularity run --nv hpc-benchmarks_23.10.sif
$ cd /workspace/hpl-linux-x86_64/
$ mpirun -np 1 hpl.sh --dat /mnt/HPL.dat --gpu-affinity 2 --no-multinode --cuda-compat
```

Key flags:
- `--nv`: Enable NVIDIA GPU passthrough in Singularity
- `--gpu-affinity 2`: Bind to specific GPU
- `--no-multinode`: Single-node execution
- `--cuda-compat`: CUDA compatibility mode

---

## 2. HPC Results: A100 GPU

### 1 A100 GPU

| N       | GFLOPS (approx.) |
|---------|-------------------|
| 20,000  | ~9,800            |
| 40,000  | ~16,000           |
| 60,000  | ~17,200           |
| 80,000  | ~17,800           |
| 100,000 | ~18,000           |

### 2 A100 GPUs

| N       | GFLOPS (approx.) |
|---------|-------------------|
| 20,000  | ~9,200            |
| 40,000  | ~25,300           |
| 60,000  | ~31,400           |
| 80,000  | ~33,400           |
| 100,000 | ~34,800           |

### Observations (A100)
- **1 GPU**: Performance plateaus around ~18,000 GFLOPS beyond N=60K
- **2 GPUs**: Scales well up to ~35,000 GFLOPS, roughly 1.9× speedup at large N
- **Small N penalty**: At N=20K, 2 GPUs are actually *slower* than 1 GPU (~9,200 vs ~9,800) due to inter-GPU communication overhead exceeding the compute benefit
- **Scaling ratio (2 GPU / 1 GPU)**: Improves with N — from 0.94× at N=20K to 1.93× at N=100K

---

## 3. HPC Results: H100 GPU

### 1 H100 GPU

| N       | GFLOPS (approx.) |
|---------|-------------------|
| 20,000  | ~16,200           |
| 30,000  | ~25,000           |
| 40,000  | ~35,500           |
| 60,000  | ~42,000           |
| 80,000  | ~44,500           |
| 100,000 | ~45,200           |

### 2 H100 GPUs

| N       | GFLOPS (approx.) |
|---------|-------------------|
| 20,000  | ~11,500           |
| 30,000  | ~25,000           |
| 40,000  | ~42,000           |
| 60,000  | ~65,000           |
| 80,000  | ~77,000           |
| 100,000 | ~82,000           |

### Observations (H100)
- **1 GPU**: Plateaus around ~45,000 GFLOPS (2.5× the A100 single-GPU peak)
- **2 GPUs**: Reaches ~82,000 GFLOPS — excellent multi-GPU scaling at large N
- **Same small-N penalty**: At N=20K, 2 GPUs slower than 1 (11,500 vs 16,200)
- **Crossover**: 2 GPUs surpass 1 GPU somewhere between N=20K and N=30K
- **Scaling ratio (2 GPU / 1 GPU)**: From 0.71× at N=20K to 1.81× at N=100K

---

## 4. A100 vs H100 Comparison (1 GPU each)

| N       | A100 GFLOPS | H100 GFLOPS | Speedup (H100/A100) |
|---------|-------------|-------------|----------------------|
| 20,000  | ~9,800      | ~16,200     | **1.60×**            |
| 40,000  | ~16,000     | ~35,500     | **2.22×**            |
| 60,000  | ~17,200     | ~42,000     | **2.43×**            |
| 80,000  | ~17,800     | ~44,500     | **2.51×**            |
| 100,000 | ~18,000     | ~45,200     | **2.51×**            |

### Key Insight
- H100 advantage grows with problem size: from 1.6× at N=20K to **2.5× at N≥80K**
- At large N, H100 delivers 2.5× the FP64 performance of A100 — consistent with the theoretical peak improvement (FP64: A100 ~19.5 TFLOPS vs H100 ~51 TFLOPS → 2.6× theoretical)
- The measured 2.51× is very close to the theoretical 2.6×, indicating HPL efficiently utilizes the hardware

---

## 5. Local Laptop Results (from previous session)

### Platform
- **Machine**: ASUS Zephyrus G14 (2020)
- **CPU**: AMD Ryzen 9 4900HS (8 cores / 16 threads)
- **RAM**: 32 GB
- **OS**: Ubuntu via WSL2
- **MPI**: OpenMPI
- **BLAS**: OpenBLAS
- **HPL**: version 2.3

### Results (CPU-only, 8 MPI processes, P=2 × Q=4)

| N      | NB  | Time (s) | GFLOPS | Status |
|--------|-----|----------|--------|--------|
| 10,000 | 192 | 42.5     | 15.7   | PASSED |
| 20,000 | 192 | 130.0    | 41.0   | PASSED |
| 30,000 | 192 | 471.2    | 38.2   | PASSED |
| 30,000 | 128 | 407.5    | 44.2   | PASSED |

### Colleague's Results (4 MPI processes, P=2 × Q=2, NB=128)

| N      | GFLOPS |
|--------|--------|
| 10,000 | 14.7   |
| 20,000 | 30.9   |

---

## 6. Key Technical Takeaways for the Project

### Algorithm
- HPL solves a dense linear system Ax=b using **LU factorization with partial pivoting**
- Computation: (2/3)N³ floating-point operations
- Matrix is distributed across processes using **2D block-cyclic distribution** (see `HPL Parameters [20].png` for the diagram showing processes 0-5 assigned cyclically across blocks)

### Performance Scaling Behavior
1. **GFLOPS increases with N** — larger problems have better compute-to-communication ratio (O(N³) compute vs O(N²) communication)
2. **Multi-GPU penalty at small N** — communication overhead between GPUs exceeds the compute benefit when N is too small
3. **Saturation at large N** — single GPU hits memory bandwidth/compute ceiling; adding GPUs extends the ceiling
4. **NB tuning matters** — on the laptop, NB=128 gave +15.6% over NB=192 at N=30K (better cache utilization)

### GPU Generation Comparison
- H100 is **2.5× faster** than A100 for HPL at large problem sizes
- This closely matches the FP64 theoretical peak ratio (~2.6×)
- HPL is compute-bound at large N, so it efficiently exploits raw FLOPS improvements

### Practical Insights
- NB=576 was used on GPU (much larger than the typical CPU value of 128-256) — GPUs benefit from larger blocks due to their massive parallelism
- Column-major PMAP was chosen (PMAP=1), suited for the GPU execution model
- BCAST=6 (MPI broadcast) was used — appropriate for single-node multi-GPU
- The `--gpu-affinity` and `--cuda-compat` flags indicate GPU-direct memory access for performance

---

## 7. Figures Inventory

| Figure | Content |
|--------|---------|
| `HPL.dat [21].png` | Full HPL.dat configuration file (27 lines) |
| `HPL Parameters [20].png` | 2D block-cyclic distribution diagram (P rows, Q cols, NB blocks, processes 0-5) |
| `HPL Step 1 Execution.png` | Directory setup commands |
| `HPL Step 2 Execution.png` | Singularity exec to verify HPL.dat |
| `HPL Step 3 Execution Before.png` | Setting SINGULARITY_BINDPATH |
| `HPL Step 4 Execution.png` | Running GPU-accelerated HPL via mpirun |
| `HPL Results on A100.png` | A100 performance: 1 GPU vs 2 GPUs, N=20K-100K |
| `HPL Results on H100.png` | H100 performance: 1 GPU vs 2 GPUs, N=20K-100K |
| `HPL Results : A100 vs. H100.png` | Side-by-side bar chart with speedup ratios (1.60× to 2.51×) |
