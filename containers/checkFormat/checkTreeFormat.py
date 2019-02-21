#!/usr/bin/env python3

import sys
import os
import argparse
from Bio import Phylo

def check_arg (args=None) :
    parser = argparse.ArgumentParser(prog = 'checkTreeFormat.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'CheckNewickFormat.py is a phylogenetic tree validator. It takes a tree file in newick or nexus format, checks its sanity and exports a canonical newick file.')

    parser.add_argument('--version', action='version', version='%(prog)s 0.3.5')

    parser.add_argument('-tree_file', required= True, help ='Path to tree file')
    parser.add_argument('-tree_format', required= True,choices = ["newick","nexus"], help = 'Tree file format [newick,nexus]')
    parser.add_argument('-output', required= False, help = 'Path to result tree file.Default = tree.nwk', default="tree.nwk")
    parser.add_argument('-event_id', required= False, help = 'OpenEbench event identifier', default="default")

    return parser.parse_args()


if __name__ == '__main__' :
    version = 'checkTreeFormat v1.0'

    arguments = check_arg(sys.argv[1:])

    # Checking if file exists
    if (not os.path.exists(arguments.tree_file)):
        print("Tree file not found.")
        sys.exit(1)

    # Read file, check it is in the correct format.
    try:
        tree = Phylo.read(arguments.tree_file, arguments.tree_format)
    except:
        if(arguments.tree_format == "newick"):
            print("Tree file not in newick format.")
        elif(arguments.tree_format == "nexus"):
            print("Tree file not in nexus format.")
        raise
        sys.exit(1)

    # If format =! newick convert to canonical format.
    if(arguments.tree_format != "newick"):
        print("Tree file not in canonical format. Converting to newick...")
    else:
        print("Tree is already in newick format, printing...")

    # Writing tree in newick format
    try:
        Phylo.write(tree,arguments.output,"newick")
        print("Successfully converted/printed to newick format! Saved in " + arguments.output)
    except:
        print("Conversion/printing to newick failed.")
        raise
        sys.exit(1)


    #for leaf in tree.get_terminals():
    #    print(leaf.name)
