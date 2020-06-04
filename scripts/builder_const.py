#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  builder_const.py
#  
ENTITIES = {'أنك': '&forms_anna;',
 'أنكم': '&forms_anna;',
 'أنكما': '&forms_anna;',
 'أنكن': '&forms_anna;',
 'أننا': '&forms_anna;',
 'أنه': '&forms_anna;',
 'أنها': '&forms_anna;',
 'أنهم': '&forms_anna;',
 'أنهما': '&forms_anna;',
 'أنهن': '&forms_anna;',
 'أني': '&forms_anna;',
 'إلى': '&forms_ila;',
 'إلي': '&forms_ila;',
 'إليك': '&forms_ila;',
 'إليكم': '&forms_ila;',
 'إليكما': '&forms_ila;',
 'إليكن': '&forms_ila;',
 'إلينا': '&forms_ila;',
 'إليه': '&forms_ila;',
 'إليها': '&forms_ila;',
 'إليهم': '&forms_ila;',
 'إليهما': '&forms_ila;',
 'إليهن': '&forms_ila;',
 'إنك': '&forms_inna;',
 'إنكم': '&forms_inna;',
 'إنكما': '&forms_inna;',
 'إنكن': '&forms_inna;',
 'إننا': '&forms_inna;',
 'إنه': '&forms_inna;',
 'إنها': '&forms_inna;',
 'إنهم': '&forms_inna;',
 'إنهما': '&forms_inna;',
 'إنهن': '&forms_inna;',
 'إني': '&forms_inna;',
 'بك': '&forms_bih;',
 'بكم': '&forms_bih;',
 'بكما': '&forms_bih;',
 'بكن': '&forms_bih;',
 'بنا': '&forms_bih;',
 'به': '&forms_bih;',
 'بها': '&forms_bih;',
 'بهم': '&forms_bih;',
 'بهما': '&forms_bih;',
 'بهن': '&forms_bih;',
 'بي': '&forms_bih;',
 'حول': '&forms_hawla;',
 'حولك': '&forms_hawla;',
 'حولكم': '&forms_hawla;',
 'حولكما': '&forms_hawla;',
 'حولكن': '&forms_hawla;',
 'حولنا': '&forms_hawla;',
 'حوله': '&forms_hawla;',
 'حولها': '&forms_hawla;',
 'حولهم': '&forms_hawla;',
 'حولهما': '&forms_hawla;',
 'حولهن': '&forms_hawla;',
 'على': '&forms_3ala;',
 'علي': '&forms_3ala;',
 'عليك': '&forms_3ala;',
 'عليكم': '&forms_3ala;',
 'عليكما': '&forms_3ala;',
 'عليكن': '&forms_3ala;',
 'علينا': '&forms_3ala;',
 'عليه': '&forms_3ala;',
 'عليها': '&forms_3ala;',
 'عليهم': '&forms_3ala;',
 'عليهما': '&forms_3ala;',
 'عليهن': '&forms_3ala;',
 'عن': '&forms_3an;',
 'عنا': '&forms_3an;',
 'عنك': '&forms_3an;',
 'عنكم': '&forms_3an;',
 'عنكما': '&forms_3an;',
 'عنكن': '&forms_3an;',
 'عنه': '&forms_3an;',
 'عنها': '&forms_3an;',
 'عنهم': '&forms_3an;',
 'عنهما': '&forms_3an;',
 'عنهن': '&forms_3an;',
 'عني': '&forms_3an;',
 'في': '&forms_fi;',
 'فيك': '&forms_fi;',
 'فيكم': '&forms_fi;',
 'فيكما': '&forms_fi;',
 'فيكن': '&forms_fi;',
 'فينا': '&forms_fi;',
 'فيه': '&forms_fi;',
 'فيها': '&forms_fi;',
 'فيهم': '&forms_fi;',
 'فيهما': '&forms_fi;',
 'فيهن': '&forms_fi;',
 'لك': '&forms_lih;',
 'لكم': '&forms_lih;',
 'لكما': '&forms_lih;',
 'لكن': '&forms_lih;',
 'لنا': '&forms_lih;',
 'له': '&forms_lih;',
 'لها': '&forms_lih;',
 'لهم': '&forms_lih;',
 'لهما': '&forms_lih;',
 'لهن': '&forms_lih;',
 'لي': '&forms_lih;',
 'مع': '&forms_ma3a;',
 'معك': '&forms_ma3a;',
 'معكم': '&forms_ma3a;',
 'معكما': '&forms_ma3a;',
 'معكن': '&forms_ma3a;',
 'معنا': '&forms_ma3a;',
 'معه': '&forms_ma3a;',
 'معها': '&forms_ma3a;',
 'معهم': '&forms_ma3a;',
 'معهما': '&forms_ma3a;',
 'معهن': '&forms_ma3a;',
 'من': '&forms_min;',
 'منك': '&forms_min;',
 'منكم': '&forms_min;',
 'منكما': '&forms_min;',
 'منكن': '&forms_min;',
 'مننا': '&forms_min;',
 'منه': '&forms_min;',
 'منها': '&forms_min;',
 'منهم': '&forms_min;',
 'منهما': '&forms_min;',
 'منهن': '&forms_min;',
 'مني': '&forms_min;'}
 
DOCTYPE=u"""  <!DOCTYPE rules [
    <!ENTITY apostrophe "['’`´‘]">
    <!ENTITY nbsp " ">
    <!ENTITY horof_jar "في|من|إلى|على|عن|مع">
    <!ENTITY unbreak_procletics "ال">
    <!ENTITY procletics "و|ف|ال|وال|فال|ب|بال|وبال|ك|كال|وكال|فكال|ل|لل|ولل|فلل">
    <!ENTITY undef_procletics "و|ف|ب|ك|">
    <!ENTITY verb_prefixes "ي|ت|ن|أ|سي|ست|سن|سأ">
    <!ENTITY verb6_prefixes "ا|ي|ت|ن|أ|سي|ست|سن|سأ">
    <!ENTITY conj "و|ف">
    <!ENTITY encletics "ه|ها|هم|هن|ك|كما|كم|كن|ي|نا">
    <!ENTITY verb_encletics "ه|ها|هم|هن|ك|كما|كم|كن|ني|نا">
    <!ENTITY forms_3an "عن|عني|عنا|عنك|عنكما|عنكم|عنكن|عنه|عنها|عنهما|عنهم|عنهن">
    <!ENTITY forms_ila "إلى|إلي|إلينا|إليك|إليكما|إليكم|إليكن|إليه|إليها|إليهما|إليهم|إليهن">
    <!ENTITY forms_3ala "على|علي|علينا|عليك|عليكما|عليكم|عليكن|عليه|عليها|عليهما|عليهم|عليهن">
    <!ENTITY forms_fi "في|فينا|فيك|فيكما|فيكم|فيكن|فيه|فيها|فيهما|فيهم|فيهن">
    <!ENTITY forms_hawla "حول|حولنا|حولك|حولكما|حولكم|حولكن|حوله|حولها|حولهما|حولهم|حولهن">
    <!ENTITY forms_min "مني|من|مننا|منك|منكما|منكم|منكن|منه|منها|منهما|منهم|منهن">
    <!ENTITY forms_ma3a "مع|معنا|معك|معكما|معكم|معكن|معه|معها|معهما|معهم|معهن">
    <!ENTITY forms_bih "بي|بنا|بك|بكما|بكم|بكن|به|بها|بهما|بهم|بهن">
    <!ENTITY forms_lih "لي|لنا|لك|لكما|لكم|لكن|له|لها|لهما|لهم|لهن">
    <!ENTITY forms_anna "أني|أننا|أنك|أنكما|أنكم|أنكن|أنه|أنها|أنهما|أنهم|أنهن">
    <!ENTITY forms_inna "إني|إننا|إنك|إنكما|إنكم|إنكن|إنه|إنها|إنهما|إنهم|إنهن">
    <!ENTITY allah_names "الآخر|الحميد|الحفيظ|اللطيف|المحيي|الجامع|الباطن|الولي|المقسط|الغفار|الودود|الوهاب|المانع|الشكور|الحليم|المتكبر|الحسيب|الجليل|النافع|الصبور|النور|المصور|الفتاح|مالك|الحي|الغني|الحق|الواسع|الجبار|المغني|العظيم|الباقي|الوارث|الرزاق|المهيمن|الضار|المقيت|الهادي|المتعالي|الوالي|المقتدر|المعز|الأول|القادر|الصمد|السميع|المذل|الكريم|ذو|البصير|العلي|السلام|المميت|العدل|الرافع|التواب|القهار|القابض|المعيد|المبدئ|الرشيد|المؤخر|المؤمن|الجلال|الظاهر|القيوم|الخبير|الوكيل|العزيز|الرحيم|الواجد|البر|المقدم|البديع|الغفور|الرقيب|الأحد|القدوس|الباسط|الجميل|والإكرام|المجيد|الرحمن|الرؤوف|المجيب|القوي|الخالق|الواحد|المنتقم|الملك|المعطي|المحصي|الكبير|العفو|المتين|الباعث|الماجد|الخافض|الحكم|العليم|البارئ|الشهي">
    <!ENTITY wrong_feminine "ذقن|رفات">
    <!ENTITY wrong_masculine "كتف|فخذ|ساق|ريح|بئر|يمين|ضبع">
          ]>"""
