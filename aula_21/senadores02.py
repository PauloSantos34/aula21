import pandas as pd
import os
import chardet
import matplotlib.pyplot as plt
import seaborn as sns

def detectar_codificacao(file_path, n_bytes=10000):
    with open(file_path, 'rb') as f:
        rawdata = f.read(n_bytes)
    resultado = chardet.detect(rawdata)
    return resultado['encoding']

def tentar_leitura_csv(caminho, encoding):
    for sep in [';', ',']:
        try:
            df = pd.read_csv(caminho, encoding=encoding, sep=sep, decimal=',')
            print(f"✔️ Leitura bem-sucedida com separador '{sep}'")
            return df
        except Exception as e:
            print(f"❌ Falha com separador '{sep}': {e}")
    return None

def carregar_dados(caminho_arquivo):
    print(f"\n📂 Carregando: {caminho_arquivo}")
    if not os.path.exists(caminho_arquivo):
        print("❌ Arquivo não encontrado.")
        return None
    encoding = detectar_codificacao(caminho_arquivo)
    print(f"-> Detecção de encoding: {encoding}")
    df = tentar_leitura_csv(caminho_arquivo, encoding)
    if df is not None:
        df.columns = df.columns.str.strip().str.lower()
        print(f"📊 {len(df)} linhas carregadas.")
        print("📌 Colunas detectadas:", df.columns.tolist())
    return df

def consolidar_gastos(df_inst, df_ceaps):
    col_inst_nome = [col for col in df_inst.columns if 'nome' in col and 'parlamentar' in col][0]
    col_inst_valor = [col for col in df_inst.columns if 'valor' in col][0]

    col_ceaps_nome = [col for col in df_ceaps.columns if 'nome' in col and 'parlamentar' in col][0]
    col_ceaps_valor = [col for col in df_ceaps.columns if 'reembolsado' in col][0]

    inst = df_inst.groupby(col_inst_nome)[col_inst_valor].sum().reset_index()
    ceaps = df_ceaps.groupby(col_ceaps_nome)[col_ceaps_valor].sum().reset_index()

    inst.rename(columns={col_inst_nome: 'nome', col_inst_valor: 'gasto_institucional'}, inplace=True)
    ceaps.rename(columns={col_ceaps_nome: 'nome', col_ceaps_valor: 'gasto_ceaps'}, inplace=True)

    df = pd.merge(inst, ceaps, on='nome', how='outer').fillna(0)
    df['gasto_total'] = df['gasto_institucional'] + df['gasto_ceaps']
    return df

def analisar_gastos(df):
    print("\n📈 Estatísticas descritivas:")
    print(df[['gasto_institucional', 'gasto_ceaps', 'gasto_total']].describe())

    print("\n💸 Top 10 senadores com maiores gastos:")
    print(df.sort_values(by='gasto_total', ascending=False)[['nome', 'gasto_total']].head(10))

    print("\n💰 Top 10 senadores com menores gastos:")
    print(df.sort_values(by='gasto_total')[['nome', 'gasto_total']].head(10))

    plt.figure(figsize=(10,6))
    sns.histplot(df['gasto_total'], bins=20, kde=True)
    plt.title('Distribuição dos Gastos Totais por Senador')
    plt.xlabel('Gasto Total (R$)')
    plt.ylabel('Número de Senadores')
    plt.tight_layout()
    plt.show()

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivo_inst = os.path.join(base_dir, 'despesas_institucional.csv')
    arquivo_ceaps = os.path.join(base_dir, 'gastos_ceaps_2022.csv')

    df_inst = carregar_dados(arquivo_inst)
    df_ceaps = carregar_dados(arquivo_ceaps)

    if df_inst is not None and df_ceaps is not None:
        df_gastos = consolidar_gastos(df_inst, df_ceaps)
        analisar_gastos(df_gastos)
    else:
        print("⚠️ Não foi possível realizar a análise por falta de dados.")

if __name__ == "__main__":
    main()
