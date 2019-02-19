from Bio import Phylo
tree = Phylo.read("int_node_labels.nwk", "newick")
for leaf in tree.get_terminals(): print leaf.name
