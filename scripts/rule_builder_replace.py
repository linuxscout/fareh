#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rule_builder.py
#  
#  Copyright 2019 zerrouki <zerrouki@majd4>
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
import re
import sys
import xml.dom.minidom

import pyarabic.araby as araby
import pyarabic.trans

import builder_const
import rule_builder
class replace_builder(rule_builder.rule_builder):
    """
    rule builder from  given data
    """
    def __init__(self,):
        """
        init the rule builder 
        """
        rule_builder.rule_builder.__init__(self,)
        self.review_mark = "@"
 
    def reset(self):
        """ reset parts"""
        self.__init__()
    def add_pattern(self, pattern):
        """ add pattern """
        self.pattern = araby.strip_tashkeel(self.clean(pattern)).split("|")
        self.pattern = list(set(self.pattern))

    def make_pattern(self,):
        """ make pattern """

        tmp_patterns = self.pattern
        for pat in self.pattern:
            if pat.startswith(u"ال"):
                # strip Al definite artilce
                pat = self.review_mark+pat[2:] 
                tmp_patterns.append(pat)
        return tmp_patterns
        

    def make_ruleid(self,):
        """ Build id rule by combining category, number and name"""
        # romanize arabic name
        
        name = pyarabic.trans.convert(self.rulename,'arabic','ascii')
        # convert spaces 
        name = name.replace(" ", "_")
        # remove extra chars
        name = re.sub('[^a-zA-Z0-9_]','_',name)
        ruleid = u"%s_%s"%(self.ruleid, name)
        return ruleid
        
    def make_suggestions(self, ):
        """ add suggestion """
        suggestions = u"|".join(self.suggestions)
        return suggestions

    def make_marker(self, marker):
        """ make marker """
        self.marker = araby.tokenize(self.clean(marker))
        
    def make_message(self, suggestions):
        """ add message """
        # prepare message
        if not self.message:
            self.message = u""
        message = self.message
        return message

    
    def make_examples(self,):
        """ make xml format example """
        return  self.examples["incorrect"] +  self.examples["correct"]



    def build(self, ):
        """ build actual rule treat rule to be displayed as LT grammar as text file
        pattern=suggestions\tmessage
        input format is 
            rule['pattern']      ;
            rule['suggestions']    
            rule['message']        ;
            rule['wrong_example']  ;
            rule['correct_example'];    
        """
        # every part is generated according to category
        # prepare pattern
        patterns = self.make_pattern()
        # prepare suggestions
        suggestions = self.make_suggestions()
        # prepare message
        message = self.make_message(suggestions)
        # prepare examples
        examples = self.make_examples()
        rule_id = self.make_ruleid()
        ruletext = ""
        ruletext += "#idr "+ rule_id +"\n"
        ruletext += "#ptt "+ u"|".join(patterns) +"\n"
        ruletext += "#sgg "+ suggestions +"\n"
        ruletext += "#msg "+ message +"\n\n"
        for i, patt in enumerate(patterns):
            if i:
                ruletext += u"#%s [%d]\n"%(rule_id,i)
            else:
                ruletext += u"#%s\n"%(rule_id)
            if self.is_to_review(patt):
                suggestions = self.review_suggestions(patt)
            ruletext += u"%s=%s\t%s\n"%(patt, suggestions, message)
        return ruletext

    def is_to_review(self, pattern):
        """ check if pattern need review"""
        return self.review_mark in pattern

    def strip_al(self, word):
        """
        if the word has an Al definite article and starts by a sun letter and its vocalized,
        we correct the shadda position
        """
        if not word.startswith(u"ال"):
            return word
        else:
           word = word[2:]
           word = re.sub(u"^([%s])(%s)"%(u"".join(araby.SUN),araby.SHADDA), word[0], word, 1, re.UNICODE)
           return word

    def review_suggestions(self, pattern):
        """
        review suggesions according to pattern
        """
        sug_list = []
        if self.review_mark in pattern:
            for sug in self.suggestions:
                if sug.startswith(u"ال"):
                   sug = self.strip_al(sug)
                   sug_list.append(sug)
        if sug_list:
            return u"|".join(sug_list)
        else:
            return u"|".join(self.suggestions)

def main(args):
    # build a rule
    rb = replace_builder()
    dataset=[
    {"pattern":u"يا أبَتِي",
    "marker":u"يا أبَتِي",
    "example":u"ياأبَتِي",
    "suggestions":u"يا أبَتِ",
    "message":u"التاء عِوَضٌ من الياء المحذوفة",
    },
     {"pattern":u"داوود|طاووس",
    "marker":u"",
    "example":u"", 
    "suggestions":u"داود|طاوس",
    "message":u"العرب تكره توالي الواوين",
    },
    
       ]
    for i, d in enumerate(dataset):
        rb.reset()
        rb.add_rulename(i, "unsorted_%d"%i)
        rb.add_pattern(d["pattern"])
        rb.add_message(d['message'])
        rb.add_marker(d['marker'])
        rb.add_suggestions(d['suggestions'])
        rb.add_example(d['example'], d['suggestions'], d["marker"])
        rule =rb.build()
        
        #~ rule_xml = xml.dom.minidom.parseString(rule)
        #~ rule_pretty_xml = xml.toprettyxml(indent=";")
        print(rule)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
