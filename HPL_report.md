<!-- image -->

<!-- image -->

```
1 HPLinpackbenchmarkinput file 2 InnovativeComputing Laboratory,UniversityofTennessee andFrankfurtInstituteforAdvancedStudies 3 HPLoutoutputfilename(ifany) 4 6 deviceout(6=stdout,7=stderr,file) 5 5 #ofproblemssizes(N) 6 20000400006000080000100000 Ns 7 1 #ofNBs 8 576 NBs 6 1 PMAPprocessmapping(O=Row-,1=Column-major) 10 1 #of process grids PxQ) 11 2 Ps 12 1 Qs 13 0.1 threshold 14 1 #ofpanelfact 15 1 PFACTs(0=left,1=Crout,2=Right) 16 1 #ofrecursive stopping criterium 17 64 NBMINs (>= 1) 18 1 #ofpanelsinrecursion 19 2 NDIVs 20 1 #ofrecursivepanel fact 21 0 RFACTs(0=left,1=Crout,2=Right) 22 1 #ofbroadcast 23 6 BCASTs(0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM,6=MPl) 24 1 #oflookaheadoptions 25 3 LOOKAHEADs(enable=1) 26 8 memoryalignmentindouble(>O) 27 100 Seedforthematrixgeneration
```

<!-- image -->

$singularityexec--bindS[pwd):/mnt./hpc-benchmarks\_23.10.sifcat/mnt/HPL.dat

$echoexportSINGULARITY\_BINDPATH=/home/karim.bezine-ext/lustre/sw\_stack-373lcd9r8io/users/karim.bezine-ext/src/data:/mnt&gt;&gt;-fbashrc $source-fbashrc

```
$singularityrun--nvhpc-benchmarks_23.10.sif $cd/workspace/hpl-linux-x86_64/ $mpirun-np1hpl.sh--dat/mnt/HPL.dat--gpu-affinity2--no-multinode--cuda-compat
```

<!-- image -->

<!-- image -->

<!-- image -->