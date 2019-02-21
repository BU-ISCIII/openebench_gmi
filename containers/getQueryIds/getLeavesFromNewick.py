#!/usr/bin/env python3

import sys
import os
import argparse
import json
from Bio import Phylo

#################
### FUNCTIONS ###
#################

def check_arg (args=None) :
    '''
    Description:
        Function collect arguments from command line using argparse
    Input:
        args # command line arguments
    Constant:
        None
    Variables
        parser
    Return
        parser.parse_args() # Parsed arguments

    '''
    parser = argparse.ArgumentParser(prog = 'getLeavesFromNewick.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'getLeavesFromNewick.py is a phylogenetic tree validator. It takes a tree file in newick or nexus format, checks its sanity and exports a canonical newick file.')

    parser.add_argument('--version', action='version', version='%(prog)s 0.3.5')

    parser.add_argument('-tree_file', required= True, help ='Path to tree file')
    parser.add_argument('-tree_format', required= False,choices = ["newick","nexus"], help = 'Tree file format [newick,nexus]', default = "newick")
    parser.add_argument('-output', required= False, help = 'Path to result tree file.Default = ids.json', default="ids.json")
    parser.add_argument('-event_id', required= False, help = 'OpenEbench event identifier', default="default")

    return parser.parse_args()


###################
### MAIN SCRIPT ###
###################

if __name__ == '__main__' :

    # Variables
    version = 'getLeavesFromNewick v1.0'  # Script version
    arguments = ""                        # Arguments from ArgParse
    tree = ""                             # Tree variable
    ids = {}                              # IDs dictionary
    leaves = []                           # Leaves list

    # Grab arguments
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

    # Create ids dictionary with event_id and sample ids from tree leaves.
    try:
        ids.update(testEventId = arguments.event_id)
        for leaf in tree.get_terminals():
            leaves.append(leaf.name)

        ids.update(queryIds = leaves)
        print("Successfully extracted ids from tree file.")
    except:
        print("Conversion/printing to newick failed.")
        raise
        sys.exit(1)

    # Outputting in json format
    try:
        with open (arguments.output,"w") as write_file:
            json.dump(ids,write_file,indent=4)
        write_file.close()
        print("Successfully created json output with ids.")
    except:
        print("Creating json output file failed.")
        raise
        sys.exit(1)
