#/usr/bin/sh
# Build Arramooz dictionary files
DATA_DIR :=data
DATA_DIR_OUT :=tests/data
RELEASES :=releases
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.1
DOC="."
#~ RULES_CANDIDATES=ArabicCommunErrors0.2.csv
RULES_CANDIDATES=Obikab-classified-0.1.csv
LIBREOFFICE=libreoffice6.3
OBIKAN_DICT=3bykan.csv

CATEGORY=all
default: all
# Clean build files
clean:
	rm -f -r $(RELEASES)/* $(OUTPUT)
backup: 
	mkdir -p $(RELEASES)/backup$(VERSION)
	touch $(RELEASES)/todo.bz2
	mv $(RELEASES)/*.bz2 $(RELEASES)/backup$(VERSION)
#create all files 
all: ods convert

# Publish to github
publish:
	git push origin master 

ods:
	$(LIBREOFFICE) --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(DATA_DIR_OUT)/ $(DATA_DIR)/*.ods

oneword:CATEGORY=oneword
spell:CATEGORY=spell
gender:CATEGORY=gender
jar:CATEGORY=jar
adj:CATEGORY=adjective
expression:CATEGORY=expression
verb:CATEGORY=verb
trans:CATEGORY=indirect-transitive
double:CATEGORY=double-transitive

misc:CATEGORY=misc
convert test oneword spell gender expression jar adj verb trans double misc:ods
	python3 $(SCRIPT)/grammar_csv2xml.py -d xml -t $(CATEGORY) -v $(VERSION) -f $(DATA_DIR_OUT)/$(RULES_CANDIDATES) > $(OUTPUT)/rules.tmp.xml
	xmllint --format  $(OUTPUT)/rules.tmp.xml  --output $(OUTPUT)/rules-candidates.xml

ods_obikan:
	$(LIBREOFFICE) --headless --convert-to "csv:Text - txt - csv (StarCalc):9,34,UTF8" --outdir $(DATA_DIR_OUT)/ $(DATA_DIR)/*.ods

#~ obikan:ods_obikan
obikan:
#~ 	python3 $(SCRIPT)/prepare_3obikan.py -l 200 -f $(DATA_DIR_OUT)/$(OBIKAN_DICT) > $(OUTPUT)/obican_dict.csv
	python3 $(SCRIPT)/prepare_3obikan.py -f $(DATA_DIR_OUT)/$(OBIKAN_DICT) -d $(DATA_DIR_OUT)/done.txt > $(OUTPUT)/obican_dict.csv
	cut -f4 $(OUTPUT)/obican_dict.csv |sort  | uniq -c
	cut -f2 $(OUTPUT)/obican_dict.csv |sort | uniq -c
done:
	cut -f1 -d= $(DATA_DIR)/done/*.txt |grep -v "^#" |sed '/^$$/d'  > /tmp/done.txt
	grep "done" $(DATA_DIR_OUT)/$(RULES_CANDIDATES)|cut -f6 >> /tmp/done.txt
	strip_tashkeel.sh /tmp/done.txt  > /tmp/done.un.txt
	sort -u /tmp/done.un.txt > $(DATA_DIR_OUT)/done.txt
messages:
	# extract keywords from messages to detect errors categories
	strip_tashkeel.sh  tests/data/notes.txt  > /tmp/notes.txt
	tokenize_uniq.sh  /tmp/notes.txt  | head -n 1000 > tests/data/keywords.txt

diac:CATEGORY=diac
replace:CATEGORY=diac
word:CATEGORY=word
darja:CATEGORY=darja
added:CATEGORY=added
homophone:CATEGORY=homophone
exp2:CATEGORY=expression
replace diac word darja added exp2 homophone:ods
	python3 $(SCRIPT)/grammar_csv2xml.py -t $(CATEGORY) -d replace -v $(VERSION) -f $(DATA_DIR_OUT)/$(RULES_CANDIDATES) > $(OUTPUT)/replaces.debug.txt
	grep -v "^$$" $(OUTPUT)/replaces.debug.txt | grep -v "#" > $(OUTPUT)/replaces.candidates.txt
	cp $(OUTPUT)/replaces.debug.txt  $(OUTPUT)/replaces.$(CATEGORY).debug.txt
	cp $(OUTPUT)/replaces.candidates.txt $(OUTPUT)/replaces.$(CATEGORY).txt
