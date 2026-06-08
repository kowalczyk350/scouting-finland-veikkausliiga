import pandas as pd
from datetime import date, datetime
import os

def oblicz_wiek(data_urodzenia_str):
    try:
        urodzenie = datetime.strptime(str(data_urodzenia_str).strip(), "%Y-%m-%d")
        dzisiaj = date.today()
        return dzisiaj.year - urodzenie.year - ((dzisiaj.month, dzisiaj.day) < (urodzenie.month, urodzenie.day))
    except:
        return "Brak danych"

def glowna():
    sciezka_csv = "data/baza_zawodnikow.csv"
    
    try:
        df = pd.read_csv(sciezka_csv, sep=None, engine='python')
    except Exception as e:
        print(f"Blad podczas wczytywania pliku CSV: {e}")
        return

    df.columns = df.columns.str.strip()
    
    sciezka_szablonu = "raporty/szablon_raportu.md"
    if not os.path.exists(sciezka_szablonu):
        print(f"Blad: Nie znaleziono pliku szablonu w {sciezka_szablonu}")
        return
        
    with open(sciezka_szablonu, "r", encoding="utf-8") as f:
        szablon = f.read()
    
    for _, wiersz in df.iterrows():
        nazwisko_klucz = "imie_i_nazwisko" if "imie_i_nazwisko" in df.columns else df.columns[0]
        imie_nazwisko = str(wiersz[nazwisko_klucz]).strip()
        
        cechy_pilkarskie = ["szybkosc", "przyspieszenie", "wytrzymalosc", "sila", "drybling", "podania", "strzal", "dosrodkowanie", "pozycjonowanie", "decyzje", "pressing"]
        oceny = []
        for c in cechy_pilkarskie:
            if c in wiersz and pd.notna(wiersz[c]):
                oceny.append(float(wiersz[c]))
        
        ocena_koncowa = round(sum(oceny) / len(oceny), 1) if oceny else 0.0
        wiek = oblicz_wiek(wiersz.get("data_urodzenia", ""))
        
        raport = szablon
        raport = raport.replace("{{zawodnik}}", imie_nazwisko)
        raport = raport.replace("Klub:", f"Klub: {wiersz.get('klub', 'Brak danych')}")
        raport = raport.replace("Pozycja:", f"Pozycja: {wiersz.get('pozycja', 'Brak danych')}")
        raport = raport.replace("Wiek:", f"Wiek: {wiek} lat")
        
        for c in cechy_pilkarskie:
            nazwa_pola = c.capitalize() + ":"
            if c == "szybkosc": nazwa_pola = "Szybkość:"
            if c == "wytrzymalosc": nazwa_pola = "Wytrzymałość:"
            if c == "sila": nazwa_pola = "Siła:"
            if c == "strzal": nazwa_pola = "Strzał:"
            if c == "dosrodkowanie": nazwa_pola = "Dośrodkowanie:"
            
            wartosc_cechy = int(wiersz[c]) if c in wiersz and pd.notna(wiersz[c]) else ""
            raport = raport.replace(nazwa_pola, f"{nazwa_pola} {wartosc_cechy}")
        
        raport = raport.replace("{{ocena}}", f"{ocena_koncowa} / 10")
        
        cena = wiersz.get('cena_rynkowa', 0)
        cena_str = f"{cena:,}" if pd.notna(cena) else "0"
        
        uwagi_tekst = (
            f"Zawodnik o narodowości {wiersz.get('narodowosc', 'Brak')}. "
            f"Wartość rynkowa wynosi {cena_str} €. "
            f"Kontrakt wygasa {wiersz.get('kontrakt_do', 'Brak danych')}."
        )
        raport = raport.replace("{{uwagi}}", uwagi_tekst)
        raport = raport.replace("{{data}}", str(date.today()))
        
        os.makedirs("raporty", exist_ok=True)
        nazwa_pliku = f"raporty/{imie_nazwisko.replace(' ', '_')}.md"
        with open(nazwa_pliku, "w", encoding="utf-8") as f:
            f.write(raport)
            
    print("Sukces! Wszystkie raporty zostaly wygenerowane automatycznie bez bledow.")

if __name__ == "__main__":
    glowna()
