# perf
1. install perf
```
kubectl exec -it tm-performance-client-0 -- sh  
microdnf install perf
```
if you have no permission, you can also install perf via dockerfile  
3. collect on-cpu on your container，the result will be stored under current dir.  
```
perf record -e cpu-clock --call-graph dwarf -p 110 -- sleep 120
```
this cmd means to collect the CPU usage of process 110 for 120seconds. There are also parameters for "perf", please refer to "perf -h"  
4. install perl which used for drawing diagram in your container.  
```
microdnf install perl
```
if you have no permission, you can also install perf via dockerfile.  
5. download Flamegraph on your host and copy it to your conatiner  
```
git clone https://github.com/brendangregg/FlameGraph.git  
kubectl cp FlameGraph tm-performance-server-0:/tmp/FlameGraph  
```
you can also do this step on your dockerfile, if you have no permission to copy.  
6. drawing diagram  
```
perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > client_timer.svg
```
this command shall be run under the dir which perf result located.
