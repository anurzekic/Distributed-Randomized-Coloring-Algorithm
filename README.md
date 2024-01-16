# Distributed Randomized Coloring Algorithm
This is an implementation of a distributed randomized coloring algorithm written in python. It uses the networkx package to create and generate graphs. 

## Algorithm
<em>Initially, all nodes are uncolored. Then, in synchronous iterations, each uncolored node selects a random candidate color from its list of available colors, that is, from the set of colors that none of its already permanently colored neighbors have. Then, nodes exchange their candidate colors with their neighbors. A node v that has a
candidate color c that is not selected as a candidate color by any of its neighbors gets permanently colored with c, otherwise v discards its candidate color, remains uncolored, and proceeds with the next iteration. </em>

## Running
Requires the networkx python package:
```
$ pip install networkx[default]
``` 
If you do not want to install the dependencies (e.g., numpy, scipy, etc.), you can use:
```
$ pip install networkx
```
To run the script:
```
$ python3 DistributedRandomizedColoringAlgorithm.py
```
Or:
```
$ python DistributedRandomizedColoringAlgorithm.py
```

## References
- https://networkx.org/
- https://networkx.org/documentation/stable/reference/index.html
- https://networkx.org/documentation/stable/install.html