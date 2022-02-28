# Fareh فارح

<div dir=rtl>
القواعد العربية للتدقيق النحوي والأسلوبي
</div>
Arabic rules database for grammar and style checking

## Description
Fareh is a database of rules applied to check grammar and languaage checking, it contains list of common errors patterns.

It will be used especially for LanguageTool grammar and style checker.[LanguageTool grammar and style checker.](http://languagetool.org) 

#### Developpers: 
 Taha Zerrouki: http://tahadz.com
    taha dot zerrouki at gmail dot com

Sohaib Afifi: http://sohaibafifi.com

Features |   value
------------|---------------------------------------------------------------------------
Authors   | [Authors.md](https://github.com/linuxscout/fareh/master/AUTHORS.md)
Release  | 0.1 
License  |[GPL](https://github.com/linuxscout/fareh/master/LICENSE)
Tracker  |[linuxscout/Fareh/Issues](https://github.com/linuxscout/fareh/issues)




## Citation
If you would cite it in academic work, can you use this citation
```
T. Zerrouki‏, S. Afifi, Fareh: Arabic rules database for grammar and style checking,  https://github.com/linuxscout/fareh/, 2019
```
or in bibtex format
```bibtex
@misc{zerrouki2019Fareh,
  title={Fareh, Arabic mophological generator Library for python.},
  author={Zerrouki, Taha and Afifi Sohaib},
  url={https://github.com/linuxscout/fareh},
  year={2019}
}
```
## Applications
* Grammar checking
* Common error checking

## Features  مزايا
<div dir=rtl>

- تسهيل بناء قواعد بصيغة xml لإثراء برنامج أداة اللغة
- صيغة مقروءة برمجيا
- متابعة التقدم في بناء القواعد

</div>
- Facilitate build rules in xml format for LanguageTool grammar checker.
- Machine readable format
- Advancement tracking in rules building

 


### Requirements
 - PyArabic: Arabic language tools library   : http://pypi.pyton/pyarabic




## أصل التسمية

<div dir=rtl>
سمي هذا البرنامج نسبة إلى الشيخ محمد فارح الجزائري، أستاذ صحفي لغوي أشتهر بعمله في التدقيق اللغوي وإعداده برنامجا إذاعيا "لغتنا الجميلة" في الإذاعة الجزائرية.

[المزيد عن الشيخ محمد فارح](doc/mohamed_fareh.md) 
</div>

Usage
=====
1- Edit  rules file
Rules file  is edited in data directory as open document format.

2- Build candidate rules in xml format:

```sh
make test
```


### Files

* file/directory    category    description 

* data/	A list of rules files

* data/done	A list of rules files already treated, it an be reviewed to fix some errors, or to avoid duplicated rules

* data/original    original source files saved as archive

* data/ArabicCommunErrors0.2.ods to add new rules as fields, or an other files with similar format

  



