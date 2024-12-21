# Minimising TLB misses using Large Pages 

We are given an unknown workload `libwork.so` which does not access all the allocated memory in a uniform manner. Hence, we need to first identify the vritual address regions that witness most TLB misses and later deploy these regions with large pages so that the TLB misses are minimised and perormance is improved.


