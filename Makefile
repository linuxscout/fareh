#/usr/bin/sh
# Build Arramooz dictionary files
DATA_DIR :=data
DATA_DIR_OUT :=tests/data
RELEASES :=releases
OUTPUT :=tests/output
SCRIPT :=scripts
VERSION=0.1
DOC="."
RULES_CANDIDATES=ArabicCommunErrors0.2.csv
LIBREOFFICE=libreoffice6.4
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
misc:CATEGORY=misc
convert test oneword spell gender expression jar adj verb misc:ods
	python3 $(SCRIPT)/grammar_csv2xml.py -t $(CATEGORY) -v $(VERSION) -f $(DATA_DIR_OUT)/$(RULES_CANDIDATES) > $(OUTPUT)/rules.tmp.xml
	xmllint --format  $(OUTPUT)/rules.tmp.xml  --output $(OUTPUT)/rules-candidates.xml
