import pandas as pd
from tabulate import tabulate

def load_institucional(path):
    """Carrega as despesas institucionais com nomes de senadores."""
    try:
        df = pd.read_csv(path, sep=';', encoding='utf-8', decimal=',')
        df['VALOR_REEMBOLSADO'] = pd.to_numeric(df['VALOR_REEMBOLSADO'], errors='coerce')
        df.dropna(subset=['VALOR_REEMBOLSADO'], inplace=True)
        return df
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {path}")
        return pd.DataFrame()

def resumo_total_por_senador(df):
    """Resumo total de valores pagos por senador."""
    resumo = df.groupby('SENADOR')['VALOR_REEMBOLSADO'].sum().reset_index()
    resumo = resumo.sort_values(by='VALOR_REEMBOLSADO', ascending=False)
    return resumo

def resumo_por_tipo_despesa(df):
    """Resumo por tipo de despesa e senador."""
    resumo = df.groupby(['SENADOR', 'TIPO_DESPESA'])['VALOR_REEMBOLSADO'].sum().reset_index()
    resumo = resumo.sort_values(by=['SENADOR', 'VALOR_REEMBOLSADO'], ascending=[True, False])
    return resumo

def main():
    # Substitua esse caminho caso o arquivo esteja em outra pasta
    arquivo = "despesas_institucional.csv"
    df = load_institucional(arquivo)

    if df.empty:
        print("Erro ao carregar dados.")
        return

    print("\n=== Total de valores pagos por SENADOR ===")
    resumo1 = resumo_total_por_senador(df)
    print(tabulate(resumo1, headers='keys', showindex=False, tablefmt='grid', floatfmt=".2f"))

    print("\n=== Total de valores pagos por SENADOR e TIPO DE DESPESA ===")
    resumo2 = resumo_por_tipo_despesa(df)
    print(tabulate(resumo2, headers='keys', showindex=False, tablefmt='grid', floatfmt=".2f"))

if __name__ == "__main__":
    main()