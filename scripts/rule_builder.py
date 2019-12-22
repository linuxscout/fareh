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
import pyarabic.araby as araby

class rule_builder:
    """
    rule builder from  given data
    """
    def __init__(self,):
        """
        init the rule builder 
        """
        self.pattern = []
        self.suggestions = []
        self.message = ""
        self.marker = []
        self.examples = {"correct":[],
                        "incorrect":[]}
        self.rulename = ""
        self.ruleid = ""
        self.category =""
    def set_category(self, category=""):
        """ set the error rule category"""
        self.category = category
    
    def add_pattern(self,pattern):
        """ add pattern """
        self.pattern = araby.tokenize(self.clean(pattern))
        
    def add_context(self, context):
        """ add context """
        self.context = araby.tokenize(self.clean(context))
        
    def add_suggestions(self, suggestions=[]):
        """ add suggestion """
        self.suggestions = self.clean(suggestions.split('|'))

    def add_marker(self, marker):
        """ add marker """
        self.marker = araby.tokenize(self.clean(marker))
        
    def add_message(self, message):
        """ add message """
        self.message = self.clean(message)
    
    def add_example(self, example, correction, word_to_mark, correct=False):
        """ add pattern """
        if not correct:
            self.examples['incorrect'].append(araby.strip_tashkeel(self.clean(example)))
        else:
            self.examples['correct'].append(self.clean(example))

    def add_rulename(self, ruleid,  rulename):
        """ add pattern """
        self.rulename = rulename 
        self.ruleid = ruleid 
    
    def clean(self, strng):
        """
        clean a string from unnecessary whitespaces
        """
        if type(strng) == str or type(strng) == unicode:
            strng = araby.strip_tatweel(strng)
            return re.sub(u'\s+', ' ', strng).strip()
        if type(strng) == list:
            l= [re.sub(u'\s+', ' ', s).strip() for s in strng]
            return [araby.strip_tatweel(s) for s in l]
            
        else:
            return strng
    
    def reset(self):
        """ reset parts"""
        self.__init__()
    @staticmethod
    def find_sublist(l, s):
        sub_set = -1
        if s == []:
            sub_set = 0
        elif s == l:
            sub_set = 0
        elif len(s) > len(l):
            sub_set = -1

        else:
            for i in range(len(l)):
                if l[i] == s[0]:
                    n = 1
                    while (n < len(s)) and (l[i+n] == s[n]):
                        n += 1
                    
                    if n == len(s):
                        sub_set = i
                        break
            else:
                sub_set = -1

        return sub_set

    
    def make_pattern(self,):
        """ make pattern """
        pattern = ""
        tokens = [araby.strip_tashkeel(t) for t in self.context]
        if self.category == u"صفة":
            if len(tokens) >= 2:
                pattern = u"""<unify>
          <feature id="definite"/><feature id="gender"/><feature id="case"/> <feature id="number"/>
          <token inflected="yes">%s</token>
          <marker><token inflected="yes"  postag="N.*;.*;--.?" postag_regexp="yes">%s</token></marker>
        </unify>"""%(tokens[0], tokens[1])
            # treat extra tokens in a context
            if len(tokens) > 2:
                for token in self.context[2:]:
                    token = araby.strip_tashkeel(token)
                    pattern += u"\t\t\t<token>%s</token>\n"%token                
        elif self.category == u"كلمة واحدة":
            if len(tokens) >= 1:
                # one word is often wrong
                pattern = u"""<marker><token regexp="yes">(&procletics;)?%s</token></marker>"""%(tokens[0])
            # treat extra tokens in a context
            if len(tokens) > 1:
                for token in self.context[1:]:
                    token = araby.strip_tashkeel(token)
                    pattern += u"\t\t\t<token>%s</token>\n"%token                
            
        else:
            for token in self.context:
                token = araby.strip_tashkeel(token)
                pattern += u"\t\t\t<token>%s</token>\n"%token
            pattern = "<marker>%s</marker>"%pattern
        return pattern
        
    def make_context(self,):
        """ add context """
        pass
    def make_suggestions(self, ):
        """ add suggestion """
        suggestions = ""
        if self.category == u"صفة":
            suggestions = """<match no="1"/>&nbsp;"""            
            for sug in self.suggestions:
                sug_tokens = araby.tokenize(sug)
                sug_tokens = [araby.strip_lastharaka(s) for s in sug_tokens]
                tokens = [araby.strip_tashkeel(t) for t in self.context]
                if len(tokens) >= 2 :
                    match = tokens[1]
                else:
                    match = "TODO"
                if len(sug_tokens) >= 2 :
                    suggest = sug_tokens[1]
                else:
                    suggest = sug
                suggestions += u"""\t\t\t<suggestion><match no="2" regexp_match="%s" regexp_replace="%s"/></suggestion>\n"""%(match,suggest)
        elif self.category == u"كلمة واحدة":
            suggestions = ""            
            for sug in self.suggestions:
                sug_tokens = araby.tokenize(sug)
                sug_tokens = [araby.strip_lastharaka(s) for s in sug_tokens]
                tokens = [araby.strip_tashkeel(t) for t in self.context]
                if len(tokens) >= 1 :
                    match = tokens[0]
                else:
                    match = "TODO"
                if len(sug_tokens) >= 1 :
                    suggest = sug_tokens[0]
                else:
                    suggest = sug
                suggestions += u"""\t\t\t<suggestion><match no="1" regexp_match="%s" regexp_replace="%s"/></suggestion>\n"""%(match,suggest)            
            
        else:
            for sug in self.suggestions:
                suggestions += u"\t\t\t<suggestion>%s</suggestion>\n"%sug
        return suggestions

    def make_marker(self, marker):
        """ add marker """
        self.marker = araby.tokenize(self.clean(marker))
        
    def make_message(self, suggestions):
        """ add message """
        # prepare message
        if not self.message:
            self.message = u"يفضل أن يقال:"
        message = u"%s \n%s"%(self.message, suggestions)
        return message

    
    def make_examples(self,):
        """ make xml format example """
        corrections = u"|".join(self.suggestions)
        examples = ""
        for exmp in self.examples["incorrect"]:
            pat = araby.strip_tashkeel(u" ".join(self.pattern)) # a list of tokens
            exmp = exmp.replace(pat, "<marker>%s</marker>"%pat)
            #~ examples +=u"<example correction='%s'>\u020B %s\u020C</example>"%(corrections, exmp)
            #~ examples +=u"<example correction='%s' type='incorrect'> %s </example>\n"%(corrections, exmp)
            #~ examples +=u"<example type='incorrect'> %s </example>\n"%(exmp)
            examples +=u"<example correction='%s' type='incorrect'> %s </example>\n"%(corrections, exmp)
            
        for exmp in self.examples["correct"]:
            #~ exmp = exmp.replace(pat, "<marker>%s</marker>"%pat)
            examples +=u"<example type='correct'> %s </example>"%(exmp)
        return examples



    def build(self, ):
        """ build actual rule treat rule to be displayed as LT grammar XML
    
        XML format as:
            <rule>
            <pattern>
            <marker><token>ثلاثة</token></marker>
            <token postag='NFP'/>           
            </pattern>          
            <message>أتقصد <suggestion>ثلاث</suggestion>؟</message>
            الاسم المؤنث يسبق بعدد مذكر
            <example correction="ثلاثة"><marker>ثلاث</marker>أولاد</example>
            <example correction="ثلاث"><marker>ثلاثة</marker>بنات</example>
        </rule>
        
        input format is 
            rule['pattern']      ;
            rule['suggestions']    
            rule['message']        ;
            rule['wrong_example']  ;
            rule['correct_example'];    
        """
        # every part is generated according to category
        # prepare pattern
        pattern = self.make_pattern()
        # prepare suggestions
        suggestions = self.make_suggestions()
        # prepare message
        message = self.make_message(suggestions)
        # prepare examples
        examples = self.make_examples()
        rulexml = u"""\t<rule id ='unsorted%03.d' name='rule_%s'>

\t\t<pattern>
%s\t\t</pattern>
\t\t<message>%s\t\t</message>
\t\t%s
\t</rule>
        """%(self.ruleid, self.rulename, pattern, message, examples)
        return rulexml


def main(args):
    # build a rule
    rb = rule_builder()
    dataset=[
    {"pattern":u"يا أبَتِي",
    "marker":u"يا أبَتِي",
    "example":u"ياأبَتِي",
    "suggestions":u"يا أبَتِ",
    "message":u"التاء عِوَضٌ من الياء المحذوفة",
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
        print(rule)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
