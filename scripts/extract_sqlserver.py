import pandas as pd
import pyodbc
import os

# Chemin de sortie pour les fichiers CSV
OUTPUT_PATH = "data/raw/sqlserver/"

# Crée le dossier si il n'existe pas
os.makedirs(OUTPUT_PATH, exist_ok=True)

def extract_from_sqlserver():
    # Connexion à SQL Server
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=Northwind;"
        "Trusted_Connection=yes;"
    )

    # Liste des tables à extraire (avec échappement des noms problématiques)
    tables = [
        "Customers",
        "Orders",
        "[Order Details]",  # espace + mot réservé "Order"
        "Employees",
        "Categories",
        "Shippers",
        "Suppliers",
        "Products"
    ]

    # Extraction et sauvegarde
    for table in tables:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            df.to_csv(os.path.join(OUTPUT_PATH, f"{table.strip('[]')}.csv"), index=False)
            print(f"[OK] Extracted {table}")
        except Exception as e:
            print(f"[ERREUR] Impossible d'extraire {table} : {e}")

    # Fermeture de la connexion
    conn.close()

if __name__ == "__main__":
    extract_from_sqlserver()
