# Minimising TLB misses using Large Pages 

This is part of Assignment 2 of course E0-243 High performance Computer Architecture offered at CSA department at Indian Institute of Science.

We are given an unknown workload `libwork.so` which does not access all the allocated memory in a uniform manner. Hence, we need to first identify the virtual address regions that witness the most TLB misses and later deploy these regions with large pages so that the TLB misses are minimised and overall program performance is improved.


To achieve this, we have used ``sudo perf mem record`` and ``sudo perf mem report`` to know the memory access patterns in given woprkload and whether they were TLB miss or hit and store them in a file called `mem_accesses.txt`.

Then run the python script `analyze.py` using command 
```
python3 analyze.py n
```
This gives the top n pages witnessing highest TLB misses in the file `largepages.txt`.

After getting top 8 pages, update the `main.c` file to allocate large pages of size 2MB to these virtual address regions and then again run `perf mem record & perf mem report` to again access regions witnessing TLB Misses in file `mem_accesses2.txt`.

We plotted graph of Number of TLB misses before and after allocating large pages and observed a significant decrease in them. 
We also observed a significant decrease in execution time of workload that had a speed up of 1.6.





