"""
election_scraper.py: Třetí projekt do Engeto Python Akademie
author: David Germ
email: david.germ@kiwi.com
discord: GermiCZ#2828
"""
import csv
import requests
import sys
from bs4 import BeautifulSoup


def main():
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205"
    soup = get_response(url)
    results = get_municipality_links(soup, base_url)
    save_to_csv(results, "vysledky.csv")


def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_municipality_links(soup, base_url):
    results = []
    i = 0
    names = soup.find_all('td', {'class': 'overflow_name'})
    for each_td in soup.find_all('td', {'class': 'cislo'}):
        line2 = [each_td.text]
        for each_name in names[i]:
            line2.append(each_name.text)
        line = each_td.a['href']
        line2.extend(collect_numbers(get_response(base_url + line)))
        results.append(line2)
        i += 1

    print(*results, sep="\n")
    return results


def collect_numbers(soup):
    data = []
    registered = soup.find('td', {'headers': 'sa2'}).text
    data.append(clean_numbers(registered))
    envelopes = soup.find('td', {'headers': 'sa5'}).text
    data.append(clean_numbers(envelopes))
    valid = soup.find('td', {'headers': 'sa6'}).text
    data.append(clean_numbers(valid))
    data.extend(collect_votes(soup))

    return data


def collect_votes(soup):
    data_votes = []
    votes = soup.find_all('td', {'headers': 't1sa2 t1sb3'})
    votes2 = soup.find_all('td', {'headers': 't2sa2 t2sb3'})
    for each in votes:
        data_votes.append(each.text)
    for each in votes2:
        data_votes.append(each.text)
    return data_votes


def clean_numbers(number):
    if "\xa0" in number:
        return ''.join(number.split())
    else:
        return number


def save_to_csv(results: list, file: str):
    """Uloz tabulku men s datem do CSV souboru"""
    header = ["Code", "Location", "Registered", "Envelopes",
               "Valid", "Občanská demokratická strana",
               "Řád národa - Vlastenecká unie", "CESTA ODPOVĚDNÉ SPOLEČNOSTI",
               "Česká str.sociálně demokrat.", "Radostné Česko",
               "STAROSTOVÉ A NEZÁVISLÍ", "Komunistická str.Čech a Moravy",
               "Strana zelených", "ROZUMNÍ-stop migraci,diktát.EU",
               "Strana svobodných občanů", "Blok proti islam.-Obran.domova",
               "Občanská demokratická aliance", "Česká pirátská strana",
               "Referendum o Evropské unii", "TOP 09",
               "ANO 2011", "SPR-Republ.str.Čsl. M.Sládka",
               "Křesť.demokr.unie-Čs.str.lid.", "Česká strana národně sociální",
               "REALISTÉ", "SPORTOVCI", "Dělnic.str.sociální spravedl.",
               "Svob.a př.dem.-T.Okamura (SPD)", "Strana Práv Občanů"]
    with open(file, "w", encoding="utf-8", newline="") as csv_s:
        write = csv.writer(csv_s, dialect="excel")
        write.writerow(header)
        write.writerows(results)


if __name__ == "__main__":
    print("Jedeme")
    main()
