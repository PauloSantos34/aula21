import chardet
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

SUBSIDIO_MENSAL = 46366.19

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

    # Identifica a coluna do nome
    col_nome = next((col for col in df.columns if "senador" in col), None)
    if not col_nome:
        raise ValueError(f"Coluna de nome do senador não encontrada em {nome_arquivo}")
    df.rename(columns={col_nome: "nome"}, inplace=True)

    # Identifica a coluna de valor
    col_valor = next((col for col in df.columns if "valor" in col), None)
    if not col_valor:
        raise ValueError(f"Coluna de valor não encontrada em {nome_arquivo}")
    df.rename(columns={col_valor: "valor_despesa"}, inplace=True)

    # Trata valores
    df = df[df["valor_despesa"].notna()]
    df["valor_despesa"] = (
        df["valor_despesa"]
        .astype(str)
        .str.replace(",", ".")
        .str.replace("R\\$", "", regex=True)
        .str.replace(" ", "")
        .astype(float)
    )
    df["nome"] = df["nome"].astype(str).str.strip().str.title()

    return df[["nome", "valor_despesa"]]

def agrupar_e_analisar(df):
    agrupado = df.groupby("nome")["valor_despesa"].agg(
        total_gasto="sum",
        gasto_medio="mean",
        gasto_desvio="std",
        num_despesas="count"
    ).reset_index()

    agrupado["eficiencia_financeira_%"] = 100 * (1 - (agrupado["total_gasto"] / SUBSIDIO_MENSAL))
    agrupado["eficiencia_financeira_%"] = agrupado["eficiencia_financeira_%"].clip(lower=0)

    agrupado = agrupado.sort_values("total_gasto", ascending=False)

    print("\n📊 Resumo por Senador (Top 10):")
    print(tabulate(agrupado.head(10), headers="keys", showindex=False, floatfmt=".2f"))

    print("\n📈 Estatísticas Gerais:")
    print(df["valor_despesa"].describe())

    return agrupado

def visualizar_dados(agrupado):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=agrupado.head(10), x="total_gasto", y="nome", palette="crest")
    plt.title("Top 10 Senadores por Gasto Total")
    plt.xlabel("Gasto Total (R$)")
    plt.ylabel("Senador")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))
    sns.boxplot(x=agrupado["total_gasto"])
    plt.title("Distribuição dos Gastos Totais por Senador")
    plt.xlabel("Gasto Total (R$)")
    plt.tight_layout()
    plt.show()

def gerar_laudo_final(agrupado):
    media_gasto = agrupado["total_gasto"].mean()
    media_eficiencia = agrupado["eficiencia_financeira_%"].mean()

    print("\n📋 Laudo Final:")
    print(f"🧾 Gasto médio dos senadores analisados: R$ {media_gasto:.2f}")
    print(f"📉 Eficiência financeira média (em relação ao subsídio de R$ {SUBSIDIO_MENSAL:.2f}): {media_eficiencia:.2f}%")

    if media_eficiencia >= 70:
        print("✅ Os senadores, em média, estão sendo financeiramente eficientes no uso da verba pública.")
    elif 40 <= media_eficiencia < 70:
        print("⚠️ A eficiência financeira é moderada. Recomenda-se análise mais aprofundada de resultados entregues.")
    else:
        print("❌ Os dados indicam baixa eficiência no uso dos recursos. Pode haver desperdício ou má gestão.")

    print("\n📣 Recomendação: Cruzar os gastos com indicadores de produtividade legislativa (projetos apresentados, relatórios, presenças) para avaliar a **eficácia** e **transparência real** da atuação parlamentar.")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = ["despesas_institucional.csv", "gastos_ceaps_2022.csv"]

    dfs = []
    for arquivo in arquivos:
        path = os.path.join(base_dir, arquivo)
        if not os.path.exists(path):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            continue
        print(f"\n📥 Lendo: {arquivo}")
        df = ler_csv_com_melhor_separador(path)
        try:
            df_limpo = limpar_e_padronizar(df, arquivo)
            dfs.append(df_limpo)
        except Exception as e:
            print(f"⚠️ Erro ao limpar {arquivo}: {e}")

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        agrupado = agrupar_e_analisar(df_total)
        visualizar_dados(agrupado)
        gerar_laudo_final(agrupado)
    else:
        print("⚠️ Nenhum dado válido encontrado.")

if __name__ == "__main__":
    main()