#!/usr/bin/env python3
## BLOCKLIST FETCHER
import os
import optparse
import sys
import urllib.request, json
from pathlib import Path
import re

unformattedBlocklists = []
blocklists = []
regex = []

class Fetcher(object):
    def remove_prefix(self, text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    def getBaseRawURL(self, repoURL):
        return "https://raw.githubusercontent.com/{}/master/".format(self.remove_prefix(self.repoURL, "https://github.com/"))

    def getListsData(self, baseRawURL):
        url =  "{}lists.json".format(baseRawURL)
        data = urllib.request.urlopen(url).read()
        listsJSON = json.loads(data)
        return(listsJSON)

    def getBlocklistsFromFile(self, filepath):
        if os.path.exists(filepath):
            Blocklists = [line.rstrip('\n') for line in open(filepath)]
            return Blocklists
        else:
            return False

    def validateBlocklists(self, bl):
        formattedBlocklists = []
        for blocklist in bl:
            theBL = blocklist

            # Format specification, will have at least 1 slash
            if "/" not in blocklist:
                print("ERROR\t Nonconforming blocklist:: " + blocklist)
            elif len(theBL.split("/")) != 2:
                print("ERROR\t Nonconforming blocklist:: " + blocklist)
            else:
                # Convert everything to lowercase
                theBL = theBL.lower()

                # Capitalize the first letter
                theBL = list(theBL)
                theBL[0] = theBL[0].upper()
                theBL = ''.join(theBL)

                # Remove .txt extention
                if ".txt" in theBL:
                    theBL = os.path.splitext(theBL)[0]

                # Check if valid
                category, _list = theBL.split("/")
                try:
                    if _list in self.listsData[category]:
                        formattedBlocklists.append(theBL)
                        print("STATUS\t Blocklist Found:: " + theBL)
                    else:
                        print("ERROR\t Invalid Blocklist:: " + blocklist)
                except KeyError:
                    print("ERROR\t Invalid Category:: " + category)

        return formattedBlocklists

    def genWildcardRegex(self, wildcard):
        base = "(^|\.){}$"
        parts = wildcard.strip("*.").split(".")
        if len(parts[0]) > 1:
            regex = base.format("\.".join(parts))
            return regex
        else:
            print("ERROR\t Malformed Wildcard Domain:: " + wildcard)
            return

    def getWildcardsFromFile(self, file):
        wildcards = []
        lines = [line.rstrip('\n') for line in open(file)]
        for line in lines:
            # Ignore comments
            if "#" not in line:
                if re.match("^\*", line):
                    regex = self.genWildcardRegex(line)
                    if regex:
                        wildcards.append(regex)
        return wildcards

    def appendFile(self, file, lines):
        TBprefix = "## FETCHER ##\n"
        with open(file, 'w') as filehandle:  
            filehandle.writelines(TBprefix)
            filehandle.writelines("%s\n" % line for line in lines)
            filehandle.writelines(TBprefix)

    def addLists(self, bl):
        # Make Directories
        if not os.path.exists(self.tempdir):
            print("STATUS:\t Making Temporary Directory")
            os.makedirs(self.tempdir)

        # Download Blocklists
        print("STATUS\t Downloading Blocklists for Review")
        dcount = 0
        for blocklist in bl:
            category, _list = blocklist.split("/")
            listURL = "{}{}.txt".format(self.baseRawURL, blocklist)
            parentDir = "{}{}".format(self.tempdir, category)
            filePath = "{}/{}.txt".format(parentDir, _list)

            # Make Download Directories
            if not os.path.exists(parentDir):
                os.mkdir(parentDir)

            # User message
            dcount += 1
            print("STATUS\t Downloading File {} of {}:: {}".format(dcount, len(bl), blocklist))
            urllib.request.urlretrieve(listURL, filePath)  
        
        print("STATUS\t Finding Wildcard Regexps")
        for blocklist in bl:
            category, _list = blocklist.split("/")
            parentDir = "{}{}".format(self.tempdir, category)
            filePath = "{}/{}.txt".format(parentDir, _list)

            wildcards = self.getWildcardsFromFile(filePath)
            if wildcards:
                regex.extend(wildcards)
        if regex:
            print("STATUS\t Number of regexp's found: {}".format(len(regex)))
            print("STATUS\t Adding regexps's to /etc/pihole/regex.list")
            self.appendFile("/etc/pihole/regex.list", regex)
        else:
            print("STATUS\t No rexp's found :(")

    def __init__(self, repoURL):
        self.repoURL = repoURL
        self.baseRawURL = self.getBaseRawURL(self.repoURL)
        self.listsData = self.getListsData(self.baseRawURL)
        self.cluserHome = str(Path.home())
        self.tempdir = "/tmp/blocklists/"
    
def main():
    ## SUDO CHECK 
    def sudoCheck():
        if os.geteuid() != 0:
            exit("You must run this script with sudo!")
    sudoCheck()

    # Instanciate the class
    fetcher = Fetcher("https://github.com/jaykepeters/Blocklists")

    ## COMMAND LINE STUFF
    parser = optparse.OptionParser()
    parser.set_usage(
        """usage: %prog [--file file | -f file ] [--list "Category/listname | -l "Category/listname"]
        Copyright 2019 Jayke Peters""")

    ## OPTIONS
    parser.add_option('--list', '-l',
        action="append",
        help="Specifies a list to be used with Pi-hole")

    parser.add_option('--file', '-f',
        action="store",
        help="Specifies a file to use containing lists to be used with Pi-hole")

    options, _ = parser.parse_args()

    if options.file and options.list:
        print("ERROR\t You can only specify a file OR a list(s)")
        exit(1)
    elif options.file:
        unformattedBlocklists = fetcher.getBlocklistsFromFile(options.file)
        if not unformattedBlocklists:
            print("ERROR\t Invalid File Format")
        pass
    elif options.list:
        unformattedBlocklists = options.list
        pass
    else:
        print("STATUS\t Looking for \"blocklists.txt\" in your home directory")
        unformattedBlocklists = fetcher.getBlocklistsFromFile(fetcher.cluserHome + "/blocklists.txt")
        if not unformattedBlocklists:
            print("ERROR\t Nonexistent file:: ~/blocklists.txt")
            exit(1)
        else:
            print("STATUS\t File Found:: blocklists.txt")

    ## Now do necessary things with the data
    # Ensure proper format for blocklists and remove bad ones
    blocklists = fetcher.validateBlocklists(unformattedBlocklists)
    
    # Add Lists
    fetcher.addLists(blocklists)  

if __name__ == "__main__": 
    main()
