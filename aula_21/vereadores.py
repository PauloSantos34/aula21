import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import pytesseract
from PIL import Image
import re
import os

# === Estilo dos gráficos
sns.set(style="whitegrid")

# === 0. OCR da imagem com salários
def extrair_salarios_da_imagem(imagem_path):
    if not os.path.exists(imagem_path):
        print(f"❌ Caminho da imagem não encontrado: {imagem_path}")
        return 0

    imagem = Image.open(imagem_path)
    texto = pytesseract.image_to_string(imagem, lang='por')

    print("📄 Texto extraído da imagem:")
    print(texto)

    # Extrair valores monetários
    valores = re.findall(r'R?\$?\s?([\d\.]+,\d{2})', texto)

    def moeda_para_float(valor):
        return float(valor.replace('.', '').replace(',', '.'))

    valores_float = [moeda_para_float(v) for v in valores]
    soma_total = sum(valores_float)

    print(f"\n💰 Total estimado dos salários encontrados: R$ {soma_total:,.2f}")
    return soma_total

# === 1. Carregar os dados dos vereadores
def carregar_dados_produtividade(caminho_csv="produtividade_vereadores.csv"):
    return pd.read_csv(caminho_csv)

def carregar_dados_gastos(caminho_csv="gastos_vereadores.csv"):
    return pd.read_csv(caminho_csv)

# === 2. Montar DataFrame final
def montar_df_completo(produtividade_df, gastos_df):
    df = produtividade_df.merge(gastos_df, on='Nome', how='left')
    df['Custo por Projeto (R$)'] = df.apply(
        lambda row: row['Gastos Totais (R$)'] / row['Projetos de Lei']
        if row['Projetos de Lei'] > 0 else None, axis=1)
    return df

# === 3. Laudo
def gerar_laudo(df):
    print("\n📋 LAUDO DE EFICIÊNCIA PARLAMENTAR - VEREADORES DE NITERÓI:\n")
    for _, row in df.iterrows():
        if row['Projetos de Lei'] >= 20 and pd.notnull(row['Custo por Projeto (R$)']) and row['Custo por Projeto (R$)'] < 10000:
            categoria = '🟢 Altamente Eficiente'
        elif row['Projetos de Lei'] <= 5 and row['Gastos Totais (R$)'] > 100000:
            categoria = '🔴 Gastos Elevados, Baixa Produção'
        elif row['Projetos de Lei'] == 0:
            categoria = '⚫ Inoperante'
        else:
            categoria = '🟡 Regular'

        custo_fmt = f"R$ {row['Custo por Projeto (R$)']:.2f}" if pd.notnull(row['Custo por Projeto (R$)']) else "N/A"

        print(f"{row['Nome']} ({row['Partido']}): {categoria} | Projetos: {row['Projetos de Lei']}, "
              f"Gasto: R$ {row['Gastos Totais (R$)']:.2f}, Custo/Projeto: {custo_fmt}")

# === 4. Análise Estatística
def analise_estatistica(df):
    print("\n📊 Resumo Estatístico:")
    print(tabulate(df.describe(include='all'), headers='keys', tablefmt='github', showindex=False))

    print("\n💰 Top 5 - Mais Gastam:")
    print(tabulate(df.sort_values(by='Gastos Totais (R$)', ascending=False).head(5), headers='keys', tablefmt='github', showindex=False))

    print("\n📜 Top 5 - Mais Projetos de Lei:")
    print(tabulate(df.sort_values(by='Projetos de Lei', ascending=False).head(5), headers='keys', tablefmt='github', showindex=False))

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Projetos de Lei', y='Gastos Totais (R$)', hue='Partido')
    plt.title('Gastos x Projetos de Lei por Vereador')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(df['Custo por Projeto (R$)'].dropna(), kde=True)
    plt.title('Distribuição do Custo por Projeto')
    plt.tight_layout()
    plt.show()

# === 5. Relatórios específicos
def gerar_relatorios_filtrados(df):
    inoperantes = df[df['Projetos de Lei'] == 0]
    alto_custo = df[(df['Projetos de Lei'] <= 5) & (df['Gastos Totais (R$)'] > 100000)]

    print("\n🔎 RELATÓRIO - VEREADORES INOPERANTES:")
    print(tabulate(inoperantes, headers='keys', tablefmt='fancy_grid', showindex=False))

    print("\n🔎 RELATÓRIO - GASTOS ELEVADOS COM BAIXA PRODUÇÃO:")
    print(tabulate(alto_custo, headers='keys', tablefmt='fancy_grid', showindex=False))

# === Execução Principal
if __name__ == "__main__":
    # 0. OCR da imagem dos salários
    imagem_salarios = "/mnt/data/53790c08-a5b8-4ba4-9c53-3fda1d450c9d.png"
    total_salarios = extrair_salarios_da_imagem(imagem_salarios)

    # 1. Carregamento de dados CSV
    try:
        produtividade = carregar_dados_produtividade()
        gastos = carregar_dados_gastos()
    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {e}")
        exit(1)

    # 2. Análise combinada
    df_final = montar_df_completo(produtividade, gastos)

    # 3. Execução das análises
    analise_estatistica(df_final)
    gerar_laudo(df_final)
    gerar_relatorios_filtrados(df_final)