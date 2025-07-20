import chardet
import pandas as pd
import os

def detectar_codificacao(file_path, n_bytes=10000):
    with open(file_path, 'rb') as f:
        rawdata = f.read(n_bytes)
    result = chardet.detect(rawdata)
    return result['encoding']

def ler_arquivo(file_path):
    encoding = detectar_codificacao(file_path)
    try:
        df = pd.read_csv(file_path, sep=';', encoding=encoding, decimal=',')
    except Exception:
        df = pd.read_csv(file_path, sep=',', encoding=encoding, decimal=',')
    return df

def analisar_despesas_ceaps(df):
    print("\n🔎 Análise de despesas do CEAPS por senador:")

    if 'Senador' not in df.columns:
        col_nome = [c for c in df.columns if 'nome' in c.lower() or 'parlamentar' in c.lower()]
        if col_nome:
            df.rename(columns={col_nome[0]: 'Senador'}, inplace=True)
        else:
            print("❌ Coluna com nome do senador não encontrada.")
            return

    col_valor = [c for c in df.columns if 'valor' in c.lower() and ('reemb' in c.lower() or 'liquid' in c.lower())]
    if not col_valor:
        col_valor = [c for c in df.columns if 'valor' in c.lower()]
    if not col_valor:
        print("❌ Coluna de valor não encontrada.")
        return
    else:
        valor_col = col_valor[0]

    df[valor_col] = pd.to_numeric(df[valor_col], errors='coerce')
    df = df.dropna(subset=[valor_col])

    resumo = df.groupby('Senador')[valor_col].agg(['sum', 'mean', 'std', 'count']).sort_values('sum', ascending=False)
    resumo.columns = ['Total (R$)', 'Média por despesa', 'Desvio padrão', 'Qtd Despesas']
    resumo['Coef. Variação'] = resumo['Desvio padrão'] / resumo['Média por despesa']

    media_geral = resumo['Total (R$)'].mean()
    desvio_geral = resumo['Total (R$)'].std()

    resumo['Acima da média?'] = resumo['Total (R$)'] > media_geral + 2 * desvio_geral
    resumo['Pontuação de Eficiência'] = resumo['Média por despesa'] / resumo['Total (R$)']

    print("\n📊 Estatísticas gerais:")
    print(resumo.head(10))
    print("\n⚠️ Senadores com gastos muito acima da média:")
    print(resumo[resumo['Acima da média?'] == True])

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = ["despesas_institucional.csv", "gastos_ceaps_2022.csv"]

    for arquivo in arquivos:
        path = os.path.join(base_dir, arquivo)
        print(f"\n📁 Lendo: {arquivo}")
        print(f"📍 Caminho: {path}")

        if not os.path.exists(path):
            print(f"❌ Arquivo não encontrado: {path}")
            continue

        df = ler_arquivo(path)
        print(f"✅ Leitura ok: {df.shape[0]} linhas, {df.shape[1]} colunas")

        if 'ceaps' in arquivo.lower():
            analisar_despesas_ceaps(df)

if __name__ == "__main__":
    main()



