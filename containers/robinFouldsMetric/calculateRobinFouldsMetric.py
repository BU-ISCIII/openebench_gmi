#!/usr/bin/env python3

import sys
import os
import argparse
import json
from Bio import Phylo
from Bio.Phylo.Applications import RaxmlCommandline

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
    parser = argparse.ArgumentParser(prog = 'calculateRobinFouldsMetric.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'calculateRobinFouldsMetric.py calculates Robin-Foulds metric between two newick trees using RAxML.')

    parser.add_argument('--version','-v', action='version', version='%(prog)s 0.3.5')

    parser.add_argument('--tree_file1','-t1', required= True, help ='Path to tree file 1')
    parser.add_argument('--tree_file2','-t2', required= True, help ='Path to tree file 2')
    parser.add_argument('--tree_format','-f' ,required= False,choices = ["newick","nexus"], help = 'Tree file format [newick,nexus]', default = "newick")
    parser.add_argument('--output' ,'-o',required= False, help = 'Path to result metric json.Default = robinfoulds.json', default="robinfoulds.json")
    parser.add_argument('--event_id','-e' ,required= False, help = 'OpenEbench event identifier', default="default")

    return parser.parse_args()


###################
### MAIN SCRIPT ###
###################

if __name__ == '__main__' :

    # Variables
    version = 'calculateRobinFouldsMetric v1.0'  # Script version
    arguments = ""                        # Arguments from ArgParse
    tree = ""                             # Tree variable
    ids = {}                              # IDs dictionary
    leaves = []                           # Leaves list

    # Grab arguments
    arguments = check_arg(sys.argv[1:])

    # Checking if file exists
    if (not os.path.exists(arguments.tree_file1)):
        print("Tree file 1 not found.")
        sys.exit(1)

    if (not os.path.exists(arguments.tree_file2)):
        print("Tree file 2 not found.")
        sys.exit(1)

    # Read file, check it is in the correct format.
    try:
        trees = [arguments.tree_file1,arguments.tree_file2]
        with open("all_trees.dnd","w") as tmp_file
        for fname in filenames:
            with open(fname) as infile:
                tmp_file.write(infile.read())
    except:
        print("Trees couldn't be concatenated.")
        raise
        sys.exit(1)

    # Calculate Robin-Foulds metric using RAxML
    raxml_cline = RaxmlCommandline(model="GTRCAT", bipartition_filename="all_trees.dnd",algorithm="r",name="Robin-Foulds")
    raxml_output = subprocess.get_output(raxml_cline)

# Create ids dictionary with event_id and sample ids from tree leaves.
#     try:
#         ids.update(testEventId = arguments.event_id)
#         for leaf in tree.get_terminals():
#             leaves.append(leaf.name)
#
#         ids.update(queryIds = leaves)
#         print("Successfully extracted ids from tree file.")
#     except:
#         print("Conversion/printing to newick failed.")
#         raise
#         sys.exit(1)
#
#     # Outputting in json format
#     try:
#         with open (arguments.output,"w") as write_file:
#             json.dump(ids,write_file,indent=4)
#         write_file.close()
#         print("Successfully created json output with ids.")
#     except:
#         print("Creating json output file failed.")
#         raise
#         sys.exit(1)
