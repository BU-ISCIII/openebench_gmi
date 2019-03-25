#!/usr/bin/env python3

import sys
import os
import io
import argparse
import json

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
    parser = argparse.ArgumentParser(prog = 'compareIds.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'compareIds.py takes two json files containing sample ids and exits with 0 or 1 if both json contains the same ids.')

    parser.add_argument('--version', action='version', version='%(prog)s 0.3.5')
    parser.add_argument('--ids1','-i1', required= True, help ='Path to ids 1 json file')
    parser.add_argument('--ids2','-i2' ,required= True, help = 'Path to ids 2 json file')

    return parser.parse_args()


###################
### MAIN SCRIPT ###
###################

if __name__ == '__main__' :

    # Variables
    version = 'compareIds v1.0'  # Script version
    arguments = ""                    # Arguments from ArgParse
    tree = ""                         # Tree variable

    # Grab arguments
    arguments = check_arg(sys.argv[1:])

    # Checking if file exists
    if (not os.path.exists(arguments.ids1)):
        print("IDs 1 json file doen't exists.")
        sys.exit(1)

    if (not os.path.exists(arguments.ids2)):
        print("IDs 2 json file doen't exists.")
        sys.exit(1)

    # Read file, check it is in the correct format.
    try:
        with io.open(arguments.ids1,mode='r',encoding="utf-8") as f1:
            ids1 = json.load(f1)
        with io.open(arguments.ids2,mode='r',encoding="utf-8") as f2:
            ids2 = json.load(f2)
    except:
        print("Failed to load json files.")
        raise
        sys.exit(1)

    #Check if same ids are present in both files
    if(set(ids1['queryIds']) == set(ids2['queryIds'])):
        print("Participant data contains same ids than input dataset.")
        sys.exit(0)
    else:
        print("Failed: Participant data contains different ids than input dataset.")
        sys.exit(1)
