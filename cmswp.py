import sys
import requests
import re
from multiprocessing.dummy import Pool
from colorama import Fore, init
from pathlib import Path 
import os

os.system("cls" if os.name == "nt" else "clear")
init(autoreset=True)

fr = Fore.RED
fc = Fore.CYAN
fw = Fore.WHITE
fg = Fore.GREEN
fm = Fore.MAGENTA

print("""\033[1;32m        

WP CMS CHECKER 

""")

requests.urllib3.disable_warnings()

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    "referer": "www.bing.com",
}

try:
    fileName = input("\033[1;31mSite Lists: ")
    file = Path(__file__).with_name(fileName)
    try:
        target = [i.strip() for i in file.open("r", encoding="utf-8").readlines()]
    except UnicodeDecodeError:
        try:
            target = [i.strip() for i in file.open("r", encoding="latin-1").readlines()]
        except UnicodeDecodeError:
            try:
                target = [i.strip() for i in file.open("r", encoding=sys.getdefaultencoding()).readlines()]
            except UnicodeDecodeError:
                exit("\n\033[1;31m  [!] Unable to decode file with popular encodings")

except IndexError:
    path = str(sys.argv[0]).split("\\")
    exit("\n\033[1;31m  [!] Enter <" + path[len(path) - 1] + "> <your list.txt>")

poolAmount = int(input("\033[1;31mThreads: "))

cms_regex = {
    "Wordpress": '(wp-content\/(themes|plugins|mu\-plugins)\/[^\n\s]+\.(js|css)|name\="generator"\scontent\="WordPress|\/xmlrpc\.php|wp\-includes\/|wp-admin\/|\/index\.php\/|\/wp-login\.php\/|\/wp-config\.php\/|\/wp-signup\.php\/|\/wps\/)',
}

def check_cms(url):
    for cms, regex in cms_regex.items():
        if re.search(regex, requests.get(url, headers=headers, allow_redirects=True, timeout=15, verify=False).text, re.IGNORECASE):
            print(f"-> {url} --> {fg}[{cms}]")
            with open(f"{cms}.txt", "a") as f:
                f.write(url + "\n")
            break
    else:
        print(f"- {url} --> {fr}[Not Wordpress]")

ababa = Pool(poolAmount)
ababa.map(check_cms, target)
ababa.close()
ababa.join()

print(f"\n [!] {fc}Results saved.")
