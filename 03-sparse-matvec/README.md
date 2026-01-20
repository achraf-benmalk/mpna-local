# Sparse Distributed Matrix-Vector Multiplication

## Description

This exercise aims to implement a function that multiplies a sparse distributed matrix by a vector.

Given a sparse matrix `A` of dimensions `n x n` and a vector `x` of dimension `n`, the product of `A` and `x` is a vector `y` of dimension `n` such that `y[i]` is the dot product of the `i`-th row of `A` and the vector `x`.

## Serial CSR Implementation

You will implement such a function in C (or C++) in the following. The Compressed Sparse Row (CSR) format will represent the matrix.
In order to test your implementation, you can read a matrix from a file in Matrix Market format and a vector from a file in plain text format.
Test matrices can be found in the data directory, and more can be found at https://sparse.tamu.edu/. You are welcome to choose or generate vectors as you wish.

## Distributed CSR Implementation

Once you have a working serial implementation, you can extend it to a distributed memory setting. You will use MPI to distribute the matrix among the processes.

You can distribute the matrix in a block-cyclic fashion, where each process will have a block of rows of the matrix. The block size can be fixed or computed based on the number of processes and the matrix size.

You will comment on the performance of your implementation and compare it to the serial version. In particular, you will measure the speedup and efficiency of your parallel implementation.

## Application: Eigenvalue Problem

You will use matrix-vector multiplication to solve an eigenvalue problem.

### Power Iteration
You will use the power iteration method to compute the largest magnitude eigenvalue of `A`.

Evaluate the convergence of the method as a function of the matrix size and the number of processes.
Comment on the algorithm's correctness by comparing your result with your knowledge of eigenvalue properties (Gershgorin circles for example).

