#!/usr/bin/env python3

import re
import sys, getopt

def DoIt(inputfile, outputfile, tabstr):
    Lines = []
    if inputfile != '':
        # Read from file
        fileR = open(inputfile, 'r')
        Lines = fileR.readlines()
    else:
        Lines = sys.stdin.readlines()

    stacks = dict()
    stack = []
    tick = 0
    for line in reversed(Lines):
        # Find end of each call stack
        if line == "\t\n" or line == "\t": # empty lines: regular and the last one
            stacks[tick] = stack.copy()
            stack = []
            tick = 0
            continue
        if line[0] != '\t':
            continue
        time_str = re.search("Time:[a-zA-Z0-9]*", line)
        if time_str:
            tick = int(re.sub("Time:", "", time_str.group(0)), 16)
            stack.append(re.sub(",Time:[a-zA-Z0-9]*",'', line))
        else:
            stack.append(line)
    
    stacks[tick] = stack.copy()

    # Store all results here
    full = []

    # using items() to get all items 
    # lambda function is passed in key to perform sort by key 
    stacks_sorted = {key: val for key, val in sorted(stacks.items(), key = lambda ele: ele[0])}

    # Find minimal index of different elements for decrement offset
    minimal_diff = None
    prev = []
    for curr in stacks_sorted.values():
        index = 0
        end = min(len(prev), len(curr))
        while index < end:
            if prev[index] != curr[index]:
                break
            index += 1

        if not minimal_diff or index < minimal_diff:
            minimal_diff = index

        prev = curr

    if not minimal_diff:
        minimal_diff = 0

    # Process stacks and collect differences into container
    prev = []
    for curr in stacks_sorted.values():
        for i, ln in enumerate(curr):
            offset = 0
            if i >= minimal_diff:
                offset = i - minimal_diff
            curr[i] = re.sub("^\t", tabstr * offset, ln)

        index = 0
        end = min(len(prev), len(curr))
        while index < end:
            if prev[index] != curr[index]:
                break
            index += 1

        for el in curr[index:]:
            full.append(el)

        prev = curr

    
    if outputfile != '':
        # Write resuls to file
        fileW = open(outputfile, 'w')
        fileW.writelines(full)
    else:
        # Std out
        for x in full:
            print(x, end='')

# main
if __name__ == "__main__":
    inputfile = ''
    outputfile = ''
    tabstr = ' '
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:t:",["help=","ifile=","ofile=","tab="])
    except getopt.GetoptError:
        print ('{appname} -i <inputfile> -o <outputfile> -t <tabstr>'.format(appname = sys.argv[0]))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print ('{appname} -i <inputfile> -o <outputfile> -t <tabstr>'.format(appname = sys.argv[0]))
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--tab"):
            tabstr = arg
    DoIt(inputfile, outputfile, tabstr)
