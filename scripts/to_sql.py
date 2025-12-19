import pandas as pd
import pyodbc
import numpy as np

# -------------------------------
# 1. Chargement du fichier parquet
# -------------------------------
df = pd.read_parquet(r"D:\BI\data\final\northwind_bi.parquet")
df = df.drop_duplicates(subset=["uniquerowid"])
print(f"📖 Fichier chargé : {len(df)} commandes uniques détectées.")

# -------------------------------
# 2. Normalisation des colonnes
# -------------------------------
for col, dtype in df.dtypes.items():
    if np.issubdtype(dtype, np.floating) or np.issubdtype(dtype, np.integer):
        df[col] = df[col].replace({np.nan: None})
    elif np.issubdtype(dtype, np.datetime64):
        # Remplace les dates hors limites par None
        df[col] = df[col].apply(
            lambda x: x if pd.isnull(x) or pd.Timestamp("0001-01-01") <= x <= pd.Timestamp("9999-12-31") else None
        )
    else:
        # Tout convertir en string et remplacer 'nan' par None
        df[col] = df[col].astype(str).replace({"nan": None})

# -------------------------------
# 3. Connexion SQL Server
# -------------------------------
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=Northwind_DWH;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# -------------------------------
# 4. Création dynamique de la table
# -------------------------------
table_name = "Fact_Orders"

# Supprime la table si elle existe
cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name};")

columns_sql = []
for col, dtype in df.dtypes.items():
    if np.issubdtype(dtype, np.integer):
        columns_sql.append(f"[{col}] INT")
    elif np.issubdtype(dtype, np.floating):
        columns_sql.append(f"[{col}] FLOAT")
    elif np.issubdtype(dtype, np.datetime64):
        columns_sql.append(f"[{col}] DATETIME2")  # DATETIME2 pour toutes les dates
    else:
        columns_sql.append(f"[{col}] NVARCHAR(MAX)")

create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns_sql)});"
cursor.execute(create_table_sql)
conn.commit()
print(f"✅ Table {table_name} créée avec {len(columns_sql)} colonnes.")

# -------------------------------
# 5. Insertion des données
# -------------------------------
cursor.fast_executemany = True
cols = ', '.join(f"[{c}]" for c in df.columns)
placeholders = ', '.join('?' for _ in df.columns)
insert_sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

# Conversion finale en liste de tuples
data = [tuple(x) for x in df.to_numpy()]
cursor.executemany(insert_sql, data)
conn.commit()

# -------------------------------
# 6. Vérification
# -------------------------------
cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
print(f"✅ Lignes confirmées dans {table_name} : {cursor.fetchone()[0]}")

cursor.close()
conn.close()
