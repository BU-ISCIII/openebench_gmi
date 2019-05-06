

```python
import sys
import os
import argparse
import json
import subprocess
from ete3 import Tree
```


```python
tree2 = Tree("datasets/goldenDataset/SIM-Sbareilly.tre")
tree2_outgroup = tree2.get_midpoint_outgroup()
tree2.set_outgroup(tree2_outgroup)
tree1 = Tree("datasets/testResultDataset/participant3.nwk")
tree1_outgroup = tree1.get_midpoint_outgroup()
tree1.set_outgroup(tree1_outgroup)

tree3 = Tree("datasets/testResultDataset/participant1.nwk")
tree3_outgroup = tree3.get_midpoint_outgroup()
tree3.set_outgroup(tree3_outgroup)

```


```python
for node_tree1 in tree1.get_descendants():
    if not node_tree1.is_leaf() and node_tree1.dist <= 1.00000050002909e-06:
        node_tree1.delete()
for node_tree2 in tree2.get_descendants():
    if not node_tree2.is_leaf() and node_tree2.dist <= 1.00000050002909e-06:
        node_tree2.delete()
```


```python
results = tree1.compare(tree2)
results

```




    {'rf': 1.0,
     'max_rf': 11.0,
     'ref_edges_in_source': 0.8333333333333334,
     'source_edges_in_ref': 1.0,
     'effective_tree_size': 23,
     'norm_rf': 0.09090909090909091,
     'treeko_dist': 'NA',
     'source_subtrees': 1,
     'common_edges': {('SIM_CFSAN000189',
       'SIM_CFSAN000191',
       'SIM_CFSAN000211',
       'SIM_CFSAN000212',
       'SIM_CFSAN000228',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000189',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000211', 'SIM_CFSAN000212', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000211', 'SIM_CFSAN000212'),
      ('SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140')},
     'source_edges': {('SIM_CFSAN000189',
       'SIM_CFSAN000191',
       'SIM_CFSAN000211',
       'SIM_CFSAN000212',
       'SIM_CFSAN000228',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000189',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000211', 'SIM_CFSAN000212', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000211', 'SIM_CFSAN000212'),
      ('SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140')},
     'ref_edges': {('SIM_CFSAN000189',
       'SIM_CFSAN000191',
       'SIM_CFSAN000211',
       'SIM_CFSAN000212',
       'SIM_CFSAN000228',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000189',
       'SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000211', 'SIM_CFSAN000212', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000191', 'SIM_CFSAN000228'),
      ('SIM_CFSAN000211', 'SIM_CFSAN000212'),
      ('SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000961',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140'),
      ('SIM_CFSAN000661',
       'SIM_CFSAN000669',
       'SIM_CFSAN000700',
       'SIM_CFSAN000752',
       'SIM_CFSAN000753',
       'SIM_CFSAN000951',
       'SIM_CFSAN000952',
       'SIM_CFSAN000954',
       'SIM_CFSAN000958',
       'SIM_CFSAN000960',
       'SIM_CFSAN000963',
       'SIM_CFSAN000968',
       'SIM_CFSAN000970',
       'SIM_CFSAN001112',
       'SIM_CFSAN001115',
       'SIM_CFSAN001118',
       'SIM_CFSAN001140')}}




```python
true_positives = len(results["common_edges"])
false_positives = len(results["source_edges"]-results["ref_edges"])
false_negatives = len(results["ref_edges"]-results["source_edges"])
```


```python
sensitivity = true_positives/(true_positives + false_negatives)
precision = true_positives/(true_positives + false_positives)
```


```python
print(sensitivity)
print(precision)
```

    0.8571428571428571
    1.0

