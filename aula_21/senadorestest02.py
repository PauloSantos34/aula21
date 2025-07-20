import pandas as pd

# Caminhos absolutos dos arquivos
arquivo_ceaps = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.csv"
arquivo_institucional = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\despesas_institucional.csv"

def carregar_csv(caminho, nome_arquivo):
    try:
        df = pd.read_csv(
            caminho,
            sep=';',
            encoding='latin1',
            decimal=',',
            thousands='.'
        )
        print(f"✔ {nome_arquivo} carregado: {df.shape[0]} linhas")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar {nome_arquivo}: {e}")
        return pd.DataFrame()

# Carregando os datasets
df_ceaps = carregar_csv(arquivo_ceaps, "gastos_ceaps_2022.csv")
df_inst = carregar_csv(arquivo_institucional, "despesas_institucional.csv")

# Limpar e padronizar nomes das colunas para evitar erros
df_ceaps.columns = df_ceaps.columns.str.strip().str.upper()
df_inst.columns = df_inst.columns.str.strip()

# Exibir as colunas para conferir
print("Colunas df_ceaps:", df_ceaps.columns.tolist())
print("Colunas df_inst:", df_inst.columns.tolist())

# Se os nomes dos senadores estiverem em colunas diferentes, ajuste aqui
# Por exemplo, no CEAPS a coluna do senador é 'SENADOR'
# No Institucional, o autor é 'Autor' (case sensitive)

# Limpar e padronizar strings dos nomes para garantir merge correto
if 'SENADOR' in df_ceaps.columns:
    df_ceaps['SENADOR'] = df_ceaps['SENADOR'].astype(str).str.strip().str.upper()
else:
    print("❌ Coluna 'SENADOR' não encontrada em df_ceaps.")

if 'Autor' in df_inst.columns:
    df_inst['Autor'] = df_inst['Autor'].astype(str).str.strip().str.upper()
else:
    print("❌ Coluna 'Autor' não encontrada em df_inst.")

# Tratar coluna VALOR_REEMBOLSADO para float
if 'VALOR_REEMBOLSADO' in df_ceaps.columns:
    df_ceaps['VALOR_REEMBOLSADO'] = (
        df_ceaps['VALOR_REEMBOLSADO']
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
    )
    df_ceaps['VALOR_REEMBOLSADO'] = pd.to_numeric(df_ceaps['VALOR_REEMBOLSADO'], errors='coerce').fillna(0.0)
else:
    print("❌ Coluna 'VALOR_REEMBOLSADO' não encontrada em df_ceaps.")

# Total gasto CEAPS por senador
if 'SENADOR' in df_ceaps.columns and 'VALOR_REEMBOLSADO' in df_ceaps.columns:
    gastos_por_senador = df_ceaps.groupby('SENADOR')['VALOR_REEMBOLSADO'].sum()
else:
    gastos_por_senador = pd.Series(dtype='float64')
    print("❌ Não foi possível calcular gastos por senador.")

# Tratar QtdeProposicoes para numérico no df_inst
if 'QtdeProposicoes' in df_inst.columns:
    df_inst['QtdeProposicoes'] = pd.to_numeric(df_inst['QtdeProposicoes'], errors='coerce')
else:
    print("❌ Coluna 'QtdeProposicoes' não encontrada em df_inst.")
    df_inst['QtdeProposicoes'] = 0

# Salário médio mensal e anual (fixo)
salario_mensal = 33789.00
salario_anual = salario_mensal * 12

# Merge entre institucional e gastos CEAPS pelo nome do senador (autores em maiúsculas)
df_analise = pd.merge(
    df_inst,
    gastos_por_senador.rename("GastosCEAPS"),
    left_on='Autor',
    right_index=True,
    how='left'
)

# Preencher NaN dos gastos CEAPS com zero
df_analise['GastosCEAPS'] = df_analise['GastosCEAPS'].fillna(0.0)

# Remover registros com QtdeProposicoes zero ou NaN para análise válida
df_analise = df_analise[df_analise['QtdeProposicoes'] > 0]

# Adicionar salário anual fixo
df_analise['SalarioAnual'] = salario_anual

# Calcular gasto total público (salário + CEAPS)
df_analise['GastoTotal'] = df_analise['SalarioAnual'] + df_analise['GastosCEAPS']

# Custo médio por proposição
df_analise['CustoPorProposicao'] = df_analise['GastoTotal'] / df_analise['QtdeProposicoes']

# Eficiência: número de proposições por R$ 1 milhão gasto
df_analise['EficienciaPorMilhao'] = df_analise['QtdeProposicoes'] / (df_analise['GastoTotal'] / 1_000_000)

# Resultado final — colunas selecionadas para visualização
df_final = df_analise[[
    'Autor', 'QtdeProposicoes', 'GastosCEAPS', 'SalarioAnual', 'GastoTotal', 'CustoPorProposicao', 'EficienciaPorMilhao'
]]

# Ordenar e exibir os 10 mais eficientes
print("\n📈 TOP 10 senadores mais eficientes (proposições por milhão gasto):")
print(df_final.sort_values(by='EficienciaPorMilhao', ascending=False).head(10).to_string(index=False))

# Ordenar e exibir os 10 menos eficientes
print("\n⚠️ TOP 10 senadores menos eficientes (custo por proposição mais alto):")
print(df_final.sort_values(by='CustoPorProposicao', ascending=False).head(10).to_string(index=False))