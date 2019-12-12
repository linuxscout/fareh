#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rule_converter.py
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
        
class rule_converter:
    """ a virtual converter of data from table to specific format
    the data is big, then every function print string """
    def __init__(self, category, version="N/A"):
        """
        initiate the dict
        """

        self.id = 0
        self.version = version
        self.field_id={
            'id':0,          #   رقم
            'rule_id':1,     #    رقم القاعدة
            'status':2,      # الحالة
            'category':3,    # صنف الخطأ
            'pattern':4,     # النمط
            'suggestions':5,   #المستبدل
            
            'note':6,        #  الملاحظة
            'wrong_example':7,     #مثال خطأ
            'correct_example':8,        # مثال صحيح
        }
        #give the display order for text format display
        self.display_order=[
            'id',          #   رقم
            'rule_id',     #    رقم القاعدة
            'status',      # الحالة
            'category',    # صنف الخطأ
            'pattern',     # النمط
            'suggestions',   #المستبدل
            
            'note',        #  الملاحظة
            'wrong_example',     #مثال خطأ
            'correct_example',        # مثال صحيح
             ]
        self.boolean_fields=[
                ]                
        category_table={
            "oneword":u"كلمة واحدة",
            "indirect-transitive":u"متعدي بحرف",
            "expression":u"تعبير",
            "jar":u"حرف جر",    
            "verb":u"فعل",
            "adjective":u"صفة",
            "all":u"كل",
        }
        counter_table={
            "oneword":0,
            "indirect-transitive":1000,
            "expression":2000,
            "jar":3000,    
            "verb":4000,
            "adjective":5000,
            "all":6000,
            "":10000,
        }
        self.id = counter_table.get(category, 1);
        self.category = category_table.get(category, "all");

        if not category: 
            print "Fatal Error : unsupported category", category;
            exit();
        #generic Header for project
        self.headerlines = [
        "*************************************",
        " Fareh, Our beautiful language, grammers errors rules",
                    "Noun dictionary file",
                    "Wordtype       : %s"%self.category,                    
                    "Version        : %s"%self.version,
                    "Generated at   : %s"%time.strftime("%Y/%m/%d:%H:%M"),                    
                    "Author         : Taha Zerrouki", 
                    "Source           : http://github.com/linuxscout/fareh",                    
                    "*************************************",
                    ]
    def add_header(self,):
        """
        add the header for new dict
        """
        line = "#" + "\n#".join(self.headerlines) + "\n"
        line +=  "#" + u"\t".join(self.display_order)
        return line
         
    def add_record(self, noun_row):
        """
        Add a new to the dict
        """
        self.id += 1
        fields = self.treat_tuple(noun_row) 
        items=[];
        for k in range(len(self.display_order)):
            key = self.display_order[k];
            # some fields are integer, than we use str
            items.append(unicode(fields[key]))
        line = u"\t".join(items);
        return line
        
    def add_footer(self):
        """close the data set, used for ending xml, or sql"""
        return ""
        
    def __str__(self,):
        """ return string to  """
        pass;

    def treat_tuple(self,tuple_noun):
        """ convert row data to specific fields
        return a dict of fields"""
        #~ self.id+=1;
        #extract field from the noun tuple
        fields={};
        for key in self.field_id.keys():
            try:
                fields[key] = tuple_noun[self.field_id[key]].strip();
            except IndexError:
                print "#"*5, "key error [%s],"%key, self.field_id[key], len(tuple_noun);
                print tuple_noun
                sys.exit()
        # change boolean fields
        for key in self.boolean_fields:
            if not fields[key]: 
                fields[key] = False
            elif fields[key] in ('n',"N", "Non"):
                fields[key] = "no"
            elif fields[key] in ('o',"O"):
                fields[key] = "yes"              
            else:
                fields[key] = 1        
        return fields;


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
