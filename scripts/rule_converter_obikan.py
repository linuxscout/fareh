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
import time
import pyarabic.araby as araby
#~ import sys

import rule_converter
import difflib

class rule_converter_obikan(rule_converter.rule_converter):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, dones=[], version="N/A"):
        """
        initiate the dict
        """
        rule_converter.rule_converter.__init__(self, "all", version)        
        # rules already managed
        self.dones = dones
        #~ print(len(dones))
        #~ sys.exit()
        self.id = 0
        self.field_id={
            'id':0,  ##الرقم الأصلي
            'root':1,  #رقم القاعدة
            'status':2,  #الحالة
            'category':3,  #صنف الخطأ
            'words':4,  #السياق
            'wrong_example':5,  #مثال خاطئ
            'correct_example':6,  #مثال صحيح
            'message':7,  #ملاحظة1
        }
        #give the display order for text format display
        self.display_order=[
            'id',  ##الرقم الأصلي
            #~ 'rule_id',  #رقم القاعدة
            'status',  #الحالة
            'words',  #الحالة
            #~ 'unvocalized',  #غير مشكول للبحث
            'category',  #صنف الخطأ
            'context',  #السياق
            'pattern',  #الخطأ
            'suggestions',  #التصحيح
            'message',  #ملاحظة1
            'wrong_example',  #مثال خاطئ
            'correct_example',  #مثال صحيح
            'example_marker_pos', # موضع الاستبدال في المثال
            'marker_pos', # موضع الاستبدال في النمط
            'inflected', # تصريف 
            'regexp',#   تعبير منتظم
            'postag', #  وسم أقسام الكلم
            'skip', # تخطي كلمة
            'remark',
            'reference',
             ]
        #generic Header for project
        self.headerlines = []
        #~ self.headerlines = [
        #~ "*************************************",
        #~ " Fareh, Our beautiful language, grammers errors rules",
                    #~ "Noun dictionary file",
                    #~ "Wordtype       : %s"%self.category,                    
                    #~ "Version        : %s"%self.version,
                    #~ "Generated at   : %s"%time.strftime("%Y/%m/%d:%H:%M"),                    
                    #~ "Author         : Taha Zerrouki", 
                    #~ "Source           : http://github.com/linuxscout/fareh",                    
                    #~ "*************************************",
                    #~ ]             
        
    def add_footer(self,):
        """
        add the footer for new dict
        """
        line = """"""
        return line
    @staticmethod
    def join_list_list(list_list, sep=u" "):
        """
        join a list of list of tokens
        """
        strng = u"|".join([sep.join(x) for x in list_list])
        return strng
    @staticmethod        
    def join_list_list_int(list_list, sep=u" "):
        """
        join a list of list of tokens
        """
        strng = u"|".join([sep.join([str(x) for x in lst]) for lst in list_list])
        return strng
        
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(noun_row)
        status =fields.get("status", False)
        if status != u"سبق":
            wrong_example = fields.get("wrong_example","")
            correct_example = fields.get("correct_example","")
            result = self.wrap_diff_line([wrong_example, correct_example])
            
            fields["pattern"] = result.get("patterns", [])
            fields["suggestions"] = result.get("suggestions", [])
            fields["context"] = result.get("context", [])
            fields["example_marker_pos"] = result.get("marker_pos", [])
            # add guessed category if no category found
            if not fields.get("category","") :
                cat = self.guess_category(fields)
                if cat:
                    fields["category"] = cat +"*"
                else:
                    fields["category"] = ""
            # guess if already treated
            if not fields.get("status","") :
                done = self.is_already_done(fields["pattern"], fields["words"], wrong_example )
                if done:
                    fields["status"] = done +"*"
                else:
                    fields["status"] = ""                    
        #
        # join positions

        
        # prepare display
        items=[];
        for key in self.display_order:
            #~ key = self.display_order[k];
            # some fields are integer, than we use str
            items.append(fields.get(key,""))
        line = u"\t".join(items);
        return line

    @staticmethod
    def guess_category(fields):
        """
        guess the category of correction
        pattern : list of token
        """
        # if is a diacritics
        #~ pat = u" ".join(pattern)
        #~ sug = u" ".join(suggestion)
        pattern = fields["pattern"]
        suggestions =fields["suggestions"]
        words   = fields["words"]
        message = araby.strip_tashkeel(fields["message"])
        pat_nm = araby.strip_tashkeel(pattern)
        sug_nm = araby.strip_tashkeel(suggestions)
        if pat_nm == sug_nm:
            return "diacritics"
        if re.search(u"|".join([u"الضبط الصحيح", u"ضبط", u"نطق", u"ما أقرته المعجمات"]), message):
            return "diacritics"            
           
        # test if rule is foreign
        if re.search("[a-zA-Z]", message):
            return "darja"
        indices = [u"فارسي",
        u"فرنسي",
        u"إنجليزي",
        u"تركي",
        u"عامي",
        u"مترجم",
        u"ترجمة",
        u"أجنبي",
        u"دخيل",
        u"أعجمي",
        u"أعجمية",
        u"لاتيني",
        u"غير عربي",      
        ]
        if re.search(u"|".join(indices), message):
            return "darja"
        # test if rule is transitive verb
        if re.search(u"|".join(['يتعدى', 'متعدي', 'بنفسه', 'بحرف', 'تعدي', u"مفعولين"]), message):
            return "trans"
        # test if rule is verb
        if re.search(u"|".join([u"فعل",]), message):
            return "verb"
        # test if rule is expression
        if re.search(u"|".join([u"تعبير",u"ركيك", u"تعابير"]), message):
            return "expression"
        # test if rule is gender related
        if re.search(u"|".join([u"مؤنث",u"مذكر", u"إناث", u"يؤنث",u"يذكر", u"ذكور", u"تأنيث", u"تذكير"]), message):
            return "expression"

        # test if rule is gender related
        if re.search(u"|".join([u"لم يرد",u"لا يوجد", u"لم تسمع", u"كلام العرب",u"لغة العرب", u"ذكور", u"تأنيث", u"تذكير"]), message):
            return "expr"
                        
        # if is just one word
        tokens = araby.tokenize(fields["words"])
        tokens_pattern = araby.tokenize(pattern)
        if len(tokens) == 1 and len(tokens_pattern) == 1:
            return "oneword"
        return ""


    def is_already_done(self, pattern, words ="", wrong_example=""):
        """
        check if the pattern is already treated in our project
        pattern : list of token
        """
        # if pattern exists in dones
        pat = araby.strip_tashkeel(pattern)
        wrd = words
        if wrd: 
            wrd = araby.strip_tashkeel(wrd)
        wrong_example = araby.strip_tashkeel(wrong_example)
        if pat in self.dones or wrd in self.dones:
            return "done"
        for d in self.dones:
            if d in wrd:
                return "done-word"
            if d in pat:
                return "done-pattern"
            if d in wrong_example:
                return "done-example"                
        return ""      

    def wrap_diff_line(self, rule):
        """
        extract information from a rule example tuple
        """
        result = self.diff_line(rule)
        #~ print(result)
        #prepare results
        result["patterns"] = self.join_list_list(result.get("patterns", []))
        #~ result["patterns"]  = araby.strip_tashkeel(result["patterns"])
        result["suggestions"] = self.join_list_list(result.get("suggestions", []))
        result["context"] = u" ".join(result.get("context", []))
        # add guessed category if no category found
        #~ result["category"] = u";".join(result.get("categories", []))
        # join positions
        result["marker_pos"] = self.join_list_list_int(result.get("marker_pos", []),'-')
        return result

    @staticmethod
    def diff_line(rule):
        """
        extract information from a rule example tuple
        """
        # a line contains a correct and incorrect exqmple
        marker_begin ="<marker>"
        marker_end ="</marker>"
        debug = False
        a,b = rule
        a = araby.tokenize(a)
        b = araby.tokenize(b)
        s = difflib.SequenceMatcher(None, a, b)
        if debug:
            for block in s.get_matching_blocks():
                print(block)
        # extract patterns
        patterns = []
        # extract suggestions
        suggestions = []
        wrong_example = []
        marker_pos = []
        correct_example = []
        categories = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if debug:
                print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(
                tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))            
            if tag == "equal":
                wrong_example.extend(a[i1:i2])
            elif tag in ("delete", "insert", "replace"):
                wrong_example.append(marker_begin)
                wrong_example.extend(a[i1:i2])
                wrong_example.append(marker_end)            
                suggestions.append(b[j1:j2])
                patterns.append(a[i1:i2])
                marker_pos.append((i1,i2))
                #~ cat = self.guess_category(a[i1:i2], b[j1:j2])
                #~ if cat :
                    #~ categories.append(cat)
            else:
                wrong_example.extend(a[i1:i2])
        result={"patterns": patterns,
            "suggestions": suggestions,
            "example_wrong": wrong_example,
            "context": a,
            "marker_pos":marker_pos,
            "example_correct": b,
            #~ "categories": list(set(categories)),
            }
        return result
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
