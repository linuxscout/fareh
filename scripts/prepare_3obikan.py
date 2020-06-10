#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  3obikan.py
#   Convert a data base of 3obikan to  rules file


import sys
import os
import argparse
#~ import differ
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
Separator="\t"

AuthorName="Taha Zerrouki"
import rule_converter_obikan
import rule_converter
# Limit of the fields treatment

MAX_LINES_TREATED=1100000;


def grabargs():
    parser = argparse.ArgumentParser(description='Convert rules dictionary to xml rule grammar.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-d", dest="done", nargs='?',
    help="Get the done file", metavar="DONE FILE")

    parser.add_argument("-v", dest="version", nargs='?',
    help="Release version", metavar="Version")
    
    parser.add_argument("-a",dest="all", type=bool, nargs='?',
                        const=True, 
                        help="Generate all categories")
    parser.add_argument("-l",dest="limit", type=int, nargs='?',
                         help="the limit of treated lines")
    parser.add_argument("-t",dest="category", type=str, nargs='?', default="all",
                        help="generate only the category of errors(oneword, expression, collocations, indirect-transitive,verb, adjective)")
    args = parser.parse_args()
    return args                                                   

def converter_factory(out_format="csv", dones=[], version="N/A"):
    """ create a converter"""
    if out_format == "obikan":
        return rule_converter_obikan.rule_converter_obikan(dones, version)   
    else:
        return rule_converter.rule_converter("all", version) 
def read_done(fl):
    """
    return a list of patterns
    """
    line = fl.readline()
    text = u""
    rule_table = [];
    nb_field = 2;
    while line :
        line = line.strip()
        if not line or not line.startswith("#"):
           rule_table.append(line);
        line = fl.readline()
    fl.close();
    return rule_table
    
def main():
    args= grabargs()
    filename = args.filename
    limit = args.limit
    category = args.category
    version = args.version
    done_filename = args.done
    try:
        fl = open(filename, encoding='utf8');
    except:
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)
    if done_filename:
        try:
            fldone = open(done_filename, encoding='utf8');
        except:
            print(" Error :No such file or directory: %s" % done_filename)
            sys.exit(0)        
    
        dones = read_done(fldone)
    else:
        dones =[]

    line = fl.readline()
    text = u""
    rule_table = [];
    nb_field = 2;
    while line :
        line = line.strip('\n')#.strip()
        if not line.startswith("#"):
            liste = line.split(Separator);
            if len(liste) >= nb_field:
                rule_table.append(liste);

        line = fl.readline()
    fl.close();

    model = 0;
    myconverter = converter_factory("obikan", dones, version)    
    # create header
    h = myconverter.add_header()
    if h:
        print(h)
    for tuple_rule in rule_table[:limit]:
        l = myconverter.add_record(tuple_rule)
        if l:
            print(l)
    # create footer
    f = myconverter.add_footer()
    if f:
        print(f)
        
    
if __name__ == "__main__":
  main()
