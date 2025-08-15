import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEY_FIELD = "Title"
KEY_VALUE = "Bochum Projekte"
API_URL = "http://localhost:8000/update"

def get_project_count(url="https://bochum-mitgestalten.de"):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", class_="resources--info-count -no-default-style", href="/projekts")

    if link:
        spans = link.find_all("span")
        if len(spans) > 1:
            return spans[1].get_text(strip=True)
        else:
            print("Kein zweites <span> gefunden.")
            return None
    else:
        print("Link nicht gefunden.")
        return None

# === Sharepoint ===
def send_to_sharepoint(anzahl):
    print("Sending...")
    payload = {
        "key_field": KEY_FIELD,
        "key_value": KEY_VALUE,
        "fields": {
            "Anzahl": int(anzahl),
            "Datum": datetime.now().isoformat()
        }
    }
    try:
        resp = requests.post(API_URL, json=payload)
        resp.raise_for_status()
        print("Daten erfolgreich an SharePoint gesendet:", resp.json())
    except requests.RequestException as e:
        print("Fehler beim Senden an SharePoint:", e)

# === Main ===
def main():
    anzahl = get_project_count()
    if anzahl:
        print(f"Anzahl der Projekte: {anzahl}")
        send_to_sharepoint(anzahl)
    else:
        print("Konnte die Anzahl der Projekte nicht ermitteln.")

if __name__ == "__main__":
    main()