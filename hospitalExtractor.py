"""
This code extracts the name of Hospitals and their address from http://www.medilexicon.com/hospitals
"""
import urllib
import re

def extractHospitalNames():

    for index in range(1, 23):
        query = "http://www.medilexicon.com/hospitals&country_select=Canada&search_by_select=hospital&page=" + str(index)
        searchResults = urllib.urlopen(query).read().replace('\n', '')

        pattern = re.compile(r'item_text.+?href=.+?hospitals.+?>(.+?)</a></h3>.+?<p>(.+?)</p>')

        for matched in re.finditer(pattern, searchResults):
            print matched.group(1) + "@" + matched.group(2).strip()

extractHospitalNames()