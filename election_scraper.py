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
    check_arguments(base_url)
    url = sys.argv[1]
    file_name = sys.argv[2]
    print(url, file_name)
    # first_soup = get_response(url)
    # results = get_municipality_links(first_soup, base_url)
    # print(f"Saving data to file: {file_name}")
    # save_to_csv(results, file_name)
    # print("All done, closing...")


def check_arguments(base_url):
    if len(sys.argv) != 3:
        print("Arguments were not entered correctly. Please check README and try it again.")
        exit()
    elif base_url not in sys.argv[1]:
        print("You have entered wrong URL. Please check README and try it again.")
        exit()
    elif ".csv" not in sys.argv[2]:
        print("You have entered wrong file name. Please check README and try it again.")
        exit()
    else:
        print(f"Downloading data from selected URL: {sys.argv[1]}")
    return


def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_municipality_links(first_soup, base_url):
    results = []
    i = 0
    names = first_soup.find_all('td', {'class': 'overflow_name'})
    for each_td in first_soup.find_all('td', {'class': 'cislo'}):
        line = [each_td.text]
        for each_name in names[i]:
            line.append(each_name.text)
        link = each_td.a['href']
        line.extend(collect_numbers(get_response(base_url + link)))
        results.append(line)
        i += 1

    # print(*results, sep="\n") Just for check
    return results


def collect_numbers(second_soup):
    data = []
    registered = second_soup.find('td', {'headers': 'sa2'}).text
    data.append(clean_numbers(registered))
    envelopes = second_soup.find('td', {'headers': 'sa5'}).text
    data.append(clean_numbers(envelopes))
    valid = second_soup.find('td', {'headers': 'sa6'}).text
    data.append(clean_numbers(valid))
    data.extend(collect_votes(second_soup))

    return data


def collect_votes(second_soup):
    data_votes = []
    votes = second_soup.find_all('td', {'headers': 't1sa2 t1sb3'})
    votes2 = second_soup.find_all('td', {'headers': 't2sa2 t2sb3'})
    for each in votes:
        data_votes.append(clean_numbers(each.text))
    for each in votes2:
        data_votes.append(clean_numbers(each.text))
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
    main()
