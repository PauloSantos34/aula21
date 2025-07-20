# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium

# ===== TÍTULO =====
st.set_page_config(layout='wide')
st.title("🔍 Dashboard da Criminalidade por CISP - Rio de Janeiro")

# ===== CARREGAR DADOS =====
@st.cache_data
def carregar_dados():
    # Substitua pelo caminho real do seu CSV
    df = pd.read_csv("dados_criminalidade_cisp.csv", sep=";", encoding="utf-8")
    df['mes_ano'] = pd.to_datetime(df['mes_ano'], format='%Ym%m', errors='coerce')
    return df

df = carregar_dados()

# ===== SIDEBAR =====
st.sidebar.header("🎛️ Filtros")
ano = st.sidebar.multiselect("Ano", df['ano'].sort_values().unique(), default=df['ano'].max())
cisp = st.sidebar.multiselect("CISP", df['cisp'].sort_values().unique(), default=df['cisp'].unique())

# Aplicar filtros
df_filtrado = df[(df['ano'].isin(ano)) & (df['cisp'].isin(cisp))]

# ===== MÉTRICAS AGREGADAS =====
col1, col2, col3 = st.columns(3)
col1.metric("Letalidade Violenta", int(df_filtrado["letalidade_violenta"].sum()))
col2.metric("Roubos de Veículos", int(df_filtrado["roubo_veiculo"].sum()))
col3.metric("Total de Ocorrências", int(df_filtrado["registro_ocorrencias"].sum()))

# ===== GRÁFICO DE TENDÊNCIA =====
st.subheader("📈 Evolução Temporal - Letalidade Violenta")
grafico_tendencia = df_filtrado.groupby('mes_ano')['letalidade_violenta'].sum().reset_index()
fig = px.line(grafico_tendencia, x='mes_ano', y='letalidade_violenta', title='Letalidade Violenta ao longo do tempo')
st.plotly_chart(fig, use_container_width=True)

# ===== RANKING DE CISPs =====
st.subheader("🏆 Ranking de CISPs por Ocorrências")
ranking = df_filtrado.groupby("cisp")[['roubo_veiculo', 'letalidade_violenta', 'registro_ocorrencias']].sum().reset_index()
ranking = ranking.sort_values(by="registro_ocorrencias", ascending=False)
st.dataframe(ranking, use_container_width=True)

# ===== MAPA COM FOLIUM (opcional com coordenadas reais) =====
st.subheader("🗺️ Mapa Interativo por CISP")

# Exemplo com dados simulados de latitude e longitude
# Substitua pelos dados reais
coordenadas_cisp = {
    1: [-22.9035, -43.2096],
    2: [-22.9121, -43.2003],
    4: [-22.9125, -43.1767],
    5: [-22.8950, -43.2450],
    6: [-22.8617, -43.2795],
    7: [-22.8772, -43.3167],
    9: [-22.8625, -43.2789],
    10: [-22.8389, -43.3008],
    12: [-22.8431, -43.3653],
    19: [-22.9608, -43.2244]
}

m = folium.Map(location=[-22.9, -43.2], zoom_start=11)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df_filtrado.iterrows():
    cisp_id = row['cisp']
    coord = coordenadas_cisp.get(cisp_id)
    if coord:
        folium.Marker(
            location=coord,
            popup=(
                f"CISP: {cisp_id}<br>"
                f"Letalidade: {row['letalidade_violenta']}<br>"
                f"Roubos de Veículo: {row['roubo_veiculo']}<br>"
                f"Ocorrências: {row['registro_ocorrencias']}"
            ),
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(marker_cluster)

st_folium(m, width=1000, height=600)

# ===== OBSERVAÇÕES =====
st.info("📌 Este dashboard usa dados criminais agregados por CISP. Você pode adaptar para mostrar bairros, AISP ou meses específicos.")
