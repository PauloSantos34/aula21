# Acerte o caminho e corrija o código para ler os arquivos csv e realizar as análises necessárias e que o código funcione corretamente.

import pandas as pd
import os
# Caminhos dos arquivos
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
        return True
    except Exception as e:
        print(f"\nErro lendo com separador '{sep}' e encoding '{encoding}': {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = ["despesas_institucional.csv", "gastos_ceaps_2022.csv"]

    for arquivo in arquivos:
        path = os.path.join(base_dir, arquivo)
        print(f"\nAnalisando arquivo: {arquivo}")
        print(f"Caminho completo: {path}")

        try:
            encoding = detectar_codificacao(path)
            print(f"Detecção automática de encoding: {encoding}")
        except FileNotFoundError as e:
            print(f"Arquivo não encontrado: {e}")
            continue

        sucesso = tentar_leitura(path, encoding, sep=';')
        if not sucesso:
            tentar_leitura(path, encoding, sep=',')


# Carregando os dados
try:
    df_ceaps = pd.read_csv(caminho_ceaps, sep=';', encoding='latin1')
    print(f"✔ gastos_ceaps_2022.csv carregado: {len(df_ceaps)} linhas")
except Exception as e:
    print(f"Erro ao ler o CSV CEAPS: {e}")
    exit()

try:
    df_inst = pd.read_csv(caminho_inst, sep=';', encoding='latin1')
    print(f"✔ despesas_institucional.csv carregado: {len(df_inst)} linhas")
except Exception as e:
    print(f"Erro ao ler o CSV Institucional: {e}")
    exit()

# ---- ANÁLISE ----

# Supondo salário mensal bruto médio em 2022
salario_mensal = 33789.00
salario_anual = salario_mensal * 12

# Total gasto no CEAPS por senador
gastos_ceaps_total = df_ceaps.groupby('SENADOR')['VALOR_REEMBOLSADO'].sum()

# Convertendo quantidade de proposições
df_inst['QtdeProposicoes'] = pd.to_numeric(df_inst['QtdeProposicoes'], errors='coerce')

# Unindo os dois conjuntos pelo nome do senador
df_analise = pd.merge(
    df_inst,
    gastos_ceaps_total.rename("GastosCEAPS"),
    left_on='Autor',
    right_index=True,
    how='left'
)

# Removendo senadores com 0 proposições ou NaN
df_analise = df_analise.dropna(subset=['QtdeProposicoes', 'GastosCEAPS'])
df_analise = df_analise[df_analise['QtdeProposicoes'] > 0]

# Adicionando salário anual fixo
df_analise['SalarioAnual'] = salario_anual

# Cálculo do total de recursos públicos por senador (salário + CEAPS)
df_analise['GastoTotal'] = df_analise['SalarioAnual'] + df_analise['GastosCEAPS']

# Custo por proposição apresentada
df_analise['CustoPorProposicao'] = df_analise['GastoTotal'] / df_analise['QtdeProposicoes']

# Eficiência: proposições por R$ 1 milhão
df_analise['EficiênciaMilhao'] = df_analise['QtdeProposicoes'] / (df_analise['GastoTotal'] / 1_000_000)

# Resultados finais
df_final = df_analise[['Autor', 'QtdeProposicoes', 'GastosCEAPS', 'SalarioAnual', 'GastoTotal', 'CustoPorProposicao', 'EficiênciaMilhao']]

# Exibe os 10 mais eficientes
print("\n📈 TOP 10 senadores mais eficientes (proposições por milhão gasto):")
print(df_final.sort_values(by='EficiênciaMilhao', ascending=False).head(10))

# Exibe os 10 mais ineficientes
print("\n⚠️ TOP 10 senadores menos eficientes (custo por proposição mais alto):")
print(df_final.sort_values(by='CustoPorProposicao', ascending=False).head(10))

if __name__ == "__main__":
    main()