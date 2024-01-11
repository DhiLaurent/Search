import os
import subprocess
import time
import sys

os.environ['SHELL'] = '/bin/bash'
os.system("clear")
def help():
    print("[1] - Parsing source code Enum")

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

if user_input == "2":
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

