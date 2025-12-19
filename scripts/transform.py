import pandas as pd
import os

# -----------------------------
# 1️⃣ Configuration des Chemins
# -----------------------------
PROCESSED_PATH = "data/processed"
FINAL_PATH = "data/final"
RAW_EXCEL_PATH = "data/raw/excel"
os.makedirs(FINAL_PATH, exist_ok=True)

# -----------------------------
# 2️⃣ Chargement des données
# -----------------------------
print("⏳ Chargement des fichiers...")
customers = pd.read_csv(f"{PROCESSED_PATH}/Customers.csv")
orders_sql = pd.read_csv(f"{PROCESSED_PATH}/Orders.csv")
order_details = pd.read_csv(f"{PROCESSED_PATH}/Order_Details.csv")
products = pd.read_csv(f"{PROCESSED_PATH}/Products.csv")

# Chargement Excel avec renommage immédiat pour éviter les conflits
orders_excel = pd.read_excel(f"{RAW_EXCEL_PATH}/orders.xlsx")
orders_excel = orders_excel.rename(columns={
    'Order ID': 'OrderID',
    'Order Date': 'OrderDate',
    'Shipped Date': 'ShippedDate',
    'Customer': 'CustomerID',
    'Employee': 'EmployeeID'
})

# Fusion des deux sources de commandes
orders = pd.concat([orders_sql, orders_excel], ignore_index=True)
orders['unique_row_id'] = range(len(orders)) # Identifiant unique pour les 878 lignes
initial_count = len(orders)

# -----------------------------
# 3️⃣ Nettoyage des Clés (Jointures)
# -----------------------------
def clean_keys(column):
    return column.astype(str).str.replace(r'\.0$', '', regex=True).str.strip().replace('nan', pd.NA)

for d in [orders, customers, order_details, products]:
    for col in ['CustomerID', 'OrderID', 'ProductID']:
        if col in d.columns:
            d[col] = clean_keys(d[col])

# -----------------------------
# 4️⃣ Jointures (Merge)
# -----------------------------
df = orders.merge(customers, on="CustomerID", how="left")
df = df.merge(order_details, on="OrderID", how="left")
df = df.merge(products, on="ProductID", how="left")

# -----------------------------
# 5️⃣ Normalisation des noms de colonnes
# -----------------------------
# Supprime espaces, underscores et met en minuscule
df.columns = df.columns.str.lower().str.replace(" ", "").str.replace("_","")
df = df.loc[:, ~df.columns.duplicated()]

# -----------------------------
# 6️⃣ SOUDURE DES DATES (Fix 2006 & 848 Livraisons)
# -----------------------------
# Gestion OrderDate (Date de commande)
date_cols = [col for col in df.columns if "orderdate" in col]
df["orderdate_main"] = pd.to_datetime(df[date_cols[0]], errors="coerce", dayfirst=True)
df["year"] = df["orderdate_main"].dt.year
df["month"] = df["orderdate_main"].dt.month

# Gestion ShippedDate (Le secret des 848 livraisons)
# On cherche toutes les colonnes qui pourraient contenir la date de livraison (ex: shippeddate, shippeddate.1)
ship_cols = [col for col in df.columns if "shippeddate" in col]
if len(ship_cols) > 1:
    df["shippeddate"] = df[ship_cols[0]].fillna(df[ship_cols[1]])
else:
    df["shippeddate"] = df[ship_cols[0]]

df["shippeddate"] = pd.to_datetime(df["shippeddate"], errors="coerce")

# -----------------------------
# 7️⃣ Calcul du Chiffre d'Affaires
# -----------------------------
# Récupération du prix unitaire (soit du détail, soit du produit)
if "unitpricex" in df.columns and "unitpricey" in df.columns:
    df["unitprice"] = df["unitpricex"].fillna(df["unitpricey"])
elif "unitpricex" in df.columns:
    df["unitprice"] = df["unitpricex"]
else:
    df["unitprice"] = df.get("unitpricey", 0)

df["unitprice"] = pd.to_numeric(df["unitprice"], errors='coerce').fillna(0)
df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce').fillna(0)
df["totalamount"] = df["unitprice"] * df["quantity"]

# -----------------------------
# 8️⃣ Rapport Final
# -----------------------------
print("\n" + "="*40)
print("📊 RAPPORT DE TRANSFORMATION")
print("="*40)
print(f"✅ Commandes sources conservées : {df['uniquerowid'].nunique()} / {initial_count}")
print(f"✅ Lignes de détails produites : {len(df)}")
print(f"💰 Chiffre d'affaires total : {df['totalamount'].sum():,.2f} €")
print(f"🚚 Commandes livrées : {df.groupby('uniquerowid')['shippeddate'].first().notna().sum()}")
print(f"📅 Années détectées : {sorted(df['year'].dropna().unique().astype(int))}")
print("="*40)

# Export
FINAL_CSV = f"{FINAL_PATH}/northwind_bi.csv"
df.to_csv(FINAL_CSV, index=False)
print(f"🚀 CSV généré avec succès : {FINAL_CSV}")