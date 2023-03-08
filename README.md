# Enegto project 3

Třetí projekt na Python Akademii od Engeta.

## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Odkaz k prohlédnutí najdete zde.

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové
virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```commandline
$ pip3 --version                    # overim verzi manazeru
$ pip3 install -r requirements.txt  # nainstalujeme knihovny
```

## Spuštění projektu

Spuštěním souboru election_scraper.py v rámci příkazového řádku požaduje dva povinné argumenty.

```commandline
python election_scraper.py <odkaz-na-uzemni-celek> <nazev-vesledneho-souboru>
```

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`

## Ukázka projektu

Výsledky hlasování pro okres Hodonín:
    
1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205`
2. argument: `vysledky_hodonin.csv`

Spuštění programu:

`python election_scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205 
vysledky_hodonin.csv`

Průběh stahování:

```commandline
Downloading data from selected URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205
Saving data to file: vysledky_hodonin.csv
All done, closing...
```

Částečný výstup:

```commandline
Code,Location,Registered,Envelopes,Valid,Občanská demokratická strana....
586030,Archlebov,752,415,415,25,0,0,47,1,12,49,9,2,3,1,1,39,1,10,89,0,0,73,0,3,1,0,46,3,0
586048,Blatnice pod Svatým Antonínkem,1733,1066,1055,101,1,1,70,4,50,61,7,9,42,0,2,74,2,40,247,0,2,199,0,7,2,1,133,0,0
586056,Blatnička,356,239,238,16,0,0,14,0,10,17,3,0,1,0,0,23,0,4,58,0,5,42,0,0,0,2,43,0,0
...
```
