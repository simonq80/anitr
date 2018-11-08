import requests
from bs4 import BeautifulSoup
import re
mal_url = "https://myanimelist.net"

class hs_api():
    def __init__(self, user):
        self.user = user
    
    def get_user_shows_info(self):
        return [self.get_show_info(url) for url in self.get_shows()]
    

    def get_shows(self):
        data = requests.get("{}/animelist/{}?status=1".format(mal_url, self.user))
        show_page = BeautifulSoup(data.text)
        def item_body(tag):
            return tag.has_attr('class') and re.compile("list-table").search(tag['class'][0])

        item_divs = show_page.find_all(item_body)[0]["data-items"]
        reg = '"anime_url":"(.*?)"'
        urls = re.findall(reg, item_divs)
        urls = [mal_url + url.replace('\\/', '/') for url in urls]
        return urls
        

    def get_show_info(self, show_url):
        try:
            data = requests.get(show_url)
            show_page = BeautifulSoup(data.text)
            main_name = show_page.find_all('h1')[0].span.contents[0].strip()
            alt_names = [] #implement if needed

            def space_div(tag):
                return tag.has_attr('class') and re.compile("spaceit").search(tag['class'][0])

            space_divs = show_page.find_all(space_div)
            episode_count = 0
            for div in space_divs:
                x = div.find_all(string=re.compile("Episodes:"))
                if len(x) > 0:
                    episode_count = int(div.contents[2])


            def spacepad_div(tag):
                return tag.has_attr('class') and re.compile("spaceit_pad").search(tag['class'][0])

            space_divs = show_page.find_all(spacepad_div)
            for div in space_divs:
                x = div.find_all(string=re.compile("English:"))
                if len(x) > 0:
                    alt_names = div.contents[2].strip()
                    
            names = [main_name] + [alt_names]

            to_return = {
                "names": names,
                "episodes": episode_count
            }
            print(to_return)
            return to_return
        except:
            return {
                "names": None,
                "episodes": 0
            }

    