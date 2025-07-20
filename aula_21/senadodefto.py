import pandas as pd
import chardet  # Certifique-se de ter instalado com: pip install chardet
import os

caminho_ceaps = r"C:/Users/User/Documents/PauloSantos/aula_21/codigo/aula_21/gastos_ceaps_2022.csv"
print("Arquivo CEAPS existe?", os.path.exists(caminho_ceaps))
# Caminhos dos arquivos - ajuste conforme necessário
caminho_ceaps = "C:/Users/User/Documents/PauloSantos/aula_21/codigo/aula_21/gastos_ceaps_2022.csv"
caminho_inst = "C:/Users/User/Documents/PauloSantos/aula_21/codigo/aula_21/despesas_institucional.csv"

def detectar_codificacao(file_path, n_bytes=10000):
    with open(file_path, 'rb') as f:
        rawdata = f.read(n_bytes)
    result = chardet.detect(rawdata)
    return result['encoding']

def tentar_leitura(file_path, encoding, sep):
    try:
        df = pd.read_csv(file_path, sep=sep, encoding=encoding, decimal=',')
        print(f"\nLeitura com separador '{sep}' e encoding '{encoding}' teve sucesso!")
        print(df.head(3))
        return df
    except Exception as e:
        print(f"\nErro lendo com separador '{sep}' e encoding '{encoding}': {e}")
        return None

def main():
    # Ler CEAPS
    encoding_ceaps = detectar_codificacao(caminho_ceaps)
    df_ceaps = tentar_leitura(caminho_ceaps, encoding_ceaps, sep=';')
    if df_ceaps is None:
        df_ceaps = tentar_leitura(caminho_ceaps, encoding_ceaps, sep=',')
    if df_ceaps is None:
        print("Falha ao ler arquivo gastos_ceaps_2022.csv. Abortando.")
        return

    # Ler institucional
    encoding_inst = detectar_codificacao(caminho_inst)
    df_inst = tentar_leitura(caminho_inst, encoding_inst, sep=';')
    if df_inst is None:
        df_inst = tentar_leitura(caminho_inst, encoding_inst, sep=',')
    if df_inst is None:
        print("Falha ao ler arquivo despesas_institucional.csv. Abortando.")
        return

    # Limpar espaços em nomes de colunas
    df_ceaps.columns = df_ceaps.columns.str.strip()
    df_inst.columns = df_inst.columns.str.strip()

    # Ajustar nomes para os que o código espera (caso necessário)
    # Verifique os nomes exatos em seus arquivos e ajuste aqui, ex:
    # df_ceaps.rename(columns={'VALOR_REEMBOLSADO':'VALOR_REEMBOLSADO', 'SENADOR':'SENADOR'}, inplace=True)
    # df_inst.rename(columns={'Autor':'Autor', 'QtdeProposicoes':'QtdeProposicoes'}, inplace=True)

    # Tratar coluna VALOR_REEMBOLSADO do CEAPS para numérico
    df_ceaps['VALOR_REEMBOLSADO'] = (
        df_ceaps['VALOR_REEMBOLSADO']
        .astype(str)
        .str.replace(',', '.')
        .astype(float)
    )

    # Tratar QtdeProposicoes no institucional para numérico
    df_inst['QtdeProposicoes'] = pd.to_numeric(df_inst['QtdeProposicoes'], errors='coerce')

    # Salário médio anual fixo
    salario_mensal = 33789.00
    salario_anual = salario_mensal * 12

    # Total gasto no CEAPS por senador
    gastos_ceaps_total = df_ceaps.groupby('SENADOR')['VALOR_REEMBOLSADO'].sum()

    # Merge dos dois dataframes pelo nome do senador
    df_analise = pd.merge(
        df_inst,
        gastos_ceaps_total.rename("GastosCEAPS"),
        left_on='Autor',
        right_index=True,
        how='left'
    )

    # Filtrar para valores válidos e positivos
    df_analise = df_analise.dropna(subset=['QtdeProposicoes', 'GastosCEAPS'])
    df_analise = df_analise[df_analise['QtdeProposicoes'] > 0]

    # Adicionar salário anual
    df_analise['SalarioAnual'] = salario_anual

    # Calcular gasto total e indicadores de eficiência
    df_analise['GastoTotal'] = df_analise['SalarioAnual'] + df_analise['GastosCEAPS']
    df_analise['CustoPorProposicao'] = df_analise['GastoTotal'] / df_analise['QtdeProposicoes']
    df_analise['EficiênciaMilhao'] = df_analise['QtdeProposicoes'] / (df_analise['GastoTotal'] / 1_000_000)

    df_final = df_analise[['Autor', 'QtdeProposicoes', 'GastosCEAPS', 'SalarioAnual', 'GastoTotal', 'CustoPorProposicao', 'EficiênciaMilhao']]

    print("\n📈 TOP 10 senadores mais eficientes (proposições por milhão gasto):")
    print(df_final.sort_values(by='EficiênciaMilhao', ascending=False).head(10))

    print("\n⚠️ TOP 10 senadores menos eficientes (custo por proposição mais alto):")
    print(df_final.sort_values(by='CustoPorProposicao', ascending=False).head(10))

if __name__ == "__main__":
    main()