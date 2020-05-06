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


import rule_builder
import rule_converter
import builder_const
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
        
class rule_converter_xml(rule_converter.rule_converter):
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, category, version="N/A"):
        """
        initiate the dict
        """
        rule_converter.rule_converter.__init__(self, category, version)        
        self.builder = rule_builder.rule_builder()
        
    def add_header(self,):
        """
        add the header for new dict
        """
        line = """<?xml version="1.0" encoding="UTF-8"?>"""
        line += "<!--" + "\n#".join(self.headerlines) + "-->\n"
        line +=  "<!--" + u"\t".join(self.display_order) + "-->\n"
        line += builder_const.DOCTYPE
        line += u"""<rules>"""
        return line

    def add_footer(self,):
        """
        add the footer for new dict
        """
        line = """</rules>"""
        return line
         
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(noun_row)
        
        status =fields.get("status", False)
        if status == "done":
            return ""        
        # add only given category
        if self.category != "all" and fields.get("category","") != self.category:
            return ""
        

        rb = self.builder
        rb.reset()
        name = araby.strip_tashkeel(fields['context'])
        rb.set_category(fields.get("category",""))
        #~ rb.set_category_english(self.category_english)
        ruleid = fields["rule_id"]
        if not ruleid:
            ruleid =  self.category_english+"_%04d"%(self.id)

        rb.add_rulename(ruleid, name)
        rb.add_context(fields["context"])
        rb.add_message(fields['note'])
        rb.add_pattern(fields["pattern"], mark_pos = fields["marker_pos"], inflected=fields["inflected"],  regexp=fields["regexp"], postag=fields["postag"], skip= fields["skip"])
        rb.add_suggestions(fields['suggestions'])
        rb.add_example(fields['wrong_example'], correction=fields['suggestions'], mark_pos = fields["example_marker_pos"], correct=False)
        rb.add_example(fields['correct_example'],correct=True)
        rule =rb.build()
        return rule

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
