#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test.py
#   Convert a file which contains grammar rules into grammar xml format for LanguageTool
#   The text file contains linguistic rules from book of "Guide of Commons errors" n by  Marwan Albawab
# الملف معالج يدويا ومجهز للبرمجة
# الملف فيه الأعمدة التالية:
# * number الرقم
# * rule id: رقم القاعدة
# * status: الحالة
# * error category: صنف الخطأ
# * style pattern النمطة
# * correction المستبدل
# * note الملاحظة
# * Error  الخطأ
# * Correction التصحيح



import sys
import os
import argparse
import  rule_builder
import  rule_converter_xml
scriptname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
scriptversion = '0.1'
Separator="\t"

AuthorName="Taha Zerrouki"

# Limit of the fields treatment

MAX_LINES_TREATED=1100000;


def grabargs():
    parser = argparse.ArgumentParser(description='Convert rules dictionary to xml rule grammar.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-d", dest="outformat", nargs='?',
    help="output format(csv, xml)", metavar="FORMAT")

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

def converter_factory(out_format="csv", category="all", version="N/A"):
    """ create a converter"""
    if out_format == "xml":
        return rule_converter_xml.rule_converter_xml(category, version)   
    else:
        return rule_converter.rule_converter(category, version)   
def main():
    args= grabargs()
    filename = args.filename
    limit = args.limit
    output_format =args.outformat
    category = args.category
    version = args.version

    try:
        fl = open(filename, encoding='utf8');
    except:
        print(" Error :No such file or directory: %s" % filename)
        sys.exit(0)

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

    myconverter = converter_factory("xml", category, version)    
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
