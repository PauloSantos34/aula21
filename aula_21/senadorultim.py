import chardet
import pandas as pd
import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# constantes
SUBSIDIO_MENSAL = 46366.19
URL_GASTOS = "https://www12.senado.leg.br/dados-abertos/senadores/ceaps-2022.csv"
URL_PRODUTIVIDADE = "https://www12.senado.leg.br/dados-abertos/senadores/projetos-2022.csv"

def detectar_codificacao_bytes(content_bytes):
    return chardet.detect(content_bytes[:10000])['encoding']

def baixar_csv(url):
    print(f"🔻 Baixando: {url}")
    r = requests.get(url)
    r.raise_for_status()
    return r.content

def ler_csv_bytes(content):
    encoding = detectar_codificacao_bytes(content)
    return pd.read_csv(pd.io.common.BytesIO(content), sep=None, engine='python', encoding=encoding)

def tratar_gastos(df):
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={"senador":"nome","valor_despesa":"valor"}, inplace=True)
    df = df[df["valor"].notna()]
    df["valor"] = (
        df["valor"].astype(str)
        .str.replace(",",".")
        .str.replace("r\\$","", regex=True)
        .astype(float)
    )
    df["nome"] = df["nome"].str.title().str.strip()
    return df[["nome","valor"]]

def tratar_produtividade(df):
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={"autor_principal":"nome"}, inplace=True)
    df["nome"] = df["nome"].str.title().str.strip()
    df = df[df["ano_apresentacao"]==2022]
    count = df.groupby("nome").size().reset_index(name="num_projetos")
    return count

def cruzar_e_analisar(df_g, df_p):
    g = df_g.groupby("nome")["valor"].sum().reset_index()
    df = pd.merge(g, df_p, how="left", on="nome").fillna(0)
    df["custo_por_projeto"] = df["valor"] / df["num_projetos"].replace(0, pd.NA)
    df["eficiencia_financeira_%"] = 100 * (1 - (df["valor"] / SUBSIDIO_MENSAL)).clip(lower=0)
    df.sort_values("valor", ascending=False, inplace=True)
    print("\n📊 Top 10 Senadores — cruzamento:")
    print(tabulate(df.head(10), headers="keys", floatfmt=".2f"))
    return df

def visualizar(df):
    plt.figure(figsize=(10,6))
    sns.scatterplot(
        data=df,
        x="num_projetos",
        y="valor",
        size="eficiencia_financeira_%",
        sizes=(50,300),
        legend=False
    )
    plt.title("Gastos vs nº de projetos (tamanho da bolha = eficiência)")
    plt.xlabel("Projetos Apresentados (2022)")
    plt.ylabel("Gasto Total (R$)")
    plt.tight_layout()
    plt.show()

def gerar_laudo(df):
    n = df.shape[0]
    print("\n📋 Laudo Final:")
    print(f"- Senadores analisados: {n}")
    print(f"- Média de projetos: {df['num_projetos'].mean():.1f}")
    print(f"- Média de custo por projeto: R$ {df['custo_por_projeto'].dropna().mean():.2f}")
    print(f"- Média de eficiência financeira: {df['eficiencia_financeira_%'].mean():.2f}%")

    if df['eficiencia_financeira_%'].mean() >= 70:
        print("✅ Em média, os senadores estão sendo financeiramente eficientes.")
    else:
        print("⚠️ Eficiência financeira abaixo do ideal; avaliar qualidade dos resultados.")

def main():
    os.makedirs("data", exist_ok=True)

    # 1. Gastos
    bin_g = baixar_csv(URL_GASTOS)
    df_g = ler_csv_bytes(bin_g)
    df_g = tratar_gastos(df_g)

    # 2. Produtividade
    bin_p = baixar_csv(URL_PRODUTIVIDADE)
    df_p = ler_csv_bytes(bin_p)
    df_p = tratar_produtividade(df_p)

    # 3. Cruzamento e análise
    df = cruzar_e_analisar(df_g, df_p)

    # 4. Visualização e laudo
    visualizar(df)
    gerar_laudo(df)

if __name__ == "__main__":
    main()
