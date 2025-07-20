import pandas as pd
from tabulate import tabulate

# Caminho do arquivo
arquivo_entrada = r'c:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.csv'

# Carregar CSV com possíveis ajustes
df_inst = pd.read_csv(arquivo_despesas, delimiter=';', encoding='latin1', skiprows=0)

# Mostrar colunas para verificar nomes reais
print("Colunas df_inst:", df_inst.columns.tolist())

# Exemplo comum: pode ter coluna 'Autor' ou 'Senador' ou 'Nome'
# Vamos checar qual existe para usar nos agrupamentos
possible_author_cols = ['Autor', 'Senador', 'Nome', 'Nome Parlamentar', 'Nome do Senador', 'Nome do Deputado']

author_col = None
for col in possible_author_cols:
    if col in df_inst.columns:
        author_col = col
        break

if author_col is None:
    print("❌ Nenhuma coluna de autor/senador encontrada para agrupamento.")
else:
    print(f"✔ Coluna de autor/senador detectada: '{author_col}'")

# Agora vamos tentar calcular os gastos totais por autor/senador

# Colunas possíveis para valor gasto - você pode ajustar se quiser outras
possible_value_cols = ['Valor Pago', 'Valor Liquidado', 'Valor Total Empenhado', 'Valor Dotação Inicial']

value_col = None
for col in possible_value_cols:
    if col in df_inst.columns:
        value_col = col
        break

if value_col is None:
    print("❌ Nenhuma coluna de valor encontrada para soma dos gastos.")
else:
    print(f"✔ Coluna de valor detectada para soma: '{value_col}'")

if author_col and value_col:
    # Agrupar e somar os gastos por autor/senador
    df_gastos = df_inst.groupby(author_col)[value_col].sum().reset_index()
    df_gastos = df_gastos.sort_values(by=value_col, ascending=False)

    # Mostrar tabela formatada
    print("\nResumo de gastos por parlamentar:")
    print(tabulate(df_gastos, headers='keys', tablefmt='psql', showindex=False))
else:
    print("❌ Não foi possível gerar resumo de gastos por falta de colunas necessárias.")