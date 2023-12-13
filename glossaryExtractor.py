import re

def extractGlossaryFromEganFundementalRTC():
    bookGlossary = open("Resources/eganGlossary").read()

    bookGlossary = bookGlossary.replace(" \n", "  ")
    bookGlossary = bookGlossary.replace("  \n", " ")
    bookGlossary = bookGlossary.replace("-\n", "")
    bookGlossary = bookGlossary.replace("- \n", "-")
    bookGlossary = bookGlossary.replace("\n", " ")

    pattern = re.compile(r'Chapter [0-9]{1,2}\)\s(.*?)\s\s')

    for matched in re.finditer(pattern, bookGlossary):
        print re.sub(r'( \(.*\))|([A-Z] )|([0-9]{4} )', '', matched.group(1))


def extractGlossaryFromCSDavis():
    bookGlossary = open("Resources/CSDavis").read()

    pattern = re.compile(r'\n([A-Z].*?):')
    for matched in re.finditer(pattern, bookGlossary):
        print re.sub(r' ([0-9])', r'\1', re.sub(r'( \(.*\))', '', matched.group(1)).lower())


#extractGlossaryFromEganFundementalRTC()
extractGlossaryFromCSDavis()