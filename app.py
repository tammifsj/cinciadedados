import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="Coffee Shop Dashboard", layout="wide")
st.title("☕ Coffee Shop Sales Dashboard")
st.markdown("""
Este dashboard analisa as vendas de uma cafeteria com base nas transações registradas ao longo do tempo.  
**Fonte:** Dataset fictício de transações  
**Objetivo:** Explorar padrões de vendas por tipo de produto, localidade e datas.
""")

#dados
@st.cache_data
def load_data():
    df = pd.read_csv("coffee_shop_clean.csv", parse_dates=["transaction_date", "transaction_datetime"])
    return df

df = load_data()

# Sidebar com filtro
st.sidebar.header("Filtros")
local = st.sidebar.selectbox("Selecione uma localidade", df["store_location"].unique())

df_filtrado = df[df["store_location"] == local]

# Tabs para visualizações
tab1, tab2, tab3 = st.tabs(["📊 Vendas por Categoria", "📈 Vendas ao Longo do Tempo", "🎯 Produtos em Destaque"])

with tab1:
    st.subheader("Total de Vendas por Categoria")
    categoria = df_filtrado.groupby("product_category")["total_price"].sum().reset_index()
    fig1 = px.bar(categoria, x="product_category", y="total_price", title="Total por Categoria")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Total de Vendas por Dia")
    por_data = df_filtrado.groupby("transaction_date")["total_price"].sum().reset_index()
    fig2 = px.line(por_data, x="transaction_date", y="total_price", title="Evolução das Vendas Diárias")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Produtos em Destaque")
    fig3 = px.sunburst(df_filtrado, path=["product_category", "product_type", "product_detail"],
                       values="total_price", title="Hierarquia de Produtos")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("Aplicativo desenvolvido para substituição da G2.")
