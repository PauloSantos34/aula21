import pandas as pd
from tabulate import tabulate

arquivo_despesas = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\despesas_institucional.csv"

# Ler CSV com encoding e delimitador correto
df_inst = pd.read_csv(arquivo_despesas, delimiter=';', encoding='latin1')

print("Colunas df_inst:", df_inst.columns.tolist())

# Renomear colunas para facilitar manipulação (opcional)
df_inst.rename(columns={
    'Exercício_Financeiro (Lan-Ef)': 'Ano',
    'Grupo de Despesa (nome)': 'Grupo_Despesa',
    'Valor Pago': 'Valor_Pago'
}, inplace=True)

# Agrupar por ano e grupo de despesa somando os valores pagos
df_resumo = df_inst.groupby(['Ano', 'Grupo_Despesa'])['Valor_Pago'].sum().reset_index()

# Ordenar para mostrar maiores gastos primeiro
df_resumo = df_resumo.sort_values(by='Valor_Pago', ascending=False)

print("\nResumo de gastos por Ano e Grupo de Despesa:")
print(tabulate(df_resumo, headers='keys', tablefmt='psql', showindex=False))