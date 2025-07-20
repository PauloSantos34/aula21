import pandas as pd

# Caminho para o arquivo de gastos do CEAPS
caminho_ceaps = 'gastos_ceaps_2022.csv'

# Leitura do arquivo com tratamento de codificação e separador
df_ceaps = pd.read_csv(
    caminho_ceaps,
    sep=';',                  # separador correto
    encoding='latin1',        # para tratar caracteres como "ç", "ã", "é"
    skiprows=1                # pula a linha "ULTIMA ATUALIZACAO"
)

# Leitura correta do arquivo com linha extra pulada
df_ceaps = pd.read_csv(
    'gastos_ceaps_2022.csv',
    sep=';',
    encoding='ISO-8859-1',
    skiprows=1  # pula a linha com "ULTIMA ATUALIZACAO"
)

# Limpa espaços dos nomes de colunas
df_ceaps.columns = df_ceaps.columns.str.strip()

# Verifica as primeiras linhas
print(df_ceaps.head())
print("\nColunas:", df_ceaps.columns.tolist())
# Remove espaços extras nos nomes das colunas
df_ceaps.columns = df_ceaps.columns.str.strip()

# Exibe as colunas disponíveis para checar
print("Colunas disponíveis:", df_ceaps.columns.tolist())

# Verifica se a coluna 'SENADOR' está presente
if 'SENADOR' not in df_ceaps.columns:
    raise ValueError("❌ A coluna 'SENADOR' não foi encontrada. Verifique o arquivo CSV.")

# Exemplo de agrupamento por senador e tipo de despesa
gastos_agrupados = df_ceaps.groupby(['SENADOR', 'TIPO_DESPESA'])['VALOR_REEMBOLSADO'].sum().reset_index()

# Converte valores para float (se ainda estiverem como string)
gastos_agrupados['VALOR_REEMBOLSADO'] = gastos_agrupados['VALOR_REEMBOLSADO'].replace(',', '.', regex=True).astype(float)

# Ordena do maior gasto para o menor
gastos_ordenados = gastos_agrupados.sort_values(by='VALOR_REEMBOLSADO', ascending=False)

# Exibe os 10 maiores gastos
print("\nTop 10 maiores gastos por senador e tipo de despesa:")
print(gastos_ordenados.head(10))