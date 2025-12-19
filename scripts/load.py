import pandas as pd
import os

INPUT_FILE = "data/final/northwind_bi.csv"
OUTPUT_PARQUET = "data/final/northwind_bi.parquet"

def load_and_validate():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erreur : Le fichier {INPUT_FILE} est introuvable.")
        return

    # 1. Chargement
    df = pd.read_csv(INPUT_FILE)

    # 2. Conversion Date robuste
    df['orderdate_main'] = pd.to_datetime(df['orderdate_main'], format='mixed', errors='coerce')

    # 3. Analyse des volumes
    total_lignes = len(df)
    commandes_uniques = df['uniquerowid'].nunique() if 'uniquerowid' in df.columns else 0

    print("--- 📋 DIAGNOSTIC DU CHARGEMENT ---")
    print(f"📊 Lignes dans le CSV : {total_lignes}")
    print(f"📊 Commandes trouvées : {commandes_uniques}")

    # ALERTE SI DIFFERENT DE 878
    if commandes_uniques != 878:
        print(f"⚠️ ATTENTION : Il manque {878 - commandes_uniques} commandes !")
        print("👉 Vérifiez que votre fichier CSV contient bien les données de 1996, 1997, 1998 ET 2006.")
    else:
        print("✅ Parfait ! Les 878 commandes sont présentes.")

    # 4. Sauvegarde Parquet
    df.to_parquet(OUTPUT_PARQUET, index=False)
    print(f"\n🚀 Fichier mis à jour : {OUTPUT_PARQUET}")

if __name__ == "__main__":
    load_and_validate()