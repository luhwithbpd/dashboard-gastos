import streamlit as st
import pandas as pd

from app.services.sheets_service import SheetsService
from app.data.processor import DataProcessor


st.set_page_config(
    page_title="Dashboard de Coletas",
    page_icon="🚚",
    layout="wide"
)


def format_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calculate_metrics(df: pd.DataFrame) -> dict:
    receita = df["valor_recebido_no_dia_r"].sum()
    gasto_total = df["gasto_total_r"].sum()
    lucro = receita - gasto_total
    total_coletas = df["coletas_realizadas"].sum()

    return {
        "receita_total": receita,
        "gasto_total": gasto_total,
        "lucro_total": lucro,
        "total_coletas": total_coletas,
        "ticket_medio_por_coleta": receita / total_coletas if total_coletas else 0,
        "custo_medio_por_coleta": gasto_total / total_coletas if total_coletas else 0,
    }


@st.cache_data(ttl=300)
def load_data():
    service = SheetsService()
    df = service.get_data()

    processor = DataProcessor(df)
    df_clean = processor.clean_data()

    return df_clean


st.title("🚚 Dashboard de Coletas")
st.caption("Controle financeiro das diárias, coletas e gastos operacionais.")

if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df.empty:
    st.warning("Nenhum dado encontrado na planilha.")
    st.stop()


# =========================
# Filtros
# =========================

df["mes"] = df["data"].dt.to_period("M").astype(str)

meses = sorted(df["mes"].dropna().unique(), reverse=True)

mes_selecionado = st.selectbox(
    "Filtrar por mês",
    options=["Todos"] + meses
)

if mes_selecionado != "Todos":
    df = df[df["mes"] == mes_selecionado]

if df.empty:
    st.warning("Nenhum registro encontrado para o filtro selecionado.")
    st.stop()

metrics = calculate_metrics(df)


# =========================
# Cards principais
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Receita Total", format_brl(metrics["receita_total"]))
col2.metric("Gasto Total", format_brl(metrics["gasto_total"]))

lucro = metrics["lucro_total"]
col3.metric(
    "Lucro Líquido",
    format_brl(lucro),
    delta="Positivo" if lucro >= 0 else "Negativo"
)

col4.metric("Total de Coletas", int(metrics["total_coletas"]))

col5, col6 = st.columns(2)

col5.metric(
    "Ticket Médio por Coleta",
    format_brl(metrics["ticket_medio_por_coleta"])
)

col6.metric(
    "Custo Médio por Coleta",
    format_brl(metrics["custo_medio_por_coleta"])
)


st.divider()


# =========================
# Resultado por dia
# =========================

st.subheader("📈 Resultado por dia")

resultado_dia = (
    df.groupby("data", as_index=False)
    .agg({
        "valor_recebido_no_dia_r": "sum",
        "gasto_total_r": "sum",
        "coletas_realizadas": "sum"
    })
)

resultado_dia["lucro"] = (
    resultado_dia["valor_recebido_no_dia_r"] - resultado_dia["gasto_total_r"]
)

st.line_chart(
    resultado_dia,
    x="data",
    y=["valor_recebido_no_dia_r", "gasto_total_r", "lucro"]
)


# =========================
# Gastos por categoria
# =========================

st.subheader("⛽ Gastos por categoria")

gastos_categoria = pd.DataFrame({
    "Categoria": ["Combustível", "Manutenção", "Pedágio"],
    "Valor": [
        df["gasto_combustivel_r"].sum(),
        df["gasto_manutencao_r"].sum(),
        df["gasto_pedagio_r"].sum()
    ]
})

st.bar_chart(gastos_categoria, x="Categoria", y="Valor")


# =========================
# Insights
# =========================

st.divider()
st.subheader("🧠 Insights")

melhor_dia = resultado_dia.loc[resultado_dia["lucro"].idxmax()]
pior_dia = resultado_dia.loc[resultado_dia["lucro"].idxmin()]

col7, col8 = st.columns(2)

col7.success(
    f"Melhor dia: {melhor_dia['data'].date()} — lucro de {format_brl(melhor_dia['lucro'])}"
)

col8.error(
    f"Pior dia: {pior_dia['data'].date()} — lucro de {format_brl(pior_dia['lucro'])}"
)


# =========================
# Tabela
# =========================

st.divider()
st.subheader("📋 Registros")

df_view = df.copy()

colunas_moeda = [
    "valor_recebido_no_dia_r",
    "gasto_combustivel_r",
    "gasto_manutencao_r",
    "gasto_pedagio_r",
    "gasto_total_r"
]

for col in colunas_moeda:
    if col in df_view.columns:
        df_view[col] = df_view[col].apply(format_brl)

st.dataframe(df_view, use_container_width=True)