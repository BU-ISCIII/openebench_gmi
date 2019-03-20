#!/usr/bin/env python3

import sys
import os
import argparse
import json
import subprocess
#from Bio import Phylo
#from Bio.Phylo.Applications import RaxmlCommandline
import dendropy
from dendropy.calculate import treecompare

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
        tns = dendropy.TaxonNamespace()
        tree1 = dendropy.Tree.get_from_path(
            arguments.tree_file1,
            "newick",
            taxon_namespace=tns)
        tree2 = dendropy.Tree.get_from_path(
            arguments.tree_file2,
            "newick",
            taxon_namespace=tns)
        tree1.encode_bipartitions()
        tree2.encode_bipartitions()
        print("Trees read successfully.")
    except:
        print("Trees couldn't be concatenated.")
        raise
        sys.exit(1)

    # Calculate Robinson-Foulds distance between two trees REF and test
    try:
        print("Calculating robin-foulds distance...")
        rf_distance = treecompare.symmetric_difference(tree1, tree2)
        wrf_distance = treecompare.weighted_robinson_foulds_distance(tree1, tree2)
        print("Calculation of robin-foulds distance failed.")
    except:
        print("Robinson-foulds distance calculation failed.")
        raise
        sys.exit(1)


    #Create ids dictionary with event_id and sample ids from tree leaves.
    try:
        metrics.update(testEventId = arguments.event_id)
        metrics_info1.update(type="metrics",units="none",name="Unweighted Robinson-Foulds metric",value=rf_distance)
        metrics_info2.update(type="metrics",units="none",name="Weighted Robinson-Foulds metric",value=wrf_distance)
        metrics.update(metrics = {'x' : metrics_info1, 'y' : metrics_info2 })

        print("Successfully extracted ids from tree file.")
    except:
        print("Conversion/printing to newick failed.")
        raise
        sys.exit(1)

    # Outputting in json format
    try:
        with open (arguments.output,"w") as write_file:
            json.dump(metrics,write_file,indent=4)
        write_file.close()
        print("Successfully created json output with ids.")
    except:
        print("Creating json output file failed.")
        raise
        sys.exit(1)
