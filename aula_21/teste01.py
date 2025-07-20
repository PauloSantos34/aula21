# esse arquivo de teste consegue ler o arquivo csv em questão e peço que ele mesmmo faça as análises necessárais as despesas do senado e
# e as agrupe por senador e por faça as análises estatísticas necessárias para vermos se os senadores estão sendo eficientes ou não
# na prestação de seus serviços e se estão gastando de forma correta o dinheiro público e se estão sendo transparentes com a população:

import chardet
import pandas as pd
import os

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

if __name__ == "__main__":
    main()