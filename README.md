#Fareh فارح

القواعد العربية للتدقيق النحوي والأسلوبي
Arabic rules database for grammar and style checking

## Description
Fareh is a database of rules applied to check grammar and languaage checking, it contains list of common errors patterns.
It will be used especially for LanguageTool grammar and style checker.[LanguageTool grammar and style checker.](http://languagetool.org) 

#### Developpers: 
 Taha Zerrouki: http://tahadz.com
    taha dot zerrouki at gmail dot com

Sohaib Afifi: http://sohaibafifi.com
Features |   value

-
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/linuxscout/fareh/master/AUTHORS.md)
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
* common error checking

## Features  مزايا
- تسهيل بناء قواعد بصيغة xml لإثراء برنامج أداة اللغة
- صيغة مقروءة برمجيا
- متابعة التقدم في بناء القواعد
- Facilitate build rules in xml format for LanguageTool grammar checker.
- Machine readable format
- Advancement tracking in rules building

 


### Requirements
``` 

```
 - PyArabic: Arabic language tools library   : http://pypi.pyton/pyarabic



## أصل التسمية
سمي هذا البرنامج نسبة إلى الشيخ محمد فارح الجزائري، أستاذ صحفي لغوي أشتهر بعمله في التدقيق اللغوي وإعداده برنامجا إذاعيا "لغتنا الجميلة" في الإذاعة الجزائرية.

[المزيد عن الشيخ محمد فارح ](https://ar.wikipedia.org/wiki/%D9%85%D8%AD%D9%85%D8%AF_%D9%81%D8%A7%D8%B1%D8%AD_(%D8%AC%D8%B2%D8%A7%D8%A6%D8%B1%D9%8A))
  
Usage
=====
1- Edit  rules file
rules file  is edited in data directory as open document format.

2- Build candidate rules in xml format:

```sh
make test
```


### Files

* file/directory    category    description 

data/	A list of rules files




