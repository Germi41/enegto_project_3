"""
election_scraper.py: Třetí projekt do Engeto Online Python Akademie
author: David Germ
email: david.germ@kiwi.com
discord: GermiCZ#2828
"""

import requests
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101"
    soup = get_response(url)
    links_table = get_municipality_links(soup, base_url)
    print(type(links_table))
    get_data(links_table)


def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def get_municipality_links(soup, base_url):
    url = []
    table = soup.find_all('td', {'class': 'center'})
    for each_td in table:
        line = each_td.a['href']
        url.append(base_url + line)
    return url


def get_data(links_table: list):
    # print(links_table)
    i = 0
    for link in links_table:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        collect_data(soup)
        # print(*soup, sep="\n")


def collect_data(soup):
    name = []
    table = soup.find_all('td', {'class': 'overflow_name'})
    for each_td in table:
        name.append(each_td.text)

    print(*name, sep="\n")




if __name__ == "__main__":
    print("Jedeme")
    main()
