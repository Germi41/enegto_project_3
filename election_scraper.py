"""
election_scraper.py: Třetí projekt do Engeto Online Python Akademie
author: David Germ
email: david.germ@kiwi.com
discord: GermiCZ#2828
"""
import unicodedata

import requests
import sys
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=5&xnumnuts=4101"
    soup = get_response(url)
    results = get_municipality_links(soup, base_url)
    # print(results)


def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_municipality_links(soup, base_url):
    results = []
    for each_td in soup.find_all('td', {'class': 'cislo'}):
        line = each_td.a['href']
        url = base_url + line
        line2 = [each_td.text]
        line2.extend(get_data(url))
        results.append(line2)

    print(*results, sep="\n")
    return results


def get_data(links_table):
    response = requests.get(links_table)
    soup = BeautifulSoup(response.text, "html.parser")
    data = collect_votes(soup)

    return data


def collect_votes(soup):
    data = []
    registered = soup.find('td', {'headers': 'sa2'}).text
    envelopes = soup.find('td', {'headers': 'sa5'}).text
    valid = soup.find('td', {'headers': 'sa6'}).text

    if "\xa0" in registered:
        clean_reg = unicodedata.normalize("NFKD", registered)
        data.append(clean_reg)
    else:
        data.append(registered)

    if "\xa0" in envelopes:
        clean_env = unicodedata.normalize("NFKD", envelopes)
        data.append(clean_env)
    else:
        data.append(envelopes)

    if "\xa0" in valid:
        clean_val = unicodedata.normalize("NFKD", valid)
        data.append(clean_val)
    else:
        data.append(valid)

    return data


# def save_to_csv(tabulka: list, file: str):
#     """Uloz tabulku men s datem do CSV souboru"""
#     header = ["Code", "Location", "Registered", "Envelopes",
#                "Valid", "Občanská demokratická strana",
#                "Řád národa - Vlastenecká unie", "CESTA ODPOVĚDNÉ SPOLEČNOSTI",
#                "Česká str.sociálně demokrat.", "Radostné Česko",
#                "STAROSTOVÉ A NEZÁVISLÍ", "Komunistická str.Čech a Moravy",
#                "Strana zelených", "ROZUMNÍ-stop migraci,diktát.EU",
#                "Strana svobodných občanů", "Blok proti islam.-Obran.domova",
#                "Občanská demokratická aliance", "Česká pirátská strana",
#                "Referendum o Evropské unii", "TOP 09",
#                "ANO 2011", "SPR-Republ.str.Čsl. M.Sládka",
#                "Křesť.demokr.unie-Čs.str.lid.", "Česká strana národně sociální",
#                "REALISTÉ", "SPORTOVCI", "Dělnic.str.sociální spravedl.",
#                "Svob.a př.dem.-T.Okamura (SPD)", "Strana Práv Občanů"]
#     with open(file, "w", encoding="utf-8", newline="") as csv_s:
#         write = csv.writer(csv_s, dialect="excel")
#         write.writerow(header)
#         write.writerows(tabulka)


if __name__ == "__main__":
    print("Jedeme")
    main()
