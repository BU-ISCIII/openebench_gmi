#!/usr/bin/env python3

import sys
import os
import argparse
import json
import subprocess
from ete3 import Tree
import shutil

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
    parser.add_argument('--benchmark_trees_path','-b', required= True, help ='Path to benchmark path where other participants tree are found.')
    parser.add_argument('--output' ,'-o',required= False, help = 'Path to result metric json.Default = participant_matrix.json', default="participant_matrix.json")
    parser.add_argument('--event_id','-e' ,required= False, help = 'OpenEbench event identifier', default="default")
    parser.add_argument('--participant_id','-p' ,required= False, help = 'OpenEbench participant identifier', default="default")

    return parser.parse_args()


#################
### FUNCTIONS ###
#################
def midpoint_root (tree):
    tree_outgroup = tree.get_midpoint_outgroup()
    tree.set_outgroup(tree_outgroup)
    return tree
def collapse_nodes (tree, branch_length):
    for node_tree in tree.get_descendants():
        if not node_tree.is_leaf() and node_tree.dist <= branch_length:
            node_tree.delete()
    return tree

###################
### MAIN SCRIPT ###
###################

if __name__ == '__main__' :

    # Variables
    version = 'calculateRobinFouldsMetric v1.0'  # Script version
    arguments = ""                        # Arguments from ArgParse
    tree = ""                             # Tree variable
    metrics = {}                          # IDs dictionary
    metrics_info1 = {}                     # Leaves list
    metrics_info2 = {}
    participants = []
    participant_row = []
    tree_files = []

    # Grab arguments
    arguments = check_arg(sys.argv[1:])

    # Checking if file exists
    if (not os.path.exists(arguments.tree_file1)):
        print("Tree file 1 not found.")
        sys.exit(1)

    if (not os.path.exists(arguments.benchmark_trees_path)):
        print("Benchmark path with public participants trees not found.")
        sys.exit(1)

    # Read benchmark data
    in_file =  os.path.join(arguments.benchmark_trees_path,"participant_matrix.json")

    with open(in_file) as json_file:
        data = json.load(json_file)

    participants = data["participants"]
    participants.append(arguments.participant_id)
    benchmark_data = data["matrix"]["values"]

    try:
        shutil.copy(arguments.tree_file1,arguments.benchmark_trees_path)
    except:
        print("New participant tree couldn't be copied to benchmark folder.")

    # Read file, check it is in the correct format.
    try:
        print("Reading participant tree, midpoint rooting and collapsing nodes...")
        tree_test = Tree(arguments.tree_file1)
        tree_test = midpoint_root(tree_test)
        tree_test = collapse_nodes(tree_test,1.00000050002909e-06)

    except:
        print("Failed to read and analyzed test tree.")
        raise
        sys.exit(1)

    try:
        print ("Reading public participants trees...")
        for public_participant in participants:
            tree_file = public_participant + ".nwk"
            part_fullpath = os.path.join(arguments.benchmark_trees_path,tree_file)
            if os.path.isfile(part_fullpath):
                tree_files.append(part_fullpath)

        for participant in tree_files:
            print("Reading public participant tree :" + participant)
            tree = Tree(participant)
            print("Setting root on midpoint...")
            tree = midpoint_root (tree)
            print("Collapsing nodes with branch distance = 0...")
            tree = collapse_nodes (tree, 1.00000050002909e-06 )
            results = tree_test.compare(tree)
            participant_row.append(results["norm_rf"])

        print("Public participants trees read and analyzed successfully.")
    except:
        print("Public participants trees couldn't be analyzed.")
        raise
        sys.exit(1)

    #Create ids dictionary with event_id and sample ids from tree leaves.
    try:
        print("Updating benchmark data with new participant..")
        benchmark_data.append(participant_row)
        data.update(participants=participants)
        data.update(matrix = {"values" : benchmark_data } )
    except:
        raise
        sys.exit(1)

    # Outputting in json format
    try:
        path_output = os.path.join(arguments.benchmark_trees_path,arguments.output)
        print("Creating json output: " + path_output)
        with open (path_output,"w") as write_file:
            json.dump(data,write_file,indent=4)
        write_file.close()
        print("Successfully created json output with ids.")
    except:
        print("Creating json output file failed.")
        raise
        sys.exit(1)

