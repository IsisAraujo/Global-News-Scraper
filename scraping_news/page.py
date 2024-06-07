import requests
from bs4 import BeautifulSoup


class NewsPortal:
    def __init__(self, news_portal):
        self.news_portal = news_portal
        self.news = []

    def update_news(self):
        """
        Update the news from the specified news portal.
        """

        if self.news_portal.lower() == 'bbc':
            url = 'https://www.bbc.com/news'
            headers = {
                'User-Agent': (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")}

            response = requests.get(url, headers=headers)
            page_content = response.text
            soup = BeautifulSoup(page_content, 'html.parser')

            articles = soup.find_all('a', {'data-testid': 'internal-link'})

            news_dict = {}

            for article in articles:
                title_element = article.find(
                    'h2', {'data-testid': 'card-headline'})
                if title_element:
                    title = title_element.text.strip().upper()
                    link = article.get('href')
                    full_link = f"https://www.bbc.com{link}"
                    news_dict[title] = full_link

            self.news = news_dict

        if self.news_portal.lower() == 'globo':
            url = 'https://www.globo.com/'
            headers = {
                'User-Agent': (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")}

            response = requests.get(url, headers=headers)
            page_content = response.text
            soup = BeautifulSoup(page_content, 'html.parser')

            articles = soup.find_all(
                'a',
                class_=[
                    'post__link',
                    'post-multicontent__link'])

            news_dict = {}

            for article in articles:
                title_element = article.find(
                    'h2',
                    class_=[
                        'post__title',
                        'post-multicontent__link--title__text'])
                if title_element:
                    title = title_element.text.strip().upper()  
                    link = article.get('href')
                    full_link = link if link.startswith(
                        'http') else f"https://www.globo.com{link}"
                    news_dict[title] = full_link

            self.news = news_dict

        if self.news_portal.lower() == 'cnn':
            url = 'https://www.cnnbrasil.com.br/'
            headers = {
                'User-Agent': (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")}

            response = requests.get(url, headers=headers)
            page_content = response.text
            soup = BeautifulSoup(page_content, 'html.parser')

            articles = soup.find_all('li', class_="block__news__item")

            news_dict = {}

            for article in articles:
                link_element = article.find('a', href=True)
                title_element = article.find('h3', class_='block__news__title')
                if title_element and link_element:
                    title = title_element.text.strip().upper()
                    link = link_element['href']
                    full_link = link if link.startswith(
                        'http') else f"https://www.cnnbrasil.com.br{link}"
                    news_dict[title] = full_link

            self.news = news_dict



