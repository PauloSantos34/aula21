import chardet
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

def detectar_codificacao(file_path, n_bytes=10000):
    with open(file_path, 'rb') as f:
        rawdata = f.read(n_bytes)
    result = chardet.detect(rawdata)
    return result['encoding']

def ler_csv_com_melhor_separador(file_path):
    encoding = detectar_codificacao(file_path)
    try:
        df = pd.read_csv(file_path, sep=';', encoding=encoding)
    except:
        df = pd.read_csv(file_path, sep=',', encoding=encoding)
    return df

def limpar_e_padronizar(df, nome_arquivo):
    df.columns = df.columns.str.strip().str.lower()
    print(f"\nColunas detectadas em {nome_arquivo}: {list(df.columns)}")

    # Identifica a coluna com o nome do senador
    col_nome = next((col for col in df.columns if "senador" in col or "parlamentar" in col or "nome" in col), None)
    if not col_nome:
        raise ValueError(f"Coluna de nome do senador/parlamentar não encontrada no arquivo {nome_arquivo}")
    
    df.rename(columns={col_nome: "nome"}, inplace=True)

    # Identifica coluna de valor
    col_valor = next((col for col in df.columns if "valor" in col and "liquid" in col), None)
    if not col_valor:
        col_valor = next((col for col in df.columns if "valor" in col), None)
    if not col_valor:
        raise ValueError(f"Coluna de valor não encontrada no arquivo {nome_arquivo}")

    df.rename(columns={col_valor: "valor_liquidado"}, inplace=True)

    df = df[df["valor_liquidado"].notna()]
    df["valor_liquidado"] = (
        df["valor_liquidado"]
        .astype(str)
        .str.replace(",", ".")
        .str.replace("R\\$", "", regex=True)
        .str.replace(" ", "")
        .astype(float)
    )
    
    df["nome"] = df["nome"].astype(str).str.strip().str.title()
    return df[["nome", "valor_liquidado"]]

def agrupar_e_analisar(df):
    agrupado = df.groupby("nome")["valor_liquidado"].agg(["sum", "mean", "std", "count"]).reset_index()
    agrupado = agrupado.sort_values("sum", ascending=False)

    print("\nResumo por Senador:")
    print(tabulate(agrupado.head(10), headers="keys", showindex=False, floatfmt=".2f"))

    print("\nEstatísticas Gerais:")
    print(df["valor_liquidado"].describe())

    return agrupado

def visualizar_dados(agrupado):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=agrupado.head(10), x="sum", y="nome", palette="viridis")
    plt.title("Top 10 Senadores por Gasto Total")
    plt.xlabel("Gasto Total (R$)")
    plt.ylabel("Senador")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))
    sns.boxplot(x=agrupado["sum"])
    plt.title("Distribuição dos Gastos Totais por Senador")
    plt.xlabel("Gasto Total (R$)")
    plt.tight_layout()
    plt.show()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = ["despesas_institucional.csv", "gastos_ceaps_2022.csv"]
    
    dfs = []
    for arquivo in arquivos:
        path = os.path.join(base_dir, arquivo)
        if not os.path.exists(path):
            print(f"Arquivo não encontrado: {arquivo}")
            continue
        print(f"\nLendo: {arquivo}")
        df = ler_csv_com_melhor_separador(path)
        try:
            df_limpo = limpar_e_padronizar(df, arquivo)
            dfs.append(df_limpo)
        except Exception as e:
            print(f"Erro ao limpar {arquivo}: {e}")

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        agrupado = agrupar_e_analisar(df_total)
        visualizar_dados(agrupado)
    else:
        print("Nenhum dado válido encontrado.")

if __name__ == "__main__":
    main()
