#!/usr/bin/env python

import urllib, urllib2
import requests
import argparse
from bs4 import BeautifulSoup

def get_soup(searchword):
    base = "https://www.google.com/search"
    params = { 'q' : 'define:%s' % searchword }
    headers = { 'User-Agent' : 'Firefox 18.3' }
    req = requests.get(base, params=params, headers=headers)
    soup = BeautifulSoup(req.text)
    return soup

class definition():
    def __init__(self, soup):
        try: rawchunk = soup.find('div', id='ires')
        except: pass

        if rawchunk:
            try: self.syllabic = rawchunk.find('span', attrs={'data-dobid':'hdw'}).text
            except: self.syllabic = ""

            try: self.phonetic = rawchunk.find('span', class_='lr_dct_ph').text
            except: self.phonetic = ""

            try: self.forms    = rawchunk.find('div', class_='xpdxpnd vk_gy').text
            except: pass

            try: self.fulldefs = [ i.text for i in rawchunk.find_all('div', attrs={'data-dobid':'dfn'}) ]
            except: pass

            try: self.sentence = rawchunk.find('div', class_="lr_dct_more_blk xpdxpnd xpdnoxpnd vk_gy").text
            except: pass

            try: thesrus       = rawchunk.find_all('table', class_='vk_tbl vk_gy')
            except: pass

            try: self.synolist = [ i.text for i in thesrus[0].find_all('a')]
            except: pass

            try: self.antolist = [ i.text for i in thesrus[1].find_all('a')]
            except: pass

    def __repr__(self):
        return __name__

def main():
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

    parser = argparse.ArgumentParser()
    parser.add_argument("search", nargs='+', help="type the word you want to search here")
    args = parser.parse_args()
    searchword = " ".join(args.search)
    defi = definition(get_soup(searchword))
    if defi.syllabic:
        head = "%s . %s . %s" % (searchword, defi.syllabic, defi.phonetic)
        print bcolors.HEADER + head + bcolors.ENDC
        print bcolors.OKGREEN + " - " + "\n - ".join(defi.fulldefs) + bcolors.ENDC
        if hasattr(defi, "forms"):
            print "\n" + bcolors.HEADER + "forms:" + bcolors.ENDC
            print bcolors.OKGREEN + " - " + "\n - ".join(defi.forms.split(';')) + bcolors.ENDC
        if hasattr(defi, "sentence"):
            print "\n" + bcolors.HEADER + "usage:" + bcolors.ENDC
            print bcolors.OKGREEN + " " + defi.sentence + bcolors.ENDC
        if hasattr(defi, "synolist"):
            print "\n" + bcolors.HEADER + "synonyms:" + bcolors.ENDC
            print bcolors.OKGREEN + " " + ", ".join(defi.synolist) + bcolors.ENDC
        if hasattr(defi, "antolist"):
            print "\n" + bcolors.HEADER + "antonyms:" + bcolors.ENDC
            print bcolors.OKGREEN + " " + ", ".join(defi.antolist) + bcolors.ENDC


if __name__ == "__main__":
    main()

