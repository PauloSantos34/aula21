import pandas as pd

# Caminhos dos arquivos
arquivo_ceaps = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.csv"
arquivo_inst = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\despesas_institucional.csv"

# Função para converter valores monetários formatados em string (ex: '1.000,50') para float 1000.50
def converte_valor(valor_str):
    if pd.isna(valor_str):
        return 0.0
    # Remove pontos e troca vírgula por ponto
    valor_str = str(valor_str).replace('.', '').replace(',', '.')
    try:
        return float(valor_str)
    except:
        return 0.0

# 1) Carregar gastos_ceaps_2022.csv
df_ceaps = pd.read_csv(arquivo_ceaps, delimiter=';', encoding='latin1')

# Ajustar colunas e converter tipos
df_ceaps['ANO'] = df_ceaps['ANO'].astype(str)
df_ceaps['MÊS'] = df_ceaps['MÊS'].astype(str).str.zfill(2)  # zfill para garantir mês 01,02,...
df_ceaps['DATA'] = pd.to_datetime(df_ceaps['DATA'], dayfirst=True, errors='coerce')
df_ceaps['VALOR_REEMBOLSADO'] = df_ceaps['VALOR_REEMBOLSADO'].apply(converte_valor)
df_ceaps['SENADOR'] = df_ceaps['SENADOR'].astype(str).str.strip()

# 2) Carregar despesas_institucional.csv
df_inst = pd.read_csv(arquivo_inst, delimiter=';', encoding='latin1')

# Converter datas e valores
df_inst['Data da Carga da Base'] = pd.to_datetime(df_inst['Data da Carga da Base'], dayfirst=True, errors='coerce')
for col in ['Valor dotaÃ§Ã£o inicial', 'Valor dotaÃ§Ã£o atualizada', 'Valor Total Empenhado', 'Valor Liquidado', 'Valor Pago']:
    df_inst[col] = df_inst[col].apply(converte_valor)

# --- Análise simples ---

# Total de despesas por senador (gastos ceaps)
gastos_por_senador = df_ceaps.groupby('SENADOR')['VALOR_REEMBOLSADO'].sum().sort_values(ascending=False)

print("\n===== Despesas totais reembolsadas por senador (2022) =====")
print(gastos_por_senador.to_string(float_format="R$ {:,.2f}".format))

# Despesas mensais totais (todos os senadores juntos)
df_ceaps['ANO_MES'] = df_ceaps['ANO'] + '-' + df_ceaps['MÊS']
despesas_mensais = df_ceaps.groupby('ANO_MES')['VALOR_REEMBOLSADO'].sum().sort_index()

print("\n===== Despesas mensais totais =====")
print(despesas_mensais.to_string(float_format="R$ {:,.2f}".format))

# Resumo do orçamento institucional (ano 2025)
total_orcamento = df_inst[['Valor dotaÃ§Ã£o inicial', 'Valor dotaÃ§Ã£o atualizada', 'Valor Total Empenhado', 'Valor Liquidado', 'Valor Pago']].sum()

print("\n===== Resumo do orçamento institucional (2025) =====")
for k, v in total_orcamento.items():
    print(f"{k}: R$ {v:,.2f}")