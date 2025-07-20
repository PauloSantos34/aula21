import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# === 1. Leitura do arquivo ===
arquivo_csv = "dados_criminais_rj.csv"  # renomeie conforme seu arquivo real
df = pd.read_csv(arquivo_csv)

# === 2. Pré-processamento ===
df.columns = df.columns.str.strip().str.lower()
df['mes_ano'] = pd.to_datetime(df['mes_ano'], format='%Y%m')

# === 3. Estatísticas descritivas por tipo de crime ===
col_crimes = [
    'hom_doloso', 'lesao_corp_morte', 'latrocinio', 'cvli', 'hom_por_interv_policial',
    'letalidade_violenta', 'roubo_veiculo', 'roubo_celular', 'roubo_transeunte',
    'furto_veiculos', 'furto_celular', 'estupro', 'sequestro', 'extorsao', 'estelionato'
]

# Agrupamento por CISP
df_cisp = df.groupby('cisp')[col_crimes].sum().reset_index()

# === 4. Exibe resumo por CISP ===
print("\nResumo por CISP (Total de crimes):")
print(tabulate(df_cisp, headers='keys', tablefmt='github', showindex=False))

# === 5. Tendência temporal de letalidade violenta ===
plt.figure(figsize=(10, 5))
df_mensal = df.groupby('mes_ano')['letalidade_violenta'].sum()
df_mensal.plot()
plt.title("Letalidade Violenta - Rio de Janeiro")
plt.xlabel("Mês/Ano")
plt.ylabel("Casos")
plt.grid(True)
plt.tight_layout()
plt.savefig("letalidade_violenta_temporal.png")
plt.close()

# === 6. Gráfico de barras: Total de roubos por CISP ===
plt.figure(figsize=(12, 6))
df_cisp_sorted = df.groupby('cisp')['roubo_veiculo'].sum().sort_values(ascending=False)
df_cisp_sorted.plot(kind='bar', color='tomato')
plt.title("Total de Roubos de Veículos por CISP")
plt.xlabel("CISP")
plt.ylabel("Casos")
plt.tight_layout()
plt.savefig("roubo_veiculo_por_cisp.png")
plt.close()

# === 7. Heatmap de correlação entre crimes ===
plt.figure(figsize=(12, 8))
sns.heatmap(df[col_crimes].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlação entre tipos de crimes")
plt.tight_layout()
plt.savefig("correlacao_crimes.png")
plt.close()

# === 8. Estatísticas descritivas gerais ===
desc = df[col_crimes].describe().T
desc['coef_var'] = desc['std'] / desc['mean']
print("\nEstatísticas descritivas dos crimes (geral):")
print(tabulate(desc[['mean', 'std', 'min', 'max', 'coef_var']], headers='keys', tablefmt='github'))

# === 9. Exporta tabelas para CSV ===
df_cisp.to_csv("resumo_crimes_por_cisp.csv", index=False)
desc.to_csv("estatisticas_crimes_geral.csv")

print("\n✅ Análises concluídas. Gráficos e tabelas salvos no diretório.")