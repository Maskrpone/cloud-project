import pandas as pd
from io import BytesIO
import requests

DATASET_URL = "https://web.archive.org/web/20240423194012/https://naehrwertdaten.ch/wp-content/uploads/2023/08/Base_de_donnees_suisse_des_valeurs_nutritives.xlsx"  # web archive to have a fix URL


def fetch_data(URL):
    try:
        response = requests.get(URL, stream=True)
        response.raise_for_status()
        data = BytesIO(response.content)
        print("Data fetched")
        df = pd.read_excel(data, engine="openpyxl", skiprows=2)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error during download : {e}")
        return


def clean_data(df: pd.DataFrame):
    df = df.drop_duplicates()
    df = df.drop(columns=["ID V 4.0", "ID SwissFIR", "Densité", "Entrée modifiée"])
    df = df.drop(df.filter(regex=r"^Source.*").columns, axis=1)
    df = df.drop(df.filter(regex=r"^Dérivation de la valeur.*").columns, axis=1)
    df = df.drop(df.filter(regex=r"^Activité de *").columns, axis=1)

    double_parenthesis_pattern = r"\s*\([^)]+\)(?=\s*\([^)]+\))"
    df.columns = df.columns.str.replace(double_parenthesis_pattern, "", regex=True)
    df.columns = [
        col.strip().replace(",", "").replace(" ", "_").lower() for col in df.columns
    ]
    return df

raw_data = fetch_data(DATASET_URL)
data = clean_data(raw_data)
print(raw_data.columns)
