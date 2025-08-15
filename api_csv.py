from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os

CSV_FILE = "daten.csv"

app = FastAPI(title="Test API für CSV-Updates")

class UpdateRequest(BaseModel):
    key_field: str
    key_value: str
    fields: dict

def upsert_csv_item(key_field: str, key_value: str, update_data: dict):
    # Falls Datei existiert, einlesen, sonst leere DataFrame anlegen
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=[key_field] + list(update_data.keys()))

    # Prüfen, ob Eintrag existiert
    if key_value in df[key_field].values:
        df.loc[df[key_field] == key_value, list(update_data.keys())] = list(update_data.values())
    else:
        new_row = {**update_data, key_field: key_value}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(CSV_FILE, index=False, sep=';')
    return True

@app.post("/update")
def update_item(req: UpdateRequest):
    upsert_csv_item(req.key_field, req.key_value, req.fields)
    return {"status": "success", "saved_to": CSV_FILE}