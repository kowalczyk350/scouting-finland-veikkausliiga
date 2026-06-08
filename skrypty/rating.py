def player_rating(speed, dribbling, strength, decisions):
    weights = {
        "speed": 0.3,
        "dribbling": 0.3,
        "strength": 0.2,
        "decisions": 0.2
    }

    rating = (
        speed * weights["speed"] +
        dribbling * weights["dribbling"] +
        strength * weights["strength"] +
        decisions * weights["decisions"]
    )

    return round(rating, 2)


# przykład (Topi Keskinen)
print(player_rating(9, 8, 6, 7))
import pandas as pd
from datetime import date

def glowna():
    # wczytaj CSV
    df = pd.read_csv("data/baza_zawodnikow.csv")
    
    # dla każdego wiersza oblicz ocenę
    df["ocena"] = df.apply(
        lambda row: player_rating(
            row["szybkosc"],
            row["drybling"],
            row["sila"],
            row["decyzje"]
        ),
        axis=1
    )
    
    # wczytaj szablon raportu
    with open("raporty/szablon_raportu.md", "r") as f:
        szablon = f.read()
    
    # dla każdego zawodnika wygeneruj raport
    for _, wiersz in df.iterrows():
        raport = szablon.replace("{{data}}", str(date.today()))
        raport = raport.replace("{{zawodnik}}", wiersz["zawodnik"])
        raport = raport.replace("{{ocena}}", str(wiersz["ocena"]))
        raport = raport.replace("{{uwagi}}", "Brak dodatkowych uwag.")
        
        # zapisz do pliku
        nazwa_pliku = f"raporty/{wiersz['zawodnik'].replace(' ', '_')}.md"
        with open(nazwa_pliku, "w") as f:
            f.write(raport)
    
    print("Raporty wygenerowane dla wszystkich zawodników.")

if __name__ == "__main__":
    glowna()
