import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import time
import json

with open("despesas_ceaps_senadores.json", encoding="utf-8") as f:
    dados = json.load(f)

for despesa in dados:
    print(f"\nSenador/Fornecedor: {despesa['fornecedor']} - Valor Total: {despesa['valor']:.2f}")
    
    if 'objetos' in despesa:
        for obj in despesa['objetos']:
            print(f"  → {obj['descricaoObjeto']} ({obj['quantidade']} x {obj['valorUnitario']:.2f}) = {obj['valorTotal']:
sns.set(style="whitegrid")

# === 1. Obter lista de senadores
def get_senadores():
    url = "https://legis.senado.leg.br/dadosabertos/senador/lista/atual.json"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    parlamentares = data['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']
    
    lista = []
    for p in parlamentares:
        dados = p.get('IdentificacaoParlamentar', {})
        lista.append({
            'CodigoParlamentar': int(dados.get('CodigoParlamentar', 0)),
            'NomeParlamentar': dados.get('NomeParlamentar', 'Desconhecido'),
            'SiglaPartido': dados.get('SiglaPartido', 'Indefinido'),
            'UF': dados.get('Uf', 'ND')
        })
    return pd.DataFrame(lista)

# === 2. Obter projetos apresentados por senador
def get_projetos_senador(codigo):
    url = f"https://legis.senado.leg.br/dadosabertos/senador/{codigo}/autorias"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            try:
                dados = r.json().get('AutoriaMateria', {}).get('Materias', {}).get('Materia', [])
                return len(dados)
            except ValueError:
                print(f"❌ Erro ao decodificar JSON para senador {codigo}")
                return 0
        else:
            print(f"❌ Erro {r.status_code} ao acessar URL de projetos para {codigo}")
            return 0
    except requests.exceptions.RequestException as e:
        print(f"❌ Falha de conexão para o senador {codigo}: {e}")
        return 0
# === 3. Gastos com CEAPS (últimos 12 meses, por exemplo)
def get_gastos_ceaps(codigo):
    url = f"https://legis.senado.leg.br/dadosabertos/senador/{codigo}/gastos"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        despesas = data.get("GastosParlamentares", {}).get("GastoParlamentar", [])
        df = pd.DataFrame(despesas)
        if not df.empty and 'ValorReembolso' in df.columns:
            df['ValorReembolso'] = df['ValorReembolso'].astype(float)
            return df['ValorReembolso'].sum()
    return 0.0

# === 4. Montar DataFrame final
def montar_df_senadores():
    senadores = get_senadores()
    lista = []

    for _, row in senadores.iterrows():
        print(f"Processando: {row['NomeParlamentar']}")
        time.sleep(0.5)
        projetos = get_projetos_senador(row['CodigoParlamentar'])
        gastos = get_gastos_ceaps(row['CodigoParlamentar'])
        lista.append({
            'Nome': row['NomeParlamentar'],
            'Partido': row['SiglaPartido'],
            'UF': row['UF'],
            'Projetos de Lei': projetos,
            'Gastos Cota Parlamentar (R$)': gastos,
            'Custo por Projeto (R$)': gastos / projetos if projetos else None
        })

    return pd.DataFrame(lista)

# === 5. Análise estatística
def analise_estatistica(df):
    print("\nResumo Estatístico:")
    print(tabulate(df.describe(include='all'), headers='keys', tablefmt='github'))

    print("\nTop 5 - Mais Gastam:")
    print(tabulate(df.sort_values(by='Gastos Cota Parlamentar (R$)', ascending=False).head(5), headers='keys', tablefmt='github'))

    print("\nTop 5 - Mais Projetos de Lei:")
    print(tabulate(df.sort_values(by='Projetos de Lei', ascending=False).head(5), headers='keys', tablefmt='github'))

    # Gráfico: Gastos vs Projetos
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Projetos de Lei', y='Gastos Cota Parlamentar (R$)', hue='UF')
    plt.title('Gastos x Projetos de Lei por Senador')
    plt.xlabel('Projetos de Lei')
    plt.ylabel('Gastos (R$)')
    plt.tight_layout()
    plt.show()

    # Gráfico: Custo por Projeto
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Custo por Projeto (R$)'].dropna(), kde=True)
    plt.title('Distribuição do Custo por Projeto de Lei')
    plt.xlabel('Custo por Projeto (R$)')
    plt.tight_layout()
    plt.show()

# === 6. Geração de parecer
def gerar_laudo(df):
    print("\n🔍 PARECER FINAL SOBRE SENADORES:\n")
    for _, row in df.iterrows():
        if row['Projetos de Lei'] >= 20 and row['Custo por Projeto (R$)'] and row['Custo por Projeto (R$)'] < 10000:
            categoria = '🟢 Altamente Eficiente'
        elif row['Projetos de Lei'] <= 5 and row['Gastos Cota Parlamentar (R$)'] > 100000:
            categoria = '🔴 Gastos Elevados, Baixa Produção'
        elif row['Projetos de Lei'] == 0:
            categoria = '⚫ Inoperante'
        else:
            categoria = '🟡 Regular'

        custo_str = f"R$ {row['Custo por Projeto (R$)']:.2f}" if row['Custo por Projeto (R$)'] else "N/A"
        print(f"{row['Nome']} ({row['UF']}/{row['Partido']}): {categoria} | Projetos: {row['Projetos de Lei']}, Gasto: R$ {row['Gastos Cota Parlamentar (R$)']:.2f}, Custo/Projeto: {custo_str}")

# === Execução principal
if __name__ == "__main__":
    df_sen = montar_df_senadores()
    analise_estatistica(df_sen)
    gerar_laudo(df_sen)