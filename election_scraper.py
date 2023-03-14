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
    first_soup = get_response(url)
    results, header = get_municipality_links(first_soup, base_url)
    print(f"Saving data to file: {file_name}")
    save_to_csv(results, header, file_name)
    print("All done, closing...")


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
    header = []
    each_region = 0

    names = first_soup.find_all('td', {'class': 'overflow_name'})
    for each_td in first_soup.find_all('td', {'class': 'cislo'}):
        line = [each_td.text]
        for each_name in names[each_region]:
            line.append(each_name.text)
        link = each_td.a['href']
        if each_region == 0:  # Pokud beru hlasy z prvniho regionu, vytvor header
            header = create_header(get_response(base_url + link))
            line.extend(collect_numbers(get_response(base_url + link)))
        else:
            line.extend(collect_numbers(get_response(base_url + link)))
        results.append(line)
        each_region += 1

    return results, header


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


def create_header(second_soup):
    header = ["Code", "Location", "Registered", "Envelopes",
              "Valid"]
    for party_name in second_soup.find_all('td', {'class': 'overflow_name'}):
        header.append(party_name.text)

    return header


def collect_votes(second_soup):
    data_votes = []
    number = 1
    table_count = len(second_soup.find_all('table'))

    while number < table_count:
        votes = second_soup.find_all('td', {'headers': f't{number}sa2 t{number}sb3'})
        for each in votes:
            data_votes.append(clean_numbers(each.text))
        number += 1

    return data_votes


def clean_numbers(number):
    if "\xa0" in number:
        return ''.join(number.split())
    else:
        return number


def save_to_csv(results: list, header: list, file: str):
    with open(file, "w", encoding="utf-8", newline="") as csv_s:
        write = csv.writer(csv_s, dialect="excel")
        write.writerow(header)
        write.writerows(results)


if __name__ == "__main__":
    main()
