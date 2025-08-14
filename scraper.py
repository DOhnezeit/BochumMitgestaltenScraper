import requests
from bs4 import BeautifulSoup
# from shareplum import Site
# from shareplum import Office365
# from shareplum.site import Version
from datetime import datetime

# === Sharepoint-Config === 
# USERNAME = "test@test.de"
# PASSWORD = "test123"
# SHAREPOINT_SITE = "..."
# LIST_NAME = "Testliste"

# === Web-Scraping ===
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
# def add_project_count_to_sharepoint(count):
#     authcookie = Office365('https://bochumdigital.sharepoint.com', username=USERNAME, password=PASSWORD).GetCookies()
#     site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=authcookie)

#     sp_list = site.List(LIST_NAME)

#     datum = datetime.now().strftime("%Y-%m-%d")

#     data = {
#         'Title': f"Projekte am {datum}",
#         'ProjektAnzahl': count,
#         'Datum': datum
#     }

#     sp_list.UpdateListItems(data=data, kind='New')
#     print("Erfolgreich!")

# === Platzhalter zum Testen ohne SP ===
def add_project_count_to_sharepoint(count):
    heute = datetime.now().strftime("%d-%m-%Y")
    
    data = {
        'Title': f"Projekte am {heute}",
        'ProjektAnzahl': count,
        'Datum': heute
    }
    
    print("Simulierter SharePoint-Eintrag:")
    print(data)

# === Main ===
def main():
    anzahl = get_project_count()
    if anzahl:
        add_project_count_to_sharepoint(anzahl)
    else:
        print("Konnte die Anzahl der Projekte nicht ermitteln.")

if __name__ == "__main__":
    main()