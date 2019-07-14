#!/usr/bin/env python3
## BLOCKLIST FETCHER
import os
import sys

lists = []
config = {
    "Ads": ["spotify"],
    "Downloads": [
        "appstore", 
        "updates.vsc", 
        "updates.windows"
    ],
    "Drugs": ["vaping"],
    "MDM": [
        "jamf", 
        "lightspeed"
    ],
    "Malicious": ["apple"],
    "Phishing": ["deals"],
    "Porn": ["porn"],
    "Proxy": [
        "1.1.1.1", 
        "lightspeed"
    ],
    "Scanners": ["scanners"],
    "Social": [
        "discord",
        "facebook",
        "groupme",
        "houseparty",
        "instagram",
        "reddit",
        "skype",
        "snapchat",
        "tiktok",
        "twitter"
    ]
}

class fetcher(object):
    def remove_prefix(self, text, prefix):
        return text[text.startswith(prefix) and len(prefix):]

    def getBaseRawURL(self, repoURL):
        return "https://raw.githubusercontent.com/{}/master/".format(self.remove_prefix(self.repoURL, "https://github.com/"))

    def __init__(self, repoURL):
        self.repoURL = repoURL
        self.baseRawURL = self.getBaseRawURL(self.repoURL)

def main():
    # Instanciate the class
    fetcherObj = fetcher("https://github.com/jaykepeters/Blocklists")

    for category in config:
        for list in config[category]:
            listURL = "{}{}/{}.txt".format(fetcherObj.baseRawURL, category, list)
            print(listURL)

    def interactive():
        print("Enter your desired lists in the format Category/list")
        print("When you are done, on the very last line, enter \".\"")
        while True:
            lists.append(input("List: "))
            if "." in lists[-1]:
                lists.pop(-1)
                done = True
                break

        while True:
            if done == True:
                print(lists)
                for item in lists:
                    # Remove non-conforming lists
                    if "/" not in item:
                        print("Nonconforming list: " + list[item])
                        lists.remove(index(item))

                    # Convert everything to lowercase
                    newitem = item.lower()

                    # Split the list into it's counterparts
                    parts = newitem.strip("/")

                    # Store the counterparts
                    category = parts[0]
                    _list = parts [1]
                    
                    # Capitalize the first letter
                    category = category[0].upper()

                    # Re-combine list
                    lists[index(item)] = "{}/{}".format(category, _list)
                break

    ## SUDO CHECK 
    def sudoCheck():
        if os.geteuid() != 0:
            exit("You must run this script with sudo!")
        else:
            try:
                if sys.argv[1] == "--interactive":
                    interactive()
            except:
                pass
    sudoCheck()

if __name__ == "__main__": 
    main()
