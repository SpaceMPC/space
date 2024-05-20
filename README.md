# Space MPC
This repository allows you to execute MP-SPDZ protocols for two satellite programs.

First, follow the installation instructions for [MP-SPDZ](https://github.com/data61/MP-SPDZ).

Then to execute our programs:
```
cd quadratic
../utils/execute.py qp3.mpc -E [MP-SPDZ protocol] -n [number of times to repeat] -p [path to MP-SPDZ compile-run.py]
```

For example, to execute the quadratic program 10 times:
```
cd quadratic
../utils/execute.py qp3.mpc -E hemi2k -n 10 -p ../../MP-SPDZ/Scripts/compile-run.py
```
