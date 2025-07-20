import pandas as pd

# Caminho do arquivo Excel salvo
arquivo_excel = r'c:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.xlsx'

# Ler o Excel
df = pd.read_excel(arquivo_excel)

# Limpar espaços em branco nas colunas
df.columns = df.columns.str.strip()

# Mostrar as primeiras linhas e colunas para confirmar leitura
print("Colunas disponíveis:\n", df.columns.tolist())
print(df.head())

# Verificar nomes exatos da coluna do senador e do valor
col_senador = 'SENADOR'
col_valor = 'VALOR_REEMBOLSADO'

# Tratar valores: substituir vírgula por ponto e converter para float (caso seja string)
df[col_valor] = df[col_valor].astype(str).str.replace(',', '.')
df[col_valor] = pd.to_numeric(df[col_valor], errors='coerce').fillna(0)

# Agrupar por senador e somar valores
totais_por_senador = df.groupby(col_senador)[col_valor].sum().sort_values(ascending=False)

print("\nTotal de gastos por senador (decrescente):")
print(totais_por_senador)

# Se quiser salvar o resultado em Excel:
totais_por_senador.to_excel('totais_gastos_por_senador.xlsx')

# Opcional: análise por tipo de despesa
if 'TIPO_DESPESA' in df.columns:
    gastos_por_tipo = df.groupby('TIPO_DESPESA')[col_valor].sum().sort_values(ascending=False)
    print("\nTotal de gastos por tipo de despesa:")
    print(gastos_por_tipo)