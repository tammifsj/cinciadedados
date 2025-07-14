import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Coffee Shop Dashboard Avançado", layout="wide")
st.title("☕ Coffee Shop Sales Dashboard - Análise Avançada")
st.markdown("""
Este dashboard explora detalhadamente os dados de vendas de uma rede de cafeterias.  
**Fonte:** Dataset de transações fictícias  
**Objetivo:** Avaliar desempenho por localidade, categoria, tipo de produto e comportamento temporal.
""")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("coffee_shop_clean.csv", parse_dates=["transaction_date", "transaction_datetime"])
    df["month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["hour"] = pd.to_datetime(df["transaction_datetime"]).dt.hour
    return df

df = load_data()

# --------------------------
# Filtros na sidebar
# --------------------------
st.sidebar.header("🎯 Filtros")

# Filtro por localização
locais = st.sidebar.multiselect("Localização da loja", options=df["store_location"].unique(), default=df["store_location"].unique())

# Filtro por categoria
categorias = st.sidebar.multiselect("Categoria de produto", options=df["product_category"].unique(), default=df["product_category"].unique())

# Filtro por mês
meses = st.sidebar.multiselect("Mês da transação", options=sorted(df["month"].unique()), default=sorted(df["month"].unique()))

# Aplicar filtros
df_filtrado = df[
    (df["store_location"].isin(locais)) &
    (df["product_category"].isin(categorias)) &
    (df["month"].isin(meses))
]

# --------------------------
# Layout com Tabs
# --------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Evolução Mensal", "🕓 Horários de Pico", "🔎 Produtos em Destaque"])

# --------------------------
# Aba 1 - Visão Geral
# --------------------------
with tab1:
    st.subheader("Total de Vendas por Localidade e Categoria")
    df_resumo = df_filtrado.groupby(["store_location", "product_category"])["total_price"].sum().reset_index()
    fig = px.bar(df_resumo, x="store_location", y="total_price", color="product_category", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Aba 2 - Evolução Mensal
# --------------------------
with tab2:
    st.subheader("Vendas Mensais por Categoria")
    evolucao = df_filtrado.groupby(["month", "product_category"])["total_price"].sum().reset_index()
    fig = px.line(evolucao, x="month", y="total_price", color="product_category", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Aba 3 - Horários de Pico
# --------------------------
with tab3:
    st.subheader("Distribuição de Transações por Hora")
    horas = df_filtrado.groupby("hour")["transaction_id"].count().reset_index()
    fig = px.bar(horas, x="hour", y="transaction_id", labels={"transaction_id": "Número de Transações", "hour": "Hora do Dia"})
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# Aba 4 - Produtos em Destaque
# --------------------------
with tab4:
    st.subheader("Produtos com Maior Faturamento")
    produtos = df_filtrado.groupby("product_detail")["total_price"].sum().reset_index().sort_values(by="total_price", ascending=False).head(15)
    fig = px.pie(produtos, names="product_detail", values="total_price", title="Top 15 Produtos por Faturamento")
    st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("Aplicativo desenvolvido para analizar as vendas de uma cafeteria")
