import pandas as pd
import unicodedata


class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def normalize_column_names(self, col: str) -> str:
        col = col.strip().lower()
        col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
        col = col.replace("(", "").replace(")", "").replace("$", "")
        col = col.replace("/", "_").replace(" ", "_")
        col = col.replace("__", "_")
        return col

    def parse_brl_value(self, value) -> float:
        if pd.isna(value) or value == "":
            return 0.0

        value = str(value).strip()

        if value in ["-", "None", "nan"]:
            return 0.0

        value = value.replace("R$", "").replace(" ", "")

        if "," in value:
            value = value.replace(".", "").replace(",", ".")
            return float(value)

        return float(value)

    def clean_data(self) -> pd.DataFrame:
        self.df.columns = [self.normalize_column_names(col) for col in self.df.columns]

        self.df["data"] = pd.to_datetime(
            self.df["data"],
            dayfirst=True,
            errors="coerce"
        )

        money_cols = [
            "valor_recebido_no_dia_r",
            "gasto_combustivel_r",
            "gasto_manutencao_r",
            "gasto_pedagio_r",
            "gasto_total_r",
        ]

        for col in money_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(self.parse_brl_value)

        if "coletas_realizadas" in self.df.columns:
            self.df["coletas_realizadas"] = pd.to_numeric(
                self.df["coletas_realizadas"],
                errors="coerce"
            ).fillna(0).astype(int)

        return self.df

    def calculate_metrics(self) -> dict:
        df = self.df

        receita = df["valor_recebido_no_dia_r"].sum()
        gasto_total = df["gasto_total_r"].sum()
        lucro = receita - gasto_total
        total_coletas = df["coletas_realizadas"].sum()

        return {
            "receita_total": receita,
            "gasto_total": gasto_total,
            "lucro_total": lucro,
            "total_coletas": total_coletas,
            "ticket_medio_por_coleta": receita / total_coletas if total_coletas > 0 else 0,
            "custo_medio_por_coleta": gasto_total / total_coletas if total_coletas > 0 else 0,
        }

    def format_brl(self, value: float) -> str:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")