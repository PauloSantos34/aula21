import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis, norm
from tabulate import tabulate

def exibir_tabela(dados, headers, titulo=None):
    if titulo: print(f"\n{titulo}")
    print(tabulate(dados, headers=headers, tablefmt="grid", floatfmt=".2f"))

# URLs de dados
URL_REC = "https://www.ispdados.rj.gov.br/Arquivos/UppEvolucaoMensalDetitulos.csv"
URL_ROU = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

# -------------------------------
# 1. Carregar e agregar dados
# -------------------------------
df_rec = pd.read_csv(URL_REC, sep=';', encoding='iso-8859-1')
df_rec = df_rec[['upp', 'recuperacao_veiculos']]
df_rec_agg = df_rec.groupby('upp', as_index=False).sum(numeric_only=True)

df_rou = pd.read_csv(URL_ROU, sep=';', encoding='iso-8859-1')
df_rou = df_rou[['munic', 'roubo_veiculo']]
df_rou_agg = df_rou.groupby('munic', as_index=False).sum(numeric_only=True)

# -------------------------------
# 2. Estatísticas da recuperação
# -------------------------------
val_rec = df_rec_agg['recuperacao_veiculos'].values
stats_rec = {
    'média': np.mean(val_rec),
    'mediana': np.median(val_rec),
    'dist_rel (|m-mdn|/mdn)': abs((np.mean(val_rec) - np.median(val_rec)) / np.median(val_rec)),
    'q1,q2,q3': np.quantile(val_rec, [0.25,0.5,0.75]),
    'iqr': np.ptp(np.quantile(val_rec, [0.25,0.75])),
    'mín,max,range': (np.min(val_rec), np.max(val_rec), np.ptp(val_rec)),
    'skewness': skew(val_rec),
    'kurtosis': kurtosis(val_rec)
}

q1_r, q2_r, q3_r = np.quantile(val_rec,[0.25,0.5,0.75])
iqr_r = q3_r - q1_r
lim_inf_r = q1_r - 1.5*iqr_r
lim_sup_r = q3_r + 1.5*iqr_r
out_rec_inf = df_rec_agg[df_rec_agg['recuperacao_veiculos'] < lim_inf_r]
out_rec_sup = df_rec_agg[df_rec_agg['recuperacao_veiculos'] > lim_sup_r]

# -------------------------------
# 3. Estatísticas do roubo
# -------------------------------
val_rou = df_rou_agg['roubo_veiculo'].values
stats_rou = {
    'média': np.mean(val_rou),
    'mediana': np.median(val_rou),
    'dist_rel': abs((np.mean(val_rou) - np.median(val_rou)) / np.median(val_rou)),
    'q1,q2,q3': np.quantile(val_rou, [0.25,0.5,0.75]),
    'iqr': np.ptp(np.quantile(val_rou, [0.25,0.75])),
    'mín,max,range': (np.min(val_rou), np.max(val_rou), np.ptp(val_rou)),
    'var': np.var(val_rou),
    'std': np.std(val_rou),
    'coef_var': np.std(val_rou)/np.mean(val_rou),
    'skew': df_rou_agg['roubo_veiculo'].skew(),
    'kurt': df_rou_agg['roubo_veiculo'].kurtosis()
}

q1_v, q2_v, q3_v = stats_rou['q1,q2,q3']
iqr_v = stats_rou['iqr']
lim_inf_v = q1_v - 1.5*iqr_v
lim_sup_v = q3_v + 1.5*iqr_v
out_rou_inf = df_rou_agg[df_rou_agg['roubo_veiculo'] < lim_inf_v]
out_rou_sup = df_rou_agg[df_rou_agg['roubo_veiculo'] > lim_sup_v]

# -------------------------------
# 4. Visualizações
# -------------------------------

# Tabelas
exibir_tabela(df_rec_agg.sort_values('recuperacao_veiculos', ascending=False).head(5),
              headers='keys', titulo="Top5 UPPs (Recuperações)")
exibir_tabela(df_rou_agg.sort_values('roubo_veiculo', ascending=False).head(5),
              headers='keys', titulo="Top5 Municípios (Roubos)")

# Estatísticas
print("\n>> Estatísticas Recuperação de Veículos por UPP:")
for k,v in stats_rec.items():
    print(f"{k}: {v}")
print("\n>> Estatísticas Roubo de Veículos por Município:")
for k,v in stats_rou.items():
    print(f"{k}: {v}")

# Histogramas e boxplots
fig, axs = plt.subplots(2,2, figsize=(16,12))
fig.suptitle("Comparativo Recuperações vs Roubos de Veículos")

axs[0,0].hist(val_rec, bins=15, color='skyblue', edgecolor='black', alpha=0.7, density=True)
x= np.linspace(min(val_rec), max(val_rec),100)
axs[0,0].plot(x, norm.pdf(x, np.mean(val_rec), np.std(val_rec)), 'k')
axs[0,0].set_title("Recuperações por UPP (hist + curva normal)")

axs[0,1].hist(val_rou, bins=15, color='salmon', edgecolor='black', alpha=0.7, density=True)
x2 = np.linspace(min(val_rou), max(val_rou),100)
axs[0,1].plot(x2, norm.pdf(x2, np.mean(val_rou), np.std(val_rou)), 'k')
axs[0,1].set_title("Roubos por Município (hist + curva normal)")

axs[1,0].boxplot(val_rec, vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
axs[1,0].set_title("Boxplot – Recuperações")

axs[1,1].boxplot(val_rou, vert=False, patch_artist=True, boxprops=dict(facecolor='lightcoral'))
axs[1,1].set_title("Boxplot – Roubos")

plt.tight_layout()
plt.show()

# KDE
plt.figure(figsize=(8,5))
sns.kdeplot(val_rec, bw_adjust=2, label='Recuperação', color='blue')
sns.kdeplot(val_rou, bw_adjust=2, label='Roubo', color='red')
plt.legend()
plt.title("Densidade – Roubos × Recuperações")
plt.xlabel("Volume (%)")
plt.show()

# -------------------------------
# 5. Correlação e Dispersão
# -------------------------------

# Comparação artificial apenas para detectar tendências gerais
min_len = min(len(df_rec_agg), len(df_rou_agg))
rec_values = df_rec_agg['recuperacao_veiculos'].sort_values(ascending=False).head(min_len).reset_index(drop=True)
rou_values = df_rou_agg['roubo_veiculo'].sort_values(ascending=False).head(min_len).reset_index(drop=True)

correlacao = rec_values.corr(rou_values)
print(f"\n>> Correlação Pearson entre Recuperações e Roubos (valores ordenados, sem base territorial comum): {correlacao:.4f}")

plt.figure(figsize=(8,6))
plt.scatter(rou_values, rec_values, color='purple', alpha=0.6)
plt.xlabel("Roubos de Veículos (municípios)")
plt.ylabel("Recuperações de Veículos (UPPs)")
plt.title("Dispersão entre Roubos e Recuperações de Veículos")
plt.grid(True)
plt.show()

# -------------------------------
# 6. Sugestões de interpretação
# -------------------------------
print("\n===== Sugestões =====")
print("- Indicar UPPs com alta recuperação X baixo roubo como áreas de atuação segura.")
print("- Municípios com roubo acima do limite superior devem ser priorizados para ações preventivas.")
print("- UPPs que são outliers inferiores em recuperação podem precisar reforço de fiscalização.")
print("- Levar em conta skew/kurtosis: distribuições muito assimétricas indicam recursos concentrados em poucas regiões.")
print("- A correlação entre os dados indica tendências gerais, mas não reflete relação territorial direta.")