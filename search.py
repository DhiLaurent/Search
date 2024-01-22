import os
import subprocess
import time
import sys

os.environ['SHELL'] = '/bin/bash'
def clear():
    subprocess.run('clear', shell=True)


def help():
    print("+-----------------------------------------+")
    print("| [1] - Parsing source code Enum          |\n"
          "| [2] - Google Hacking                    |\n"
          "| [3] - Zone Transfer validation          |\n"
          "| [4] - Check Alias (SubDomain Take Over) |\n"
          "| [5] - Wayback Enumeration               |")
    print("+-----------------------------------------+\n")

clear()
help()

user_input = input("Number: ")



if user_input == "1":
    try:
        url = input("URL: ")
        extensions = input("Extension Search? (Y/N): ").upper()
        if extensions == "Y":
            extension = input("Exemple: php,txt,html...\nType extension without dot: ").lower()
            download_source = f'wget {url} -O output.html 2>/dev/null'
            subprocess.run(download_source, shell=True)
            parsing_extension = rf"grep -o '\b[[:alnum:]_]*\.{extension}\b' output.html | sort | uniq "
            result_parsing_extension = subprocess.run(parsing_extension, shell=True, stdout=subprocess.PIPE, text=True)
            print("-" * 50)
            print(f"[*] Extensions \n\n{result_parsing_extension.stdout}")
            print("-" * 50)
            cleaning = 'rm output.*'
            remove = subprocess.run(cleaning, shell=True)


        else:
            # Download Source Code
            print("[*] Download and Parsing...")
            download_source = f'wget {url} -O output.html 2>/dev/null'
            subprocess.run(download_source, shell=True)

            # Parsing href
            print("-" * 50)
            parsing_href = 'cat output.html | grep "href" | cut -d "/" -f3 | grep "\\." | cut -d \'"\' -f1 | grep -v "<l" | grep -v ";" | grep -v "linkTags" | sort | uniq'

            # Parsing dirs / files
            # parsing_dirs = 'cat output.html | grep -oP \'href="(http[s]?://[^"]+)\' | cut -d \'"\' -f2 | grep -v "?" | sort | uniq '
            parsing_dirs = 'cat output.html | grep -oP \'href="([^"]+)\' | cut -d \'"\' -f2 | grep -v "#" | grep -v "javascript" | grep -v "?" | sort | uniq'


            # Parsing src
            parsing_src_1 = 'cat output.html | grep \'src="\' | cut -d \'"\' -f2 | grep "https" | grep "https" | sort | uniq '
            parsing_src_2 = 'cat output.html | grep \'src="\' | cut -d \'"\' -f2 | sort | uniq'


            parsing_href_param = """cat output.html | grep -oP 'href="(http[s]?://[^"]+)' | grep "?" | cut -d '"' -f2 | sort | uniq """
            parsing_href_param += """ && cat output.html | grep -oP 'href="\\?[^\"]*' | sed 's/href="//; s/\"$//' | sort | uniq"""


            # Parsing results
            result_parsing = subprocess.run(parsing_href, shell=True, stdout=subprocess.PIPE, text=True)
            result_parsing_dirs = subprocess.run(parsing_dirs, shell=True, stdout=subprocess.PIPE, text=True)
            result_parsing_param = subprocess.run(parsing_href_param, shell=True, stdout=subprocess.PIPE, text=True)
            result_parsing_src = subprocess.run(parsing_src_1, shell=True, stdout=subprocess.PIPE, text=True)
            result_parsing_src_1 = subprocess.run(parsing_src_2, shell=True, stdout=subprocess.PIPE, text=True)


            # Print Results
            print(f"[*] HREF Domains/Subdomains\n\n{result_parsing.stdout}")
            print("-" * 50)
            print(f"[*] HREF Directories/Files\n\n{result_parsing_dirs.stdout}")
            print("-" * 50)
            print(f"[*] HREF Parameters: \n\n{result_parsing_param.stdout}")
            print("-" * 50)
            print(f"[*] SRC Files\n\n{result_parsing_src.stdout}\n{result_parsing_src_1.stdout}")

            # Remove index.html
            cleaning = 'rm output.*'
            remove = subprocess.run(cleaning, shell=True)
    except Exception as error:
        print(f"[!] {error}")
        exit()

elif user_input == "2":
    from googlesearch import search

    def search_google(query):
        results = []
        for j in search(query, num=5, stop=5, pause=2, extra_params={'filter': '0'}):
            results.append({
                'title': j,
                'url': j
            })

        return results

    def help():
        print("\033[31m[!] Be careful when searching too much,may 429 code appears\033[m")
        print("[1] - Search only domain\n[2] - Search Index Of")

    query = input("Domain: ")
    help()
    google = input("Type a number: ")
    if google == "1":
        form = "site:" + query
        print("-" * 50)
        print("[*] Searching...")
        search_results = search_google(form)
        print("[!] Domain results")
        print("-" * 50)
        for result in search_results:
            print(f"URL: {result['url']}")
            print("-" * 50)

    if google == "2":
        form = "site:" + query + ' intitle: "index of" "parent directory"'
        print("-" * 50)
        print("[*] Searching...")
        search_results = search_google(form)
        print("-" * 50)
        print("[!] Index of results")
        print("-" * 50)
        for result in search_results:
            print(f"URL: {result['url']}")
            print("-" * 50)

elif user_input == "3":
    domain = input("Domain: ")
    zone_transfer = f'for server in $(host -t ns {domain} | cut -d " " -f4); do host -l -a {domain} $server | grep -v "failed" | grep -v "timed out" | grep -v "no servers could be reached"; done'
    result_zt = subprocess.run(zone_transfer, shell=True, stdout=subprocess.PIPE, text=True)
    print(result_zt.stdout)

elif user_input == "4":
    print("[!] Need Sub domain list\n"
          "[*] Example:\n"
          "www\n"
          "www2\n"
          "admin\n"
          "support")
    file = input("File name: ")
    domain = input("Domain: ")
    alias_sdtk = f'for palavra in $(cat {file});do host -t cname $palavra.{domain} | grep "alias for"; done'

    result_sdtk = subprocess.run(alias_sdtk, shell=True, stdout=subprocess.PIPE, text=True)
    print("-" * 50)
    print(result_sdtk.stdout)
    print("-" * 50)

elif user_input == "5":
    try:
        import importlib
        importlib.import_module('waybackpy')
        print("[1] - Sub domain Enumeration\n"
            "[2] - Enumerate all\n")
        option = input("Type an option: ") 
        domain = input("Type domain: ")
        if option == "1":
            sub_domains = f'waybackpy -u {domain} -sub --known-urls | cut -d "/" -f1,2,3 | sort | uniq'
            result_wayback_sub = subprocess.run(sub_domains, shell=True, stdout=subprocess.PIPE, text=True)
            print(result_wayback_sub.stdout)
        elif option == "2":
            results = f'waybackpy -u {domain} -sub --known-urls'
            result_wayback = subprocess.run(results, shell=True, stdout=subprocess.PIPE, text=True)
            print(result_wayback.stdout)

    except Exception as error:
        print(f"[!] Module waybackpy not installed\n[*] {error}")
        result_install = subprocess.run('pip3 install waybackpy > /dev/null 2>&1', shell=True)
        print("[!] Module waybackpy installed run script again!")
        exit(0)
       

else:
    print("[!] Type valid number")
    exit()
