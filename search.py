import os
import subprocess
import time
import sys

os.environ['SHELL'] = '/bin/bash'
os.system("clear")
def help():
    print("[1] - Parsing source code Enum")

user_input = int(input("Number: "))




if user_input == 1:


    try:
        url = str(input("URL: "))
        # Download Source Code
        print("[*] Download and Parsing...")
        download_source = f'wget {url} -O output.html 2>/dev/null'
        subprocess.run(download_source, shell=True)

        # Parsing href
        print("-" * 50)
        parsing_href = 'cat output.html | grep "href" | cut -d "/" -f3 | grep "\\." | cut -d \'"\' -f1 | grep -v "<l" | grep -v ";" | grep -v "linkTags" | sort | uniq'

        # Parsing dirs / files
        parsing_dirs = 'cat output.html | grep -oP \'href="(http[s]?://[^"]+)\' | cut -d \'"\' -f2 | grep -v "?" | sort | uniq '

        # Parsing src
        parsing_src_1 = 'cat output.html | grep \'src="\' | cut -d \'"\' -f2 | grep "https" | grep "https" | sort | uniq '
        parsing_src_2 = 'cat output.html | grep \'src="\' | cut -d \'"\' -f2 | sort | uniq'

        parsing_href_param = 'cat output.html | grep -oP \'href="(http[s]?://[^"]+)\' | grep "?" | cut -d \'"\' -f2 | sort | uniq '
        #parsing_href_param = 'cat output.html | grep -oP "href=\"(http[s]?://[^\"]+|\?[^\"]+)" | cut -d \" -f2'
        #parsing_href_param = r"grep -oE 'href=\"(http[s]?://[^\"]+|\?[^\"]+)\"' output.html | cut -d '\"' -f2"


        # Parsing results
        result_parsing = subprocess.run(parsing_href, shell=True, stdout=subprocess.PIPE, text=True)
        result_parsing_dirs = subprocess.run(parsing_dirs, shell=True, stdout=subprocess.PIPE, text=True)
        result_parsing_param = subprocess.run(parsing_href_param, shell=True, stdout=subprocess.PIPE, text=True)
        result_parsing_src = subprocess.run(parsing_src_1, shell=True, stdout=subprocess.PIPE, text=True)
        result_parsing_src_1 = subprocess.run(parsing_src_2, shell=True, stdout=subprocess.PIPE, text=True)


        # Print Results
        print(f"[*] HREF Domains/Subdomains\n{result_parsing.stdout}")
        print("-" * 50)
        print(f"[*] HREF Directories/Files\n{result_parsing_dirs.stdout}")
        print("-" * 50)
        print(f"[*] HREF Parameters: \n{result_parsing_param.stdout}")
        print("-" * 50)
        print(f"[*] SRC Files\n{result_parsing_src.stdout}\n{result_parsing_src_1.stdout}")

        # Remove index.html
        cleaning = 'rm output.*'
        remove = subprocess.run(cleaning, shell=True)
    except Exception as error:
        print(f"[!] {error}")
    exit()

