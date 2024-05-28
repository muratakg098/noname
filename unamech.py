import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import click

def check_uname(url, timeout=10, file=None):
    try:
        response = requests.get(url, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        nobr_tag = soup.find('nobr', string=lambda text: 'Linux' in text)  
        if nobr_tag:
            uname_info = nobr_tag.get_text(strip=True)
            result = "{} - {}".format(url, uname_info)
            click.secho(result, fg='green')
            if file:
                file.write(result + "\n")
                file.flush() 
        else:
            result = "{} -> failed".format(url)
            click.secho(result, fg='red')
    except Exception as e:
        result = "{} -> failed".format(url)
        click.secho(result, fg='red')

def main():
    input_file = input("List: ")
    output_file = "uname.txt"
    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        urls = [line.strip() for line in f_in]
        with ThreadPoolExecutor(max_workers=10) as executor:
            check_partial = partial(check_uname, timeout=10, file=f_out)
            executor.map(check_partial, urls)

if __name__ == "__main__":
    main()
