import chardet
import pandas as pd
import os
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Subsídio e URLs de Dados Abertos
SUBSIDIO_MENSAL = 46366.19
URL_GASTOS = "https://seu_servidor/despesas_institucional.csv"
URL_PRODUTIVIDADE = "https://dadosabertos.senado.gov.br/dataset/xyz-projetos.csv"

def detectar_codificacao(file_path_or_bytes, n_bytes=10000):
    raw = file_path_or_bytes if isinstance(file_path_or_bytes, bytes) else open(file_path_or_bytes,'rb').read(n_bytes)
    return chardet.detect(raw)['encoding']

def baixar_csv(url):
    print(f"🔻 Baixando {url}")
    r = requests.get(url)
    r.raise_for_status()
    return r.content

def ler_csv_conteudo(content):
    enc = detectar_codificacao(content)
    df = pd.read_csv(pd.io.common.BytesIO(content), sep=None, engine='python', encoding=enc)
    return df

# A – LEITURA E TRATAMENTO DE GASTOS
def tratar_gastos(df):
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={"senador":"nome","valor_despesa":"valor"}, inplace=True)
    df = df[df["valor"].notna()]
    df["valor"] = df["valor"].astype(str).str.replace(",",".").str.replace("r\\$","",regex=True).astype(float)
    df["nome"] = df["nome"].str.title().str.strip()
    return df[["nome","valor"]]

# B – LEITURA E TRATAMENTO DE PRODUTIVIDADE
def tratar_produtividade(df):
    df.columns = df.columns.str.strip().str.lower()
    df.rename(columns={
        "autor_principal":"nome",
        "ano_apresentacao":"ano",
        "sigla_tipo_materia":"tipo"
    }, inplace=True)
    df = df[df["ano"]==2022]
    df["nome"] = df["nome"].str.title().str.strip()
    return df.groupby("nome").size().reset_index(name="num_projetos")

# C – ANÁLISE E CRUZAMENTO
def cruzar_e_analisar(df_gastos, df_prod):
    g = df_gastos.groupby("nome")["valor"].sum().reset_index()
    df = pd.merge(g, df_prod, how="left", on="nome").fillna(0)
    df["custo_por_projeto"] = df["valor"] / df["num_projetos"].replace(0, pd.NA)
    df["eficiencia_financeira_%"] = 100*(1 - df["valor"]/SUBSIDIO_MENSAL).clip(lower=0)
    df.sort_values("valor", ascending=False, inplace=True)
    print(tabulate(df.head(10), headers="keys", floatfmt=".2f"))
    return df

# D – VISUALIZAÇÕES
def visualizar(df):
    plt.figure(figsize=(12,6))
    sns.scatterplot(df, x="num_projetos", y="valor", size="eficiencia_financeira_%", legend=False, sizes=(50,200))
    plt.title("Gastos x Projetos (bolha ~ eficiência)")
    plt.xlabel("Número de Projetos em 2022")
    plt.ylabel("Gasto Total (R$)")
    plt.tight_layout(); plt.show()

# Main
def main():
    # Gastos
    content_g = baixar_csv(URL_GASTOS)
    df_g = tratar_gastos(ler_csv_conteudo(content_g))
    # Produtividade
    content_p = baixar_csv(URL_PRODUTIVIDADE)
    df_p = tratar_produtividade(ler_csv_conteudo(content_p))
    # Cruzamento
    df = cruzar_e_analisar(df_g, df_p)
    visualizar(df)
    # Laudo:
    print(f"\nMédia de projetos: {df['num_projetos'].mean():.1f}")
    print(f"Média custo por projeto: R$ {df['custo_por_projeto'].mean():.2f}")

if __name__=="__main__":
    main()
