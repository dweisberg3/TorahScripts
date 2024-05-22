
import requests
import re

def remove_html_tags(text):
    # Regular expression to match HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_tractate_pages(tractate, num_dafs):
    pages = []
    for i in range(2, num_dafs + 1):
        pages.append(f"{tractate}.{i}a")
        pages.append(f"{tractate}.{i}b")
    return pages

def fetch_page_content(page):
    url = f"https://www.sefaria.org/api/v3/texts/{page}?version=hebrew|Wikisource%20Talmud%20Bavli"
    response = requests.get(url)
    return response.json()


def main():
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


    for tractate, page_num in talmud_tractates_daf_count.items():
           
            with open(f'{tractate.lower()}.txt', 'w') as textFile:
                pages = get_tractate_pages(tractate,page_num)
                # print(f'Mesechta : {tractate} . Num of Daf : {page_num} . Num of Pages : {len(pages)}')
                
                for page in pages:
                
                    content = fetch_page_content(page)
                    if "versions" in content:
                        content_no_html_tags = remove_html_tags((' '.join(content['versions'][0]['text'])))
                        page_name = page.split('.')
                        textFile.write(f'{page_name[0]} {page_name[1]} : \n')
                        textFile.write(f'{content_no_html_tags}\n')


if __name__ == "__main__":
    main()
