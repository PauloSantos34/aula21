import pandas as pd
from tabulate import tabulate

# Caminho do arquivo CEAPS
arquivo_ceaps = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.csv"

# Ler CSV - aqui pode precisar ajustar encoding/delimitador se der erro
df_ceaps = pd.read_csv(arquivo_ceaps, delimiter=';', encoding='latin1')

# Mostrar colunas para identificar os nomes corretos
print("Colunas df_ceaps:", df_ceaps.columns.tolist())

# Ajustar nomes de colunas importantes, caso necessário
# Exemplo:
# 'SENADOR', 'VALOR_REEMBOLSADO', 'ANO' podem ter nomes diferentes
# Você deve substituir os nomes abaixo pelos que aparecem na sua tabela
col_senador = 'SENADOR'  # ajuste se for diferente
col_valor = 'VALOR_REEMBOLSADO'  # ajuste se for diferente
col_ano = 'ANO'  # ajuste se for diferente

# Verificar se colunas existem
missing_cols = [c for c in [col_senador, col_valor, col_ano] if c not in df_ceaps.columns]
if missing_cols:
    print(f"❌ Colunas faltando: {missing_cols}")
    print("Revise os nomes das colunas e ajuste no código.")
else:
    # Converter coluna de valor para numérico (retirando possíveis caracteres)
    df_ceaps[col_valor] = pd.to_numeric(df_ceaps[col_valor].astype(str).str.replace(',', '.').str.replace('[^0-9.]', '', regex=True), errors='coerce').fillna(0)

    # Agrupar por senador e ano, somando os valores
    df_gastos = df_ceaps.groupby([col_senador, col_ano])[col_valor].sum().reset_index()

    # Ordenar para visualização
    df_gastos = df_gastos.sort_values(by=[col_ano, col_valor], ascending=[True, False])

    print("\nResumo de gastos CEAPS por senador e ano:")
    print(tabulate(df_gastos, headers='keys', tablefmt='psql', showindex=False))