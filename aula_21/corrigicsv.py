import pandas as pd
from ftfy import fix_text
import os

pasta_dados = r'c:\Users\User\Documents\PauloSantos\aula_21\dados'
print("Arquivos encontrados na pasta:")
print(os.listdir(pasta_dados))

# Caminho do arquivo original
arquivo_entrada = r"c:\Users\User\Documents\PauloSantos\aula_21\dados\gastos_ceaps_2022.csv"
# Caminho do novo arquivo corrigido
arquivo_saida = 'dados_senado_corrigido.csv'

# Leitura do arquivo original com encoding que não quebre os caracteres
df = pd.read_csv(arquivo_entrada, encoding='latin1', sep=';')

# Corrige a acentuação de todos os campos de texto
for coluna in df.columns:
    if df[coluna].dtype == 'object':
        df[coluna] = df[coluna].apply(lambda x: fix_text(str(x)))

# Salva o arquivo corrigido em UTF-8 com ; como separador
df.to_csv(arquivo_saida, sep=';', index=False, encoding='utf-8')

print(f"Acentuação corrigida e arquivo salvo em: {arquivo_saida}")
