#!/usr/bin/env python3

import sys
import os
import argparse
import json
import subprocess
from ete3 import Tree

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
    parser = argparse.ArgumentParser(prog = 'calculateSnPrecision.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'calculateSpPrecision.py calculates Specificity and Precision metric between two newick trees using RAxML.')

    parser.add_argument('--version','-v', action='version', version='%(prog)s 0.3.5')

    parser.add_argument('--tree_file1','-t1', required= True, help ='Path to tree file 1')
    parser.add_argument('--tree_file2','-t2', required= True, help ='Path to tree file 2')
    #parser.add_argument('--tree_format','-f' ,required= False,choices = ["newick","nexus"], help = 'Tree file format [newick,nexus]', default = "newick")
    parser.add_argument('--output' ,'-o',required= False, help = 'Path to result metric json. Default = specificityPrecision.json', default="specificityPrecision.json")
    parser.add_argument('--event_id','-e' ,required= False, help = 'OpenEbench event identifier', default="default")
    parser.add_argument('--participant_id','-p' ,required= False, help = 'OpenEbench participant identifier', default="default")

    return parser.parse_args()

def calculate_sensitivity(true_positives, false_negatives) :
    sensitivity = true_positives /(true_positives + false_negatives)
    return sensitivity
    
def calculate_precision(true_positives, false_positives) :
    precision = true_positives /(true_positives + false_positives)
    return precision


###################
### MAIN SCRIPT ###
###################

if __name__ == '__main__' :

    # Variables
    version = 'calculateSnPrecision v1.0'  # Script version
    arguments = ""                        # Arguments from ArgParse
    tree = ""                             # Tree variable
    metrics = {}                          # IDs dictionary
    metrics_info1 = {}                     # Leaves list
    metrics_info2 = {}

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
        print("Reading Trees...")
        tree1 = Tree(arguments.tree_file1)
        tree2 = Tree(arguments.tree_file2)
        print("Setting root on midpoint...")
        tree1_outgroup = tree1.get_midpoint_outgroup()
        tree1.set_outgroup(tree1_outgroup)
        tree2_outgroup = tree2.get_midpoint_outgroup()
        tree2.set_outgroup(tree2_outgroup)
        print("Collapsing nodes with branch distance = 0...")
        for node_tree1 in tree1.get_descendants():
            #print(node2.dist)
            #if not node2.is_leaf() and round(node2.dist,4) <= 1:
            if not node_tree1.is_leaf() and node_tree1.dist <= 1.00000050002909e-06:
                node_tree1.delete()
        for node_tree2 in tree2.get_descendants():
            #print(node2.dist)
            #if not node2.is_leaf() and round(node2.dist,4) <= 1:
            if not node_tree2.is_leaf() and node_tree2.dist <= 1.00000050002909e-06:
                node_tree2.delete()
        print("Trees read successfully.")
    except:
        print("Trees couldn't be loaded.")
        raise


    # Calculate Robinson-Foulds distance between two trees REF and test
    try:
        print("Calculating robinson-foulds distance...")
        results = tree1.compare(tree2)
        print("Calculation of robin-foulds distance failed.")
    except:
        print("Robinson-foulds distance calculation failed.")
        raise


    true_positives = len(results["common_edges"])
    false_positives = len(results["source_edges"]-results["ref_edges"])
    false_negatives = len(results["ref_edges"]-results["source_edges"])
    sensitivity = calculate_sensitivity(true_positives, false_negatives)
    precision = calculate_precision(true_positives, false_positives)

    #Create ids dictionary with event_id and sample ids from tree leaves.
    try:
        
        metrics.update(event_id = arguments.event_id)
        metrics.update(participant_id = arguments.participant_id)
        metrics_info1.update(type="metrics",units="none",name="sensitivity",value=sensitivity)
        metrics_info2.update(type="metrics",units="none",name="precision",value=precision)
        metrics.update(metrics = {'x' : metrics_info1, 'y' : metrics_info2 })

        print("Successfully extracted ids from tree file.")
    except:
        print("Conversion/printing to newick failed.")
        raise

    # Outputting in json format
    try:
        with open (arguments.output,"w") as write_file:
            json.dump(metrics,write_file,indent=4)
        write_file.close()
        print("Successfully created json output with ids.")
    except:
        print("Creating json output file failed.")
        raise
