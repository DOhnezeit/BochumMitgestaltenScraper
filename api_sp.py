from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import logging
import os

# === Logging ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/api_sp.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === Sharepoint-Config ===
URL = "https://bochumdigital.sharepoint.com" # später auf die richtige URL ändern
CLIENT_ID = "hier-steht-die-app-id" # Platzhalter
CLIENT_SECRET = "hier-steht-das-secret" # Platzhalter
LIST_NAME = "Dashboard" # ggf. auch ändern

# === FastAPI Setup ===
app = FastAPI(title="Sharepoint API")

# === Request-Model ===
class ListItemData(BaseModel): # Pydantic-Model
    Titel: str
    Anzahl: int
    source: str = "unbekannt" # Optional vielleicht sinnvoll, wo die Daten herkommen?
    Datum: datetime = Field(default_factory=datetime.now)
    external_id: str

# === Funktion zum Schreiben in Sharepoint ===
def write_to_sharepoint(data: dict):
    ctx = ClientContext(URL).with_credentials(ClientCredential(CLIENT_ID, CLIENT_SECRET))
    sp_list = ctx.web.lists.get_by_title(LIST_NAME)

    # +++ Vielleicht hier ID generieren +++

    sp_list.add_item(data).execute_query()

# === Endpoint ===
@app.post("/update")
def update_list(item: ListItemData):
    try:
        write_to_sharepoint(item.model_dump())
        logging.info(f"Erfolgreich geschrieben: {item.model_dump()}")
        return {"status": "success"}
    except Exception as e:
        logging.error(f"Fehler beim Schreiben: {e}")
        return {"status": "error", "message": str(e)}