#tento kod sthuje z prihlasky patentu casovou osu

import requests

from bs4 import BeautifulSoup
import time
import csv

# Název přihlášky
nazev_prihlasky = "2015-923"

# Krok 1: Získejte dotaz ID z první URL
url1 = "https://isdv.upv.gov.cz/webapp/resdb.dotaz.getDotazID"
data1 = {
    "pD": "1730824751721"
}
response1 = requests.post(url1, data=data1)
if response1.status_code != 200:
    print(f"Chyba při získávání ID dotazu, status code: {response1.status_code}")
    exit()

# Zpoždění 3 sekundy mezi požadavky
time.sleep(3)

# Krok 2: Odeslání žádosti s číslem přihlášky
url2 = "https://isdv.upv.gov.cz/webapp/!resdb.formxml.make"
data2 = {
    "dotaz/polozka[2]/hodnota": nazev_prihlasky
}
response2 = requests.post(url2, data=data2)
if response2.status_code != 200:
    print(f"Chyba při odesílání přihlášky, status code: {response2.status_code}")
    exit()

# Zpoždění 3 sekundy mezi požadavky
time.sleep(3)

# Krok 3: Získání dat z divu s třídou 'casosaobal'
url3 = "https://isdv.upv.gov.cz/webapp/resdb.print_detail.Detail"
data3 = {
    "pIdSpis": "qEfEalyxDRBGfJx",       # Tento parametr je potřeba aktualizovat podle skutečné hodnoty
    "pLang": "CS",
    "pIdDotaz": "RES0000000032965488AvhEPUZB",  # Tento parametr může být také dynamický
    "pD": "1730825374356"              # Tento parametr je nutné získat z předchozích kroků nebo zadat
}

response3 = requests.post(url3, data=data3)
if response3.status_code != 200:
    print(f"Chyba při získávání časové osy, status code: {response3.status_code}")
    print(f"Odpověď serveru: {response3.text}")
    exit()

# Zpracování odpovědi pomocí BeautifulSoup
soup = BeautifulSoup(response3.text, 'html.parser')

# Vyhledání divu s třídou "casosaobal"
casosaobal_div = soup.find('div', {'class': 'casosaobal'})
if casosaobal_div:
    # Otevřeme soubor CSV pro zápis
    with open('casova_osa.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Zapisujeme hlavičku CSV souboru
        writer.writerow(["Nazev prihlasky", "Datum", "Popis"])
        
        # Najdeme všechny prvky "tlpoint", které obsahují data
        timeline_points = casosaobal_div.find_all('div', {'class': 'tlpoint'})
        
        for point in timeline_points:
            # Extrahujeme datum
            date = point.find('span', {'class': 'dtm'}).text.strip()
            # Extrahujeme popis
            description = point.find('p').text.strip()
            # Zapisujeme do CSV
            writer.writerow([nazev_prihlasky, date, description])
    
    print("Data byla úspěšně uložena do casova_osa.csv")
else:
    print("Data nebyla nalezena")
