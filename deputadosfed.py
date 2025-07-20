# fazer esse mesmo código só que agora para os vereadores da Câmara Municipal de Niterói:
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import time

# Estilo visual
sns.set(style="whitegrid")
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# === 1. Obter lista de deputados federais em exercício
def get_deputados():
    url = f"{BASE_URL}/deputados?itens=100&ordem=ASC&ordenarPor=nome"
    r = requests.get(url)
    data = r.json()
    deputados = pd.DataFrame(data['dados'])
    return deputados[['id', 'nome', 'siglaPartido', 'siglaUf', 'email']]

# === 2. Obter quantidade de projetos de lei apresentados por cada deputado
def get_projetos_por_deputado(deputado_id):
    url = f"{BASE_URL}/proposicoes?autor={deputado_id}&siglaTipo=PL"
    r = requests.get(url)
    if r.status_code == 200:
        return len(r.json().get('dados', []))
    return 0

# === 3. Obter gastos da cota parlamentar
def get_gastos_por_deputado(deputado_id):
    url = f"{BASE_URL}/deputados/{deputado_id}/despesas?itens=100"
    r = requests.get(url)
    if r.status_code == 200:
        despesas = pd.DataFrame(r.json()['dados'])
        return despesas['valorDocumento'].sum()
    return 0

# === 4. Monta DataFrame com todas as informações
def montar_df_completo(limite=30):
    deputados = get_deputados().head(limite)
    lista = []

    for _, row in deputados.iterrows():
        print(f"Processando: {row['nome']}")
        time.sleep(0.5)
        projetos = get_projetos_por_deputado(row['id'])
        gastos = get_gastos_por_deputado(row['id'])

        lista.append({
            'Nome': row['nome'],
            'Partido': row['siglaPartido'],
            'UF': row['siglaUf'],
            'Projetos de Lei': projetos,
            'Gastos Cota Parlamentar (R$)': gastos,
            'Custo por Projeto (R$)': gastos / projetos if projetos else None
        })

    df_final = pd.DataFrame(lista)
    return df_final

# === 5. Gera Laudo/Parecer
def gerar_laudo(df):
    print("\n📋 LAUDO DE EFICIÊNCIA PARLAMENTAR:\n")
    for _, row in df.iterrows():
        if row['Projetos de Lei'] >= 20 and (row['Custo por Projeto (R$)'] is not None and row['Custo por Projeto (R$)'] < 10000):
            categoria = '🟢 Altamente Eficiente'
        elif row['Projetos de Lei'] <= 5 and row['Gastos Cota Parlamentar (R$)'] > 100000:
            categoria = '🔴 Gastos Elevados, Baixa Produção'
        elif row['Projetos de Lei'] == 0:
            categoria = '⚫ Inoperante'
        else:
            categoria = '🟡 Regular'

        custo = row['Custo por Projeto (R$)']
        custo_fmt = f"R$ {custo:.2f}" if pd.notnull(custo) else "N/A"

        print(f"{row['Nome']} ({row['UF']}/{row['Partido']}): {categoria} | Projetos: {row['Projetos de Lei']}, "
              f"Gasto: R$ {row['Gastos Cota Parlamentar (R$)']:.2f}, Custo/Projeto: {custo_fmt}")

# === 6. Visualizações e estatísticas
def analise_estatistica(df):
    print("\n📊 Resumo Estatístico:")
    print(tabulate(df.describe(include='all'), headers='keys', tablefmt='github'))

    print("\n💰 Top 5 - Mais Gastam:")
    print(tabulate(df.sort_values(by='Gastos Cota Parlamentar (R$)', ascending=False).head(5), headers='keys', tablefmt='github'))

    print("\n📜 Top 5 - Mais Projetos de Lei:")
    print(tabulate(df.sort_values(by='Projetos de Lei', ascending=False).head(5), headers='keys', tablefmt='github'))

    # Gráfico: Gastos vs Projetos
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Projetos de Lei', y='Gastos Cota Parlamentar (R$)', hue='UF')
    plt.title('Gastos x Projetos de Lei por Deputado')
    plt.xlabel('Projetos de Lei')
    plt.ylabel('Gastos (R$)')
    plt.tight_layout()
    plt.show()

    # Gráfico: Custo por Projeto
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Custo por Projeto (R$)'].dropna(), kde=True, bins=20)
    plt.title('Distribuição do Custo por Projeto de Lei')
    plt.xlabel('Custo por Projeto (R$)')
    plt.tight_layout()
    plt.show()

# === 7. Salvar o laudo em arquivo texto
def salvar_laudo_em_txt(df, caminho="laudo_deputados.txt"):
    with open(caminho, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            if row['Projetos de Lei'] >= 20 and (row['Custo por Projeto (R$)'] is not None and row['Custo por Projeto (R$)'] < 10000):
                categoria = '🟢 Altamente Eficiente'
            elif row['Projetos de Lei'] <= 5 and row['Gastos Cota Parlamentar (R$)'] > 100000:
                categoria = '🔴 Gastos Elevados, Baixa Produção'
            elif row['Projetos de Lei'] == 0:
                categoria = '⚫ Inoperante'
            else:
                categoria = '🟡 Regular'

            custo = row['Custo por Projeto (R$)']
            custo_fmt = f"R$ {custo:.2f}" if pd.notnull(custo) else "N/A"

            f.write(f"{row['Nome']} ({row['UF']}/{row['Partido']}): {categoria} | Projetos: {row['Projetos de Lei']}, "
                    f"Gasto: R$ {row['Gastos Cota Parlamentar (R$)']:.2f}, Custo/Projeto: {custo_fmt}\n")

# === 8. Separação e relatórios filtrados
def gerar_relatorios_filtrados(df):
    inoperantes = df[df['Projetos de Lei'] == 0]
    alto_custo_baixa_producao = df[(df['Projetos de Lei'] <= 5) & (df['Gastos Cota Parlamentar (R$)'] > 100000)]

    print("\n🔎 RELATÓRIO - DEPUTADOS INOPERANTES (0 projetos):")
    print(tabulate(inoperantes, headers='keys', tablefmt='fancy_grid', showindex=False))

    print("\n🔎 RELATÓRIO - GASTOS ELEVADOS COM BAIXA PRODUÇÃO (<=5 projetos e > R$100 mil):")
    print(tabulate(alto_custo_baixa_producao, headers='keys', tablefmt='fancy_grid', showindex=False))

    # Opcional: salvar os CSVs
    inoperantes.to_csv("inoperantes.csv", index=False)
    alto_custo_baixa_producao.to_csv("alto_custo_baixa_producao.csv", index=False)

    # Opcional: salvar como texto
    with open("relatorio_inoperantes.txt", "w", encoding="utf-8") as f:
        f.write(tabulate(inoperantes, headers='keys', tablefmt='grid'))

    with open("relatorio_alto_custo.txt", "w", encoding="utf-8") as f:
        f.write(tabulate(alto_custo_baixa_producao, headers='keys', tablefmt='grid'))

# === Execução Principal
if __name__ == "__main__":
    df = montar_df_completo(limite=30)  # Ajuste o limite conforme desejado
    analise_estatistica(df)
    gerar_laudo(df)
    gerar_relatorios_filtrados(df)
    # salvar_laudo_em_txt(df)  # Descomente para salvar o laudo completo