import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# 1. CONFIGURATION DE LA PAGE
# ==============================
st.set_page_config(
    page_title="Northwind BI — Version PRO",
    layout="wide"
)

# ==============================
# 2. STYLE CSS (THEME SOMBRE)
# ==============================
st.markdown("""
<style>
.main { background-color: #0e1117; }
.stMetric {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. CHARGEMENT DES DONNÉES
# ==============================
@st.cache_data(show_spinner=False)
def load_data():
    file_path = "data/final/northwind_bi.parquet"
    df = pd.read_parquet(file_path)

    df['orderdate_main'] = pd.to_datetime(df['orderdate_main'], errors='coerce')
    df['shippeddate'] = pd.to_datetime(df['shippeddate'], errors='coerce')

    df['year'] = df['orderdate_main'].dt.year.astype('Int64')
    df['month_num'] = df['orderdate_main'].dt.month.astype('Int64')
    df['month_name'] = df['orderdate_main'].dt.strftime('%B')

    return df


df_raw = load_data()

# ==============================
# 4. KPI GLOBAUX
# ==============================
df_unique_total = df_raw.drop_duplicates(subset='uniquerowid')

total_c = len(df_unique_total)
livrees_c = df_unique_total['shippeddate'].notna().sum()
non_livrees_c = total_c - livrees_c
taux_livraison = (livrees_c / total_c * 100) if total_c > 0 else 0

# ==============================
# 5. SIDEBAR - FILTRES
# ==============================
st.sidebar.header("🔍 Configuration")

years_list = sorted(df_raw['year'].dropna().unique())
sel_years = st.sidebar.multiselect(
    "Années",
    years_list,
    default=years_list
)

empl_list = sorted(df_raw['employeeid'].dropna().unique())
sel_empl = st.sidebar.multiselect(
    "Employés",
    empl_list,
    default=empl_list
)

cust_list = sorted(df_raw['customerid'].dropna().unique())
sel_cust = st.sidebar.multiselect(
    "Clients",
    cust_list
)

# ==============================
# 6. FILTRAGE DES DONNÉES
# ==============================
df_f = df_raw[
    df_raw['year'].isin(sel_years) &
    df_raw['employeeid'].isin(sel_empl)
].copy()

if sel_cust:
    df_f = df_f[df_f['customerid'].isin(sel_cust)]

# ==============================
# 7. INTERFACE PRINCIPALE
# ==============================
st.title("📊 Dashboard BI — Version PRO")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total commandes", total_c)
c2.metric("Livrées", livrees_c)
c3.metric("Non livrées", non_livrees_c)
c4.metric("Taux livraison", f"{taux_livraison:.2f}%")

st.divider()

# ==============================
# CONFIGURATION PLOTLY (CENTRALISÉE)
# ==============================
plotly_config = {
    "displayModeBar": True,
    "responsive": True,
    "scrollZoom": False
}

# ==============================
# 8. GRAPHIQUE LINÉAIRE
# ==============================
st.subheader("📈 Volume des commandes par mois")

monthly_data = (
    df_f
    .drop_duplicates('uniquerowid')
    .groupby(['month_num', 'month_name'], as_index=False)
    .size()
    .rename(columns={'size': 'Nb'})
    .sort_values('month_num')
)

fig_line = px.line(
    monthly_data,
    x='month_name',
    y='Nb',
    markers=True,
    color_discrete_sequence=['#58a6ff']
)

fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="white"
)

st.plotly_chart(
    fig_line,
    use_container_width=True,
    config=plotly_config
)

# ==============================
# 9. RÉPARTITION RÉGIONALE
# ==============================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Livrées par région")
    fig_don1 = px.pie(
        df_f[df_f['shippeddate'].notna()],
        names='country',
        hole=0.6
    )
    st.plotly_chart(
        fig_don1,
        use_container_width=True,
        config=plotly_config
    )

with col_b:
    st.subheader("Non livrées par région")
    fig_don2 = px.pie(
        df_f[df_f['shippeddate'].isna()],
        names='country',
        hole=0.6
    )
    st.plotly_chart(
        fig_don2,
        use_container_width=True,
        config=plotly_config
    )

# ==============================
# 10. ANALYSE 3D
# ==============================
st.divider()
st.subheader("🧊 Analyse 3D : Période × Employé × Client")

fig_3d = px.scatter_3d(
    df_f.drop_duplicates('uniquerowid'),
    x='month_num',
    y='employeeid',
    z='customerid',
    color='year',
    size='totalamount',
    opacity=0.8,
    height=700
)

st.plotly_chart(
    fig_3d,
    use_container_width=True,
    config=plotly_config
)

# ==============================
# 11. REGISTRE COMPLET
# ==============================
st.divider()
st.subheader("📑 Registre complet")

st.dataframe(
    df_f,
    use_container_width=True
)
