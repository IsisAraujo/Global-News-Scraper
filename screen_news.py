import os
from threading import Thread
import time
from datetime import datetime
import sys
import pickle
import webbrowser
from math import ceil
from pytimedinput import timedInput

from scraping_news.page import NewsPortal


class ScrapingNews:
    def __init__(self):
        self.dict_site = {}
        self.all_sites = ['bbc', 'globo', 'cnn']

        self.screen = 0
        self.kill = False

        self.page = 1

        self.news = self.read_file('news') if 'news' in os.listdir() else []
        self.update_file(self.news, 'news')
        self.sites = self.read_file('sites') if 'sites' in os.listdir() else []
        self.update_file(self.sites, 'sites')

        for site in self.all_sites:
            self.dict_site[site] = NewsPortal(site)

        self.news_thread = Thread(target=self.update_news)
        self.news_thread.setDaemon(True)
        self.news_thread.start()

    def update_file(self, lista, mode='news'):
        with open(mode, 'wb') as fp:
            pickle.dump(lista, fp)

    def read_file(self, mode='news'):
        with open(mode, 'rb') as fp:
            n_list = pickle.load(fp)
            return n_list

    def receive_command(self, valid_commands, timeout=30):
        command, timed_out = timedInput('>>', timeout)
        while command.lower() not in [cmd.lower()
                                      for cmd in valid_commands] and not timed_out:
            print("Invalid command. Please try again\n")
            command, timed_out = timedInput('>>', timeout)
        command = command.lower()
        command = '0' if command == '' else command
        return command

    def main_loop(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            match self.screen:
                case 0:
                    print('WELCOME TO GLOBAL NEWS SCRAPER.')
                    print('Please choose an item from the menu')
                    print('')
                    print(
                        "1. Latest News\n2. Add Site\n3. Remove Site\n4. Exit Program")

                    self.screen = int(self.receive_command(
                        ['1', '2', '3', '4'], 5))
                    print(self.screen, type(self.screen))

                case 1:
                    self.display_news()
                    command = self.receive_command(['n', 'p', 'l', 'b'], 5)
                    match command:
                        case 'n':
                            if self.page < self.max_page:
                                self.page += 1

                        case 'p':
                            if self.page > 1:
                                self.page -= 1

                        case 'b':
                            self.screen = 0
                            continue

                        case 'l':
                            link = int(
                                input('>> Enter the article number you want to open: '))
                            if link < 1 or link > len(self.filtered_news):
                                print('Article does not exist!')
                            else:
                                webbrowser.open(
                                    self.filtered_news[link - 1]['link'])

                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(
                        'Enter the number of the site you want to add to the active sites list.\nPress 0 to return to the menu.')
                    print("\tACTIVE SITES ===============\n")
                    for i in self.sites:
                        print('\t', i)

                    print("\n\tINACTIVE SITES =============")
                    inactive_sites = [
                        i for i in self.all_sites if i not in self.sites]
                    for i in range(len(inactive_sites)):
                        print(f'\t{i+1}. {inactive_sites[i]}')
                    site = int(self.receive_command(
                        [str(i) for i in range(len(inactive_sites) + 1)], 50))

                    if site == 0:
                        self.screen = 0
                        continue
                    self.sites += [inactive_sites[site - 1]]
                    self.update_file(self.sites, 'sites')

                case 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(
                        'Enter the number of the site to remove it. To return to the menu, enter 0\n')
                    for i in range(len(self.sites)):
                        print(f'\t{i+1}. {self.sites[i]}')
                    site = int(self.receive_command(
                        [str(i) for i in range(len(self.sites) + 1)], 50))
                    if site == 0:
                        self.screen = 0
                        continue

                    del self.sites[site - 1]
                    self.update_file(self.sites, 'sites')

                case 4:
                    self.kill = True
                    sys.exit()

    def display_news(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        self.filtered_news = [
            i for i in self.news if i["source"] in self.sites]
        self.max_page = ceil(len(self.filtered_news) / 20)

        if self.page > self.max_page:
            self.page = 1

        start_index = (self.page - 1) * 10

        for i, article in enumerate(
                self.filtered_news[start_index:start_index + 10]):
            print(
                f"{start_index+i+1}. {article['date'].strftime('%d/%m/%Y %H:%M')} - {article['source'].upper()} - {article['article']}")
        print(f'Page {self.page}/{self.max_page}')

        print('================================================================\n')
        print('Commands:')
        print('N - Next Page | P - Previous Page | L - Open article in browser | B - Back')

    def update_news(self):
        while not self.kill:
            print('update')
            for site in self.all_sites:
                self.dict_site[site].update_news()

                for key, value in self.dict_site[site].news.items():
                    aux_dict = {}
                    aux_dict['date'] = datetime.now()
                    aux_dict['source'] = site
                    aux_dict['article'] = key
                    aux_dict['link'] = value

                    if len(self.news) == 0:
                        self.news.insert(0, aux_dict)
                        continue

                    add_article = True
                    for news_item in self.news:
                        if aux_dict["article"] == news_item["article"] and aux_dict["source"] == news_item["source"]:
                            add_article = False
                            break

                    if add_article:
                        self.news.insert(0, aux_dict)
            self.news = sorted(
                self.news,
                key=lambda d: d['date'],
                reverse=True)
            self.update_file(self.news, 'news')
            time.sleep(300)


self = ScrapingNews()
self.main_loop()
