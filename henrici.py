import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, norm

def exibir_tabela(dados, headers, titulo=None):
    if titulo: print(f"\n{titulo}")
    print(tabulate(dados, headers=headers, tablefmt="grid", floatfmt=".2f"))

try:
    print("Obtendo dados...")
    df = pd.read_csv("https://www.ispdados.rj.gov.br/Arquivos/UppEvolucaoMensalDetitulos.csv",
                     sep=';', encoding='iso-8859-1')[['upp', 'recuperacao_veiculos']]
    df_total = df.groupby('upp', as_index=False).sum(numeric_only=True)
    exibir_tabela(df_total.head(), headers='keys', titulo="Dados iniciais (TOP 5 UPPs)")
except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()

try:
    print("\nCalculando estatísticas...")
    v = df_total['recuperacao_veiculos'].to_numpy()
    media, mediana = np.mean(v), np.median(v)
    q1, q2, q3 = np.quantile(v, [0.25, 0.5, 0.75])
    iqr, dist, minimo, maximo = q3 - q1, abs((media - mediana)/mediana), v.min(), v.max()
    lim_inf, lim_sup, amplitude = q1 - 1.5*iqr, q3 + 1.5*iqr, maximo - minimo
    assimetria, curt = skew(v), kurtosis(v)

    exibir_tabela([["Média", media], ["Mediana", mediana], ["Distância (média-mediana)", dist]],
                  headers=["Métrica", "Valor"], titulo="Medidas de tendência central")
    exibir_tabela([["Q1", q1], ["Q2 (Mediana)", q2], ["Q3", q3], ["IQR", iqr]],
                  headers=["Quartil", "Valor"], titulo="Quartis e IQR")
    exibir_tabela([["Limite Inferior", lim_inf], ["Mínimo", minimo], ["Máximo", maximo],
                   ["Limite Superior", lim_sup], ["Amplitude Total", amplitude]],
                  headers=["Extremos", "Valor"], titulo="Limites e Extremos")
    exibir_tabela([["Assimetria", assimetria], ["Curtose", curt]],
                  headers=["Medida", "Valor"], titulo="Assimetria e Curtose")

    df_desc = df_total.sort_values(by='recuperacao_veiculos', ascending=False).reset_index(drop=True)
    exibir_tabela(df_desc, headers='keys', titulo="Ranqueamento das UPPs - Ordem Decrescente")

except Exception as e:
    print(f"Erro ao obter informações estatísticas: {e}")
    exit()

# GRÁFICOS - Parte 1
try:
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Análise Estatística das Recuperações de Veículos por UPP', fontsize=16)

    top10 = df_desc.head(10)
    axs[0, 0].barh(top10['upp'], top10['recuperacao_veiculos'], color='steelblue')
    axs[0, 0].invert_yaxis(); axs[0, 0].set_title('Top 10 UPPs'); axs[0, 0].set_xlabel('Quantidade')

    axs[0, 1].axis('off')
    stats_txt = f"""Média: {media:.2f}
Mediana: {mediana:.2f}
Distância: {dist:.4f}
Q1: {q1:.2f}
Q3: {q3:.2f}
IQR: {iqr:.2f}
Min: {minimo}
Max: {maximo}
Lim Inf: {lim_inf:.2f}
Lim Sup: {lim_sup:.2f}
Amplitude: {amplitude}
Assimetria: {assimetria:.4f}
Curtose: {curt:.4f}"""
    axs[0, 1].text(0.1, 0.5, stats_txt, fontsize=10, va='center')

    top5 = df_desc.head(5)
    axs[1, 0].pie(top5['recuperacao_veiculos'], labels=top5['upp'],
                 autopct='%1.1f%%', startangle=140)
    axs[1, 0].set_title('Top 5 - Participação nas Recuperações')

    axs[1, 1].boxplot(v, vert=False, patch_artist=True,
                      boxprops=dict(facecolor='lightblue', color='black'),
                      medianprops=dict(color='red'))
    axs[1, 1].set_title('Boxplot'); axs[1, 1].set_xlabel('Quantidade')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]); plt.show()
except Exception as e:
    print(f"Erro ao gerar gráficos (parte 1): {e}")

# GRÁFICOS - Parte 2
try:
    fig2, axs2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle('Distribuição, Assimetria e Curtose da Recuperação de Veículos', fontsize=16)

    axs2[0].hist(v, bins=15, color='lightgreen', edgecolor='black', density=True, alpha=0.6)
    x = np.linspace(*axs2[0].get_xlim(), 100)
    axs2[0].plot(x, norm.pdf(x, media, np.std(v)), 'k', linewidth=2)
    axs2[0].set_title(f'Histograma com Curva Normal\nAssimetria: {assimetria:.2f}')

    axs2[1].violinplot(v, showmeans=True, showmedians=True)
    axs2[1].set_title(f'Curtose: {curt:.2f}'); axs2[1].set_ylabel('Recuperações')

    plt.tight_layout(); plt.show()
except Exception as e:
    print(f"Erro ao gerar gráficos (parte 2): {e}")