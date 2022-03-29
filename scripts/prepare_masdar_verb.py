#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prepare_masdar_verb.py
#  
#  Copyright 2022 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import pandas as pds
import pyarabic.araby as ar
DATA_FILE= "../data/dictionaries/masdars-verbs7000.csv"
SEP=","
def treat_verb(word):
    """
    treat verb field
    """
    # remove spaces
    word = word.strip()
    # ~ # remove مص
    # ~ word = word.replace("(مص.","")
    # ~ word = word.replace("(مص ","")
    # ~ # remove paranthesis
    # ~ word = word.replace(")","")
    # if not vocalized
    if not ar.is_vocalized(word):
        word += "Unvocalized"
    # Tshakeel before ALEF with hamza and Alef
    word = word.replace(ar.ALEF_HAMZA_ABOVE, ar.ALEF_HAMZA_ABOVE+ar.FATHA)
    word = word.replace(ar.ALEF_HAMZA_ABOVE+ar.FATHA+ar.SUKUN, ar.ALEF_HAMZA_ABOVE+ar.SUKUN)
    word = word.replace(ar.ALEF_HAMZA_ABOVE+ar.FATHA+ar.SHADDA, ar.ALEF_HAMZA_ABOVE+ar.SHADDA)
    word = word.replace(ar.TATWEEL,"")
    word = word.replace(ar.ALEF+ar.FATHA, ar.ALEF)
    word = word.replace(ar.ALEF_MAKSURA, ar.FATHA+ar.ALEF_MAKSURA)
    word = word.replace(ar.ALEF, ar.FATHA+ar.ALEF)
    word = word.replace(ar.HAMZA, ar.HAMZA+ar.FATHA)
    if word.startswith(ar.FATHA):
        word = word[1:]
    if not word.endswith(ar.FATHA):
        if not word.endswith(ar.ALEF_MAKSURA) and not word.endswith(ar.ALEF):
            word += ar.FATHA
    # remove successive fatha made by replacement
    while ar.FATHA+ar.FATHA in word:
        word = word.replace(ar.FATHA+ar.FATHA, ar.FATHA)
    
    wordlist = [w.strip() for w in word.split("،")]
    
    return wordlist
    

def treat_masdar(word, extra=""):
    """
    treat masdar field
    """
    wordlist = []
    # remove spaces
    word = word.strip()
    
    # split into fields
    fields = word.split("-")
    new_word = ""
    if len(fields)== 2:
        word1 =  ar.strip_harakat(fields[0].strip())
        word2 =  ar.strip_harakat(fields[1].strip())
        if word1 == word2:
            wordlist.append(word1)
        else:

            wordlist.extend([word1,word2])
    else:
        wordlist.append(word)
    # remove spaces
    return wordlist

    
def treat_line(line):
    """
    Treat a line
    """
    list_tuple = []
    if line.startswith("#"):
        return False
    else:
        fields = line.split(SEP)
        if len(fields)>= 2:
            verbs = treat_verb(fields[0])
            masdars = treat_masdar(fields[1])
            for verb in verbs:
                for masdar in masdars:
                    list_tuple.append({"verb":verb, "masdar":masdar})
    return list_tuple;
def load_file(filename):
    """ readline and extract masdars/verbs
    """
    # open file
    try:
        fl=open(filename, "r", encoding="utf8")
    except:
        print("Can't open file:", filename)
        sys.exit()
    list_tuple= []    
    for line in fl.readlines():
        masdar_verb = treat_line(line)
        if masdar_verb:
            list_tuple.extend(masdar_verb)
    
    return list_tuple

def display(data, option="masdar"):
    """
    Display as masdar= verb  or verb to masdar
    """
    df = pds.DataFrame.from_records(data)
    # ~ print(df.head())
    dict_by_verb = df.groupby('verb')['masdar'].apply(list).to_dict()
    dict_by_masdar = df.groupby("masdar")['verb'].apply(list).to_dict()
    # ~ print(d)
    # ~ print(list_tuple)
    if option == "masdar":
        for key in dict_by_masdar:
            # key is masdar, and must be unvocalized
            key_nm = ar.strip_tashkeel(key)
            # values are verbs, must be vocalized
            verbs = dict_by_masdar[key]
            print("=".join([key_nm, "|".join(verbs)]))
    elif option == "verb":
        for key in dict_by_verb:
            # key is verb, and must be vocalized
            # value are masdars, and must be unvocalized
            masdars = [ar.strip_tashkeel(m) for m in dict_by_verb[key]]
            print("=".join([key, "|".join(masdars)]))
    else:
        print("Error: format not specified", option)
        
def generate_example(data, option="masdar"):
    """
    Display as masdar= verb  or verb to masdar
    """
    df = pds.DataFrame.from_records(data)
    # ~ print(df.head())
    dict_by_verb = df.groupby('verb')['masdar'].apply(list).to_dict()
    dict_by_masdar = df.groupby("masdar")['verb'].apply(list).to_dict()
    # ~ print(d)
    # ~ print(list_tuple)
    if option == "masdar":
        for tup in data:
            masdar = ar.strip_tashkeel(tup.get("masdar",""))
            print("الولد  يقوم بال%s"%(masdar))
    elif option == "verb":
        for tup in data:
            verb = ar.strip_tashkeel(tup.get("verb",""))
            print(" الولد  %s بأسلوب جيد"%(verb))
    else:
        print("Error: format not specified", option)
def tread_data(data):
    df = pds.DataFrame.from_records(data)
    print(df.head())
    d = df.groupby('verb')['masdar'].apply(list).to_dict()
    print(d)
def main(args):
    data = load_file(DATA_FILE)
    # generate data and example for masdars
    # ~ display(data, "masdar")
    # ~ generate_example(data,"masdar")
    # generate data and example for masdars
    display(data, "verb")
    # ~ generate_example(data,"verb")

    return 0
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
