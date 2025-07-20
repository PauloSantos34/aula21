import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

def carregar_emendas_local():
    try:
        df = pd.read_csv("emendas_parlamentares.csv", sep=';', encoding='utf-8')
        df = df[['idAutor', 'valorEmenda']].dropna()
        df['valorEmenda'] = df['valorEmenda'].astype(float)
        return df
    except Exception as e:
        print(f"Erro ao carregar emendas: {e}")
        return pd.DataFrame()

def carregar_proposicoes_local():
    try:
        df = pd.read_csv("proposicoes_legislativas.csv", sep=';', encoding='utf-8')
        df = df[['idAutor', 'idProposicao']].dropna()
        return df
    except Exception as e:
        print(f"Erro ao carregar proposições: {e}")
        return pd.DataFrame()

def analisar_eficiencia(emendas, proposicoes):
    print("\n📊 Análise de Eficiência dos Senadores (baseada em emendas x proposições):")
    
    gasto_por_senador = emendas.groupby('idAutor').sum().rename(columns={"valorEmenda": "total_emendas"})
    propostas_por_senador = proposicoes.groupby('idAutor').count().rename(columns={"idProposicao": "total_propostas"})

    eficiencia = gasto_por_senador.join(propostas_por_senador, how='inner')
    eficiencia['custo_por_proposta'] = eficiencia['total_emendas'] / eficiencia['total_propostas']
    eficiencia = eficiencia.sort_values('custo_por_proposta', ascending=False)

    print(tabulate(eficiencia.head(10), headers='keys', tablefmt='grid', floatfmt=".2f"))
    return eficiencia

def visualizar_distribuicao(eficiencia):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.histplot(eficiencia["custo_por_proposta"], bins=30, kde=True, color='green')
    plt.title("Distribuição do Custo por Proposição Legislativa")
    plt.xlabel("Custo (R$)")
    plt.ylabel("Número de Senadores")
    plt.tight_layout()
    plt.show()

def main():
    print("🔍 Carregando dados locais de emendas e proposições...")

    emendas = carregar_emendas_local()
    proposicoes = carregar_proposicoes_local()

    if emendas.empty or proposicoes.empty:
        print("⚠️ Dados não encontrados ou mal formatados.")
        return

    eficiencia = analisar_eficiencia(emendas, proposicoes)
    visualizar_distribuicao(eficiencia)

if __name__ == "__main__":
    main()