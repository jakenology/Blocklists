#!/usr/bin/env python3
## BLOCKLIST FETCHER
"""
TO DO
- Config file, if not existing, back up old from calls, etc...
"""
import os
import optparse
import sys
import urllib.request, json
from pathlib import Path
import re
import subprocess

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
        response = urllib.request.urlopen(url)
        str_response = response.read().decode('utf-8')
        listsJSON = json.loads(str_response)
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

    def editConfig(self, file, content=[], delete=False):
        fileContent = [line.rstrip('\n') for line in open(file)]

        fileContentToWrite = []
        newln = "\n"

        index = 0
        cindexes = []
        for line in fileContent:
            index += 1
            if self.TBprefix in line:
                cindexes.append(index)
        
        # The file has never been written to before by fetcher
        if not cindexes:
            with open(file, 'a') as outfile:
                if fileContentToWrite:
                    if fileContentToWrite[-1] != '':
                        self.tprefix = newln + self.TBprefix + newln
                elif fileContent:
                    if fileContent[-1] != '':
                        self.tprefix = newln + self.TBprefix + newln
                outfile.writelines(self.tprefix)
                outfile.writelines("%s\n" % line for line in content)
                outfile.writelines(self.TBprefix)
        
        # There is content in between the prefixes, let's modify and write the file accordingly
        elif cindexes and not delete:
            ltr = fileContent[cindexes[0]-1:cindexes[1]]
            if ltr[1:-1] == content:
                print("STATUS\t There is no content to update or remove")
            else:
                linesToRemove = set(ltr)
                fileContentToWrite = [x for x in fileContent if x not in linesToRemove]
                with open(file, 'w') as outfile:
                    outfile.writelines("%s\n" % line for line in fileContentToWrite)
                    if fileContentToWrite:
                        if fileContentToWrite[-1] != '':
                            self.tprefix = newln + self.TBprefix + newln
                    elif fileContent:
                        if fileContent[-1] != '':
                            self.tprefix = newln + self.TBprefix + newln
                    outfile.writelines(self.tprefix)
                    outfile.writelines("%s\n" % line for line in content)
                    outfile.writelines(self.TBprefix)

        # We want to remove the prefixes and everything in between from the file
        else:
            with open(file, 'w') as outfile:
                linesToRemove = set(fileContent[cindexes[0]:cindexes[1]])
                fileContentToWrite = [x for x in fileContent if x not in linesToRemove]
                outfile.writelines("%s\n" % line for line in fileContentToWrite)
        
    def addLists(self, bl):
        blURLS = []

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

            # Add the url to the list of blocklists
            blURLS.append(listURL)

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
            
            # Add regexes
            print("STATUS\t Adding regexps's to /etc/pihole/regex.list")
            self.editConfig("/etc/pihole/regex.list", regex)
        else:
            print("STATUS\t No rexp's found :(")

        # Add blocklists
        print("STATUS\t Adding blocklists to Pi-hole")
        self.editConfig("/etc/pihole/adlists.list", blURLS)

        # Update Gravity
        print("STATUS\t Telling Pi-hole to uptade gravity and load new regexp's")
        subprocess.run(["pihole", "-g"], stdout=subprocess.PIPE)

    def __init__(self, repoURL):
        self.repoURL = repoURL
        self.baseRawURL = self.getBaseRawURL(self.repoURL)
        self.listsData = self.getListsData(self.baseRawURL)
        self.cluserHome = str(Path.home())
        self.tempdir = "/tmp/blocklists/"
        self.TBprefix = "## FETCHER – DO NOT MODIFY ##"
        self.tprefix = self.TBprefix + "\n"
    
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
    #elif options.delete:
        #self.appendFile("/etc/pihole/regex.list", '', delete=True)
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
