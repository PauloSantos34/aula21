import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import os
from pathlib import Path
import pandas as pd
import os
# 1. Leitura dos dados
print("Diretório atual:", os.getcwd())
print("Arquivos na pasta-pai:", os.listdir('..'))

df = pd.read_csv('../dados_municipios.csv')   # Esperado: colunas ['Município', 'Reprovação', 'Abandono', 'Proficiência']

# 2. Estatísticas descritivas
estatisticas = {}
for col in ['Reprovação', 'Abandono', 'Proficiência']:
    series = df[col]
    estatisticas[col] = {
        'Média': round(series.mean(), 2),
        'Mediana': round(series.median(), 2),
        'Desvio Padrão': round(series.std(), 2),
        'Mínimo': round(series.min(), 2),
        'Máximo': round(series.max(), 2),
        'Q1': round(series.quantile(0.25), 2),
        'Q3': round(series.quantile(0.75), 2),
        'IQR': round(series.quantile(0.75) - series.quantile(0.25), 2),
        'Assimetria': round(skew(series), 2),
        'Curtose': round(kurtosis(series), 2)
    }
estatisticas_df = pd.DataFrame(estatisticas)

# 3. Gerar boxplots
sns.set(style="whitegrid", palette="pastel", font_scale=1.1)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
for ax, col in zip(axes, ['Reprovação', 'Abandono', 'Proficiência']):
    sns.boxplot(y=df[col], ax=ax)
    ax.set_title(f"Boxplot - {col}")
    ax.set_ylabel(f"{col} (%)")

plt.tight_layout()

# Certifique-se que a pasta existe
output_folder = "./aula_21"
os.makedirs(output_folder, exist_ok=True)
plt.savefig(os.path.join(output_folder, "boxplots_indicadores.png"))
plt.close()

# 4. Identificar outliers
outliers_dict = {}
for col in ['Reprovação', 'Abandono', 'Proficiência']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lim_inf) | (df[col] > lim_sup)][['Município', col]]
    outliers_dict[col] = outliers

# 5. Melhores e piores municípios
melhores_piores = {}
for col in ['Reprovação', 'Abandono']:
    melhores_piores[col] = {
        'Melhores': df.nsmallest(5, col)[['Município', col]],
        'Piores': df.nlargest(5, col)[['Município', col]]
    }
melhores_piores['Proficiência'] = {
    'Melhores': df.nlargest(5, 'Proficiência')[['Município', 'Proficiência']],
    'Piores': df.nsmallest(5, 'Proficiência')[['Município', 'Proficiência']]
}

# 6. Exportar para Excel
with pd.ExcelWriter("analise_educacao_municipios.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Dados Brutos", index=False)
    estatisticas_df.T.to_excel(writer, sheet_name="Estatísticas")
    for col, out_df in outliers_dict.items():
        # Nomes de abas no Excel têm limite de 31 caracteres
        sheet_name = f"Outliers - {col}"
        if len(sheet_name) > 31:
            sheet_name = sheet_name[:31]
        out_df.to_excel(writer, sheet_name=sheet_name, index=False)
    for col, subgrupos in melhores_piores.items():
        for nome, dados in subgrupos.items():
            aba = f"{nome} - {col}"
            if len(aba) > 31:
                aba = aba[:31]
            dados.to_excel(writer, sheet_name=aba, index=False)
