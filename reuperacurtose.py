import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, norm

def exibir_tabela(dados, headers, titulo=None):
    if titulo:
        print(f"\n{titulo}")
    print(tabulate(dados, headers=headers, tablefmt="grid", floatfmt=".2f"))

try:
    print("Obtendo dados...")
    URL = "https://www.ispdados.rj.gov.br/Arquivos/UppEvolucaoMensalDetitulos.csv"
    df = pd.read_csv(URL, sep=';', encoding='iso-8859-1')
    df = df[['upp', 'recuperacao_veiculos']]
    df_total = df.groupby('upp', as_index=False).sum(numeric_only=True)
    exibir_tabela(df_total.head(), headers='keys', titulo="Dados iniciais (TOP 5 UPPs)")
except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()

try:
    print("\nCalculando estatísticas...")

    valores = df_total['recuperacao_veiculos'].to_numpy()

    media = np.mean(valores)
    mediana = np.median(valores)
    distancia = abs((media - mediana) / mediana)

    q1, q2, q3 = np.quantile(valores, [0.25, 0.50, 0.75])
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr
    minimo = np.min(valores)
    maximo = np.max(valores)
    amplitude_total = maximo - minimo

    assimetria = skew(valores)
    curtose_val = kurtosis(valores)

    outliers_inf = df_total[df_total['recuperacao_veiculos'] < limite_inf]
    outliers_sup = df_total[df_total['recuperacao_veiculos'] > limite_sup]

    exibir_tabela([
        ["Média", media],
        ["Mediana", mediana],
        ["Distância relativa (média-mediana)", distancia]
    ], headers=["Métrica", "Valor"], titulo="Medidas de tendência central")

    exibir_tabela([
        ["Q1", q1],
        ["Q2 (Mediana)", q2],
        ["Q3", q3],
        ["IQR (Q3 - Q1)", iqr]
    ], headers=["Quartil", "Valor"], titulo="Quartis e IQR")

    exibir_tabela([
        ["Limite Inferior", limite_inf],
        ["Valor Mínimo", minimo],
        ["Valor Máximo", maximo],
        ["Limite Superior", limite_sup],
        ["Amplitude Total", amplitude_total]
    ], headers=["Extremos", "Valor"], titulo="Valores Extremos e Limites de Outliers")

    exibir_tabela([
        ["Assimetria", assimetria],
        ["Curtose", curtose_val]
    ], headers=["Medida", "Valor"], titulo="Assimetria e Curtose")

    df_desc = df_total.sort_values(by='recuperacao_veiculos', ascending=False).reset_index(drop=True)
    exibir_tabela(df_desc, headers='keys', titulo="Ranqueamento das UPPs - Ordem Decrescente (Maior para Menor)")

except Exception as e:
    print(f"Erro ao obter informações estatísticas: {e}")
    exit()

# GRÁFICOS - Parte 1
try:
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Análise Estatística das Recuperações de Veículos por UPP', fontsize=16)

    # Gráfico 1 - Barras (Top 10 UPPs)
    top10 = df_desc.head(10)
    axs[0, 0].barh(top10['upp'], top10['recuperacao_veiculos'], color='steelblue')
    axs[0, 0].invert_yaxis()
    axs[0, 0].set_title('Top 10 UPPs - Recuperações de Veículos')
    axs[0, 0].set_xlabel('Quantidade')

    # Gráfico 2 - Texto estatístico
    axs[0, 1].axis('off')
    texto_estatisticas = f"""
    Média: {media:.2f}
    Mediana: {mediana:.2f}
    Distância (média-mediana): {distancia:.4f}
    Q1: {q1:.2f}
    Q3: {q3:.2f}
    IQR: {iqr:.2f}
    Mínimo: {minimo}
    Máximo: {maximo}
    Limite Inf: {limite_inf:.2f}
    Limite Sup: {limite_sup:.2f}
    Amplitude Total: {amplitude_total}
    Assimetria: {assimetria:.4f}
    Curtose: {curtose_val:.4f}
    """
    axs[0, 1].text(0.1, 0.5, texto_estatisticas, fontsize=10, va='center')

    # Gráfico 3 - Pizza (Top 5 UPPs)
    top5 = df_desc.head(5)
    axs[1, 0].pie(top5['recuperacao_veiculos'], labels=top5['upp'], autopct='%1.1f%%', startangle=140)
    axs[1, 0].set_title('Top 5 UPPs - Participação nas Recuperações')

    # Gráfico 4 - Boxplot
    axs[1, 1].boxplot(valores, vert=False, patch_artist=True,
                      boxprops=dict(facecolor='lightblue', color='black'),
                      medianprops=dict(color='red'))
    axs[1, 1].set_title('Boxplot - Recuperações de Veículos')
    axs[1, 1].set_xlabel('Quantidade')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

except Exception as e:
    print(f"Erro ao gerar gráficos (parte 1): {e}")

# GRÁFICOS - Parte 2: Assimetria e Curtose
try:
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle('Distribuição, Assimetria e Curtose da Recuperação de Veículos:', fontsize=16)

    # Histograma com densidade (Assimetria)
    axs2[0].hist(valores, bins=15, color='lightgreen', edgecolor='black', density=True, alpha=0.6)
    xmin, xmax = axs2[0].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, media, np.std(valores))
    axs2[0].plot(x, p, 'k', linewidth=2)
    axs2[0].set_title(f'Histograma com Curva Normal\nAssimetria: {assimetria:.2f}')

    # Densidade + Comparação de curtose
    axs2[1].violinplot(valores, showmeans=True, showmedians=True)
    axs2[1].set_title(f'Curtose: {curtose_val:.2f}')
    axs2[1].set_ylabel('Recuperações')

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro ao gerar gráficos (parte 2): {e}")
