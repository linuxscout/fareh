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
        self.category_english =""
        self.mark_pos = 0
        self.example_marker_pos = 0
        self.inflected = ""
        self.regexp = ""
        self.postag = ""        
    def set_category(self, category=""):
        """ set the error rule category"""
        self.category = category
    def set_category_english(self, category=""):
        """ set the error rule category"""
        self.category_english = category
    
    def add_pattern(self,pattern, mark_pos = "", inflected="",  regexp="", postag="", skip=""):
        """ add pattern """
        self.pattern = araby.tokenize(self.clean(pattern))
        try:
            self.mark_pos = int(mark_pos) - 1
        except ValueError:
            self.mark_pos = 0
        self.inflected = inflected
        self.regexp = regexp
        self.postag = postag
        try:
            self.skip = int(skip)
        except ValueError:
            self.skip = 0
        
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
    
    def add_example(self, example, correction=[],  mark_pos ="", correct=False):
        """ add pattern """
        if mark_pos:
            try:
                self.example_marker_pos = int(mark_pos) - 1
            except ValueError:
                self.example_marker_pos = 0
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
        #if type(strng) == str or type(strng) == unicode:
        if type(strng) == str:#python3
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
        tokens = [araby.strip_tashkeel(t) for t in self.pattern]
        
        # make attributes
        attributes = []
        if self.inflected =="yes":
            attributes.append('inflected="yes"')
        if self.regexp =="yes":
            attributes.append('regexp="yes"')
        if self.postag:
            attributes.append('postag="%s" postag_regexp="yes"'%self.postag)
        if self.skip:
            attributes.append('skip="%d"'%self.skip)
        attributes = u" ".join(attributes)


        if self.category == u"صفة":
            if len(tokens) >= 2:
                pattern = u"""<unify>
          <feature id="definite"/><feature id="gender"/><feature id="case"/> <feature id="number"/>
          <token inflected="yes">%s</token>
          <marker><token inflected="yes"  postag="N.*;.*;--.?" postag_regexp="yes">%s</token></marker>
        </unify>"""%(tokens[0], tokens[1])
            # treat extra tokens in a context
            if len(tokens) > 2:
                for token in self.pattern[2:]:
                    token = araby.strip_tashkeel(token)
                    pattern += u"   <token>%s</token>\n"%token                
        elif self.category == u"كلمة واحدة":
            if len(tokens) >= 1:
                # one word is often wrong
                pattern = u"""<marker><token regexp="yes">(&procletics;)?%s</token></marker>"""%(tokens[0])
            # treat extra tokens in a context
            if len(tokens) > 1:
                for token in self.pattern[1:]:
                    token = araby.strip_tashkeel(token)
                    pattern += self.make_token(token)                
        elif self.category in (u"فعل", u"متعدي بحرف",):
            for i in range(len(tokens)):
                if i == self.mark_pos :
                    # one word is often wrong
                    pattern += u"""<marker>%s</marker>"""%self.make_token(self.pattern[i], attributes)

                # treat extra tokens in a context
                else:
                    token = self.pattern[i]
                    # some categories impose diacritized tokens out of marker
                    if self.category not in (u"متعدي بحرف",):
                        token = araby.strip_tashkeel(token)
                    pattern += self.make_token(token, attributes)
        else:
            for token in self.context:
                token = araby.strip_tashkeel(token)
                pattern += self.make_token(token)
            pattern = "<marker>%s</marker>"%pattern
        return pattern
        
    def make_context(self,):
        """ add context """
        pass
    def make_ruleid(self,):
        """ Build id rule by combining category, number and name"""
        # romanize arabic name
        
        name = pyarabic.trans.convert(self.rulename,'arabic','ascii')
        # convert spaces 
        name = name.replace(" ", "_")
        # remove extra chars
        name = re.sub('[^a-zA-Z0-9_]','_',name)
        #~ ruleid = self.category_english+"_%04d_%s"%(self.ruleid, name)
        ruleid = u"%s_%s"%(self.ruleid, name)
        return ruleid
        
    def make_token(self, token, attributes=""):
        """ Prapare a token"""
        # if token is stop word
        # make it as regular expression
        entity = builder_const.ENTITIES.get(token, token)
        if token != entity:
            line = u'   <token regexp="yes">%s</token>\n'%entity           
        
        else:
            line = u"   <token %s>%s</token>\n"%(attributes,token)
        return line
    def make_suggestions(self, ):
        """ add suggestion """
        suggestions = ""
        if self.category == u"صفة":
            suggestions = """<match no="1"/>&nbsp;"""            
            for sug in self.suggestions:
                sug_tokens = araby.tokenize(sug)
                sug_tokens = [araby.strip_lastharaka(s) for s in sug_tokens]
                tokens = [araby.strip_tashkeel(t) for t in self.pattern]
                if len(tokens) >= 2 :
                    match = tokens[1]
                else:
                    match = "TODO"
                if len(sug_tokens) >= 2 :
                    suggest = sug_tokens[1]
                else:
                    suggest = sug
                suggestions += u"""   <suggestion><match no="2" regexp_match="%s" regexp_replace="%s"/></suggestion>\n"""%(match,suggest)
        elif self.category in (u"كلمة واحدة", u"فعل"):
            suggestions = ""            
            for sug in self.suggestions:
                sug_tokens = araby.tokenize(sug)
                sug_tokens = [araby.strip_lastharaka(s) for s in sug_tokens]
                tokens = [araby.strip_tashkeel(t) for t in self.pattern]
                if len(tokens) >= 1 :
                    match = tokens[0]
                else:
                    match = "TODO"
                if len(sug_tokens) >= 1 :
                    suggest = sug_tokens[0]
                else:
                    suggest = sug
                suggestions += u"""   <suggestion><match no="1" regexp_match="%s" regexp_replace="%s"/></suggestion>\n"""%(match,suggest)            
        # make suggestion for verb category
        else:
            for sug in self.suggestions:
                suggestions += u"   <suggestion>%s</suggestion>\n"%sug
        return suggestions

    def make_marker(self, marker):
        """ make marker """
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
        #~ print('#********************%s'%self.example_marker_pos)
        
        for exmp in self.examples["incorrect"]:
            ex_tokens = araby.tokenize(exmp)
            try:
                pat = ex_tokens[self.example_marker_pos]
                exmp = exmp.replace(pat, "<marker>%s</marker>"%pat)

            except:
                pat = "Example with problem"
                exmp = "Example with problem" + exmp
                #~ print(exmp, self.example_marker_pos)
                #~ sys.exit()

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
        rule_id = self.make_ruleid()
        rulexml = u"<!-- %s %s -->" %(rule_id," ".join(self.context))
        rulexml += u""" <rule id ='%s' name='%s'>

  <pattern>
%s  </pattern>
  <message>%s</message>
  %s
 </rule>
        """%(rule_id, self.rulename, pattern, message, examples)
        

        #~ rulexml = self.pretty(rulexml)
        return rulexml

    def pretty(self, rulexml):
        """ Convert xml rule to pretty format
        """
        # indent xml string
        rulexml = re.sub("[\t\n]","", rulexml)
        #.replace("\t"," ")
        #rulexml = rulexml.replace("\n","")
        rulexml = xml.dom.minidom.parseString(rulexml)
        rulexml = rulexml.toprettyxml(indent=" ")
        rulexml = rulexml.replace('<?xml version="1.0" ?>','')
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
        
        rule_xml = xml.dom.minidom.parseString(rule)
        rule_pretty_xml = xml.toprettyxml(indent=";")
        print(rule_pretty_xml)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
