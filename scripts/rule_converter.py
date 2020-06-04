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
import sys
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
# * example_marker_pos موضع الاستبدال في المثال
# * marker_pos موضع الاستبدال في النمط
# * inflected تصريف 
# * regexp   تعبير منتظم
# * postag  وسم أقسام الكلم

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
            'id':0,  ##الرقم الأصلي
            'rule_id':1,  #رقم القاعدة
            'status':2,  #الحالة
            'unvocalized':3,  #غير مشكول للبحث
            'category':4,  #صنف الخطأ
            'context':5,  #السياق
            'pattern':6,  #الخطأ
            'suggestions':7,  #التصحيح
            'note':8,  #ملاحظة1
            'wrong_example':9,  #مثال خاطئ
            'correct_example':10,  #مثال صحيح
            'example_marker_pos':11, # موضع الاستبدال في المثال
            'marker_pos':12, # موضع الاستبدال في النمط
            'inflected':13, # تصريف 
            'regexp':14,#   تعبير منتظم
            'postag':15, #  وسم أقسام الكلم
            'skip':16, # تخطي كلمة

        }
        #give the display order for text format display
        self.display_order=[
            'id',  ##الرقم الأصلي
            'rule_id',  #رقم القاعدة
            'status',  #الحالة
            'unvocalized',  #غير مشكول للبحث
            'category',  #صنف الخطأ
            'context',  #السياق
            'pattern',  #الخطأ
            'suggestions',  #التصحيح
            'note',  #ملاحظة1
            'wrong_example',  #مثال خاطئ
            'correct_example',  #مثال صحيح
            'example_marker_pos', # موضع الاستبدال في المثال
            'marker_pos', # موضع الاستبدال في النمط
            'inflected', # تصريف 
            'regexp',#   تعبير منتظم
            'postag', #  وسم أقسام الكلم
            'skip', # تخطي كلمة
             ]
        self.boolean_fields=[
                ]                
        category_table={
            "oneword":u"كلمة واحدة",
            "indirect-transitive":u"متعدي بحرف",
            "double-transitive":u"متعدي إلى مفعولين",            
            "expression":u"تعبير",
            "jar":u"حرف جر",    
            "verb":u"فعل",
            "gender":u"نوع",
            "adjective":u"صفة",
            "spell":u"خطأ إملائي",
            "misc":u"منوع",
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
            "misc":8000,
            "":10000,
        }
        self.id = counter_table.get(category, 1);
        self.category = category_table.get(category, "all");
        self.category_english = category

        if not category: 
            print("Fatal Error : unsupported category", category)
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
        # add only given category
        if self.category != "all" and fields.get("category","") != self.category:
            return ""
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
                print("#"*5, "key error [%s],"%key, self.field_id[key], len(tuple_noun))
                print(list(enumerate(tuple_noun)))
                print("key error", key)
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
