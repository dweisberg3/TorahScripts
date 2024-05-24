
import requests
import json
import sys
import glob
from dominate import document
from dominate.tags import *
import re
import urllib.parse


def remove_and_capture_between_hyphen_colon(s):
    # Define the regex pattern to match the characters between "-" and ":"
    pattern = r'-.*?:'
    # Find all matches of the pattern
    removed_texts = re.findall(pattern, s)
    # Use re.sub() to replace the matched patterns with an empty string
    modified_string = re.sub(pattern, '', s)
    # Join all removed texts into a single string if needed, or keep as list
    removed_text = ''.join(removed_texts)
    return modified_string, removed_text



def remove_html_tags(text):
    # Regular expression to match HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def format_rashi(text):
#     pattern = r": ([^-]+) -"

# # Define the replacement pattern
#     replacement = r"\1\n"

# # Perform the replacement
#     return re.sub(pattern, replacement, text)
    return text

talmud_tractates_daf_count = {
    "Berakhot": 64,
    "Shabbat": 157,
    "Eruvin": 105,
    "Pesachim": 121,
    "Yoma": 88,
    "Sukkah": 56,
    "Beitzah": 40,
    "Rosh Hashanah": 35,
    "Taanit": 31,
    "Megillah": 32,
    "Moed Katan": 29,
    "Chagigah": 27,
    "Yevamot": 122,
    "Ketubot": 112,
    "Nedarim": 91,
    "Nazir": 66,
    "Sotah": 49,
    "Gittin": 90,
    "Kiddushin": 82,
    "Bava Kamma": 119,
    "Bava Metzia": 119,
    "Bava Batra": 176,
    "Sanhedrin": 113,
    "Makkot": 24,
    "Shevuot": 49,
    "Avodah Zarah": 76,
    "Horayot": 14,
    "Zevachim": 119,
    "Menachot": 110,
    "Chullin": 142,
    "Bekhorot": 61,
    "Arakhin": 34,
    "Temurah": 34,
    "Keritot": 27,
    "Meilah": 21,
    "Tamid": 10,
    "Middot": 10,
    "Kinnim": 3,
    "Niddah": 73
}

def fetch_page_content(section):
    url = f"https://www.sefaria.org/api/v3/texts/{section}"
    print(f'the url {url}')
    response = requests.get(url)
    return response.json()

def get_tractate_pages(tractate, num_dafs):
    pages = []
    for i in range(2, num_dafs + 1):
        pages.append(f"{tractate}.{i}a")
        pages.append(f"{tractate}.{i}b")
    return pages

def main():
    version = "?version=hebrew|Wikisource%20Talmud%20Bavli"
    args = sys.argv
    mesechta = args[1]
    perush   = args[2]
    dafs = talmud_tractates_daf_count[mesechta]
    pages = get_tractate_pages(mesechta,dafs)
    print(f'mesechta : {mesechta}   perush : {perush}')
    with document(title='Shas') as doc:
         style_content = """
            .hebrew-text {
                direction: rtl;      /* Set text direction to right-to-left */
                text-align: right;   /* Align text to the right */
                white-space: pre-wrap; /* Preserve whitespace and wrap lines as necessary */
            }
            """
         style(style_content)
         h1('Gemara')
         for idx, page in enumerate(pages):
            # print(idx)
            rashi_url = f'Rashi%20on%20'
            rashi_idx = 1
            if(idx == 0):
                daf = page.split(".")[-1]
                print(daf)
                daf_side = page[-1]
                print(f'daf side {daf_side}')
                content = fetch_page_content(f'{page}{version}')
                # print(content['he'])
                final_content = remove_html_tags((' '.join(content['versions'][0]['text'])))
                pre(final_content,cls='hebrew-text')
                rashi_content = fetch_page_content(f'Rashi%20on%20{page}:{rashi_idx}')
                with open('ziziz.json','w') as junk:
                    json.dump(rashi_content,junk,indent=4)
                final_rashi_content = format_rashi(' '.join(rashi_content['versions'][0]['text'][0]))
                print( final_rashi_content)
                print(rashi_content['sections'])
                while(rashi_content['sections'][0] == daf):
                    next_one = rashi_content['next']
                    print(f' the next!!!!!! {next_one}')
                    path = '%20'.join(next_one)
                    print(f' the path   {path}')
                    rashi_content = fetch_page_content(urllib.parse.quote(next_one))

                    print('hehehe')
                    with open('stuf.json','w') as junk:
                        json.dump(rashi_content,junk,indent=4)
                    print(' '.join(rashi_content['versions'][0]['text'][0]))
                    final_rashi_content = format_rashi(''.join(rashi_content['versions'][0]['text'][0]))
                    with open("rashi.txt", 'w') as ff:
                        ff.write(final_rashi_content)
                    final_rashi_content = final_rashi_content.split(":")
                    # h2(perush)
                    for dibur_hamaschil in final_rashi_content:
                        gemera_quote_with_perush = dibur_hamaschil.split("-")
                    
                        if(len(gemera_quote_with_perush) == 1):
                            print("got in 1")
                            pre(b(''.join(dibur_hamaschil)),cls='hebrew-text')
                            continue
                        if(len(gemera_quote_with_perush) == 2):
                            print("got in 2")
                        
                            pre(b(gemera_quote_with_perush[0]),gemera_quote_with_perush[1],cls='hebrew-text')
                        
                        # print(len(gemera_quote_with_perush))
                # mod, removed = remove_and_capture_between_hyphen_colon(final_rashi_content)
               
                # pre(final_rashi_content,cls='hebrew-text')
              

    with open('shas.html', 'w') as f:
        f.write(doc.render())
    # rashi = fetch_page_content()
    # with open('rashi.json', 'w') as jsonfile:
    #     json.dump(rashi,jsonfile,indent=4,ensure_ascii=False)
    # # print(type(rashi))
    # if(not rashi['he']):
    #     print('fghfghfg')
    # rashi = str(rashi)
    # # for i in range(0,len(rashi),80):
        
    #   print(rashi[i:i+80])

if __name__ == "__main__":
    main()