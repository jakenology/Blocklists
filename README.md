# Blocklists
Blocklists for Pi-hole

# Fetcher (In Beta State)
## Use fetcher.py to select certain lists from this repo or a forked one and add them to your Pi-hole installation
### Usage: 
```bash
fetcher.py [--list "Category/list"] [--file filename]
```
### Tips
- The format for a list is as follows:
```
Category/List Name
```
- ALWAYS use quotes, spaces could be in the category name
- Use --list a list. CAN BE SPECIFIED MULTIPLE TIMES
- Use --file to specify a file of lists to be used
  - For Example 
  ```
  Social/Snapchat
  Social/Instagram
  ```
- Any minor errors will be corrected by the program
  - For Example `SoCiAl/InStAgAaM.txt` would be corrected to `Social/instagram`
 
# CONTRIBUTION
## Contribution to this collection of blocklists is always welcome, however I recommend that you follow the guidelines below:
- The first letter of a category is always capitalized
- All list names shall be lowercase end end with the txt extension
- Subcategories may be used, only if multiple lists would fall into that category
  - The format is: Category/subcategory.listname.txt
- Wildcards may be used
  - If fetcher.py is used, they will be added as regex to Pi-hole
  - Pi-hole by default will ignore these
  - The format is `*.domain.com` OR  `*.tld`
  - If there are TLD's associated with a category, please add a corresponding "tlds.txt" file
- This README shall be updated
- lists.json shall be updated

# Ads
- [Spotify](Ads/spotify.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Ads/spotify.txt)
  
# Downloads/Updates
- [Apple App Store](Downloads/appstore.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Downloads/appstore.txt)
- [Windows Updates](Downloads/updates.windows.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Downloads/updates.windows.txt)
  
# Drugs
- [Vaping](Drugs/vaping.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Drugs/vaping.txt)
  
# Malicious
- [Apple](Malicious/apple.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Malicious/apple.txt)
  
# MDM (Mobile Device Management)
- [Jamf Now/Jamf Pro](MDM/jamf.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/MDM/jamf.txt)
- [Lightspeed Systems](MDM/lightspeed.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/MDM/lightspeed.txt)
  
# Porn
- [Blocklist](Porn/porn.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Porn/porn.txt)
- [TLDs (Top-level Domains)](Porn/tlds.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Porn/tlds.txt)
  
# Proxy
- [1.1.1.1](Proxy/1.1.1.1.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Proxy/1.1.1.1.txt)
- [Lightspeed Systems](Proxy/lightspeed.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Proxy/lightspeed.txt)
  
# Phishing
- [Deals](Phishing/deals.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Phishing/deals.txt)
  
# Scanners
- [Scanners](https://github.com/jaykepeters/Blocklists/blob/master/Scanners/scanners.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Scanners/scanners.txt)

# Search Engines
- Contains a list of commonly heard of search engines, as well as search engines that to not support enforcing a DNS SafeSearch option.
- [Non-SafeSearch](Search Engines/non-safesearch.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Search Engines/non-safesearch.txt)
  
# Social Media
- [Discord](Social/discord.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/discord.txt)
- [Facebook](Social/facebook.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/facebook.txt)
- [GroupMe](Social/groupme.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/groupme.txt)
- [Houseparty](Social/houseparty.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/houseparty.txt)
- [Instagram](Social/instagram.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/instagram.txt)
- [LinkedIn](Social/linkedin.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/linkedin.txt)
- [Reddit](Social/reddit.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/reddit.txt)
- [Skype](Social/skype.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/skype.txt)
- [Snapchat](Social/snapchat.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/snapchat.txt)
- [TikTok](Social/tiktok.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/tiktok.txt)
- [Twitter](Social/twitter.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/twitter.txt)
- [Whatsapp](Social/whatsapp.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/Social/whatsapp.txt)
  
# TV
- [Hulu](TV/hulu.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/TV/hulu.txt)
- [Sling](TV/sling.txt)
  - [Raw](https://raw.githubusercontent.com/jaykepeters/Blocklists/master/TV/sling.txt)
