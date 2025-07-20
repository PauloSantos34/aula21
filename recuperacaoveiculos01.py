# import re
# import unicodedata
import pandas as pd
import numpy as np


try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/UppEvolucaoMensalDetitulos.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    # encoding='iso-8859-1' - Codificação dos caracteres com acentuação
    # outras opções: utf-8, iso-8859-1, latin1, cp1252
    # encodings principais: https://docs.python.org/3/library/codecs.html#standard-encodings
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    
    # Demilitando somente as variáveis do Exemplo01: UPP e recuperação de_veiculos
    # Dados sendo obtidos do ISP (Istituto de Segurança Pública - rj.gov.br no Período de 01/2007 a 06/2021).
    df_ocorrencias = df_ocorrencias[['upp', 'recuperacao_veiculos']]

    # Totalizar recuperação de veiculo por UPP (agrupar e somar)
    # reset_index(), traz de volta os índeces que numera as colunas, pois eles se perdem
    # nesta operação
    df_recuperacao_veiculos = df_ocorrencias.groupby('upp').sum(['recuperacao_veiculos']).reset_index()

    # Printando as linhas iniciais com o método head() apenas para ver se os dados
    # foram obtidos corretamente
    print(df_recuperacao_veiculos.head())

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Inicando a obtenção das medidas fundamentadas em estatística descritiva
try:
    print('Obtendo informações sobre padrão de recuperação de veículos...')

    # Numpy
    # Uso do ARRAY
    # Array faz parte da biblioteca numpy
    # Array é uma estrutura de dados que armazena uma coleção de dados
    # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
    # pip install numpy
    # import numpy as np
    # NumPy significa numerical python e tem como objetivo adicionar suporte
    # para arrays e matrizes multidimensionais, juntamente com uma grande
    # coleção de funções matemáticas de alto nível.
    # Uso do array significa ganho computacional
    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos['recuperacao_veiculos'])

    # Obtendo média de recuperação de veiculos
    media_recuperacao_veiculos = np.mean(array_recuperacao_veiculos)

    # Obtendo mediana de rrecuperação de veiculos
    # Mediana é o valor que divide a distribuição em duas partes iguais
    # (50% dos dados estão abaixo e 50% acima)
    mediana_recuperacao_veiculos = np.median(array_recuperacao_veiculos)

    # Distânicia entre média e mediana
    # A distância entre a média e a mediana é uma medida de assimetria
    # A distância é obtida dividindo a diferença entre a média e a mediana
    # pela mediana
    # Se a distância for pequena, a distribuição é simétrica
    # Se a distância for grande, a distribuição é assimétrica
    # A distância é dada em porcentagem
    # Exemplo: 0.1 significa 10%
    # Se a distância for menor que 0.1, a distribuição tende a ser simétrica
    # Se a distância for maior que 0.1 e menor que 0.25, a distribuição tende
    # a ser assimétrica moderada. Pode ser que a média esteja sofrendo 
    # influência de valores extremos. Se a distância for maior que 0.25, a
    # distribuição tende a ser assimétrica forte. A tendência é, que nestes 
    # caso, a média esteja sofrendo influência de valores extremos.
    distancia = abs((media_recuperacao_veiculos-mediana_recuperacao_veiculos) / mediana_recuperacao_veiculos)

    # Medidas de tendência central
    # Se a média for muito diferente da mediana, distribuição é assimétrica. 
    # Não tende a haver um padrão e pode ser, que existam outliers (valores discrepantes)
    # Se a média for próxima (25%) a mediana, distribuição é simétrica. Neste 
    # caso, tende a haver um padrão
    print('\nMedidas de tendência central: ')
    print(30*'-')
    print(f'Média de recuperação de veículos: {media_recuperacao_veiculos:.2f}')
    print(f'Mediana de recuperação de veículos: {mediana_recuperacao_veiculos:.2f}')
    print(f'Distância entre média e mediana: {distancia:.2f}')


    # Quartis
    # Os quartis são os valores que dividem a distribuição em 4 partes iguais.
    # O primeiro quartil (Q1) é o valor que divide a distribuição em 25% e 75%.
    # O segundo quartil (Q2) é o valor que divide a distribuição em 50% e 50%.
    # O terceiro quartil (Q3) é o valor que divide a distribuição em 75% e 25%.
    # O quartil é uma medida de posição que indica a posição de um valor em relação
    # a uma distribuição.
    
    # OBS: O método weibull é o método padrão, mas NÃO é necessário passá-lo
    # como parâmetro ao calcular os quartis.
    # Podemos emos usar o método 'linear' ou 'hazen' também.
    # A sintaxe pode ser assim, sem os métodos:
    # q1 = np.quantile(array_roubo_veiculo, 0.25)
    # q2 = np.quantile(array_roubo_veiculo, 0.50)
    # q3 = np.quantile(array_roubo_veiculo, 0.75)
    q1 = np.quantile(array_recuperacao_veiculos, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_recuperacao_veiculos, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_recuperacao_veiculos, 0.75, method='weibull') # Q3 é 75%

    print('\nMedidas de posição: ')
    print(60*'-')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # OBTENDO AS UPPS COM MAIORES E MONORES NÚMEROS DE RECUPERAÇÕES DE VEÍCULOS
    # Filtramos os registros do DataFrame df_recuperacao_veiculos para achar os uppS
    # com menores e maiores números de recuperações de veículos.
    df_recuperacao_veiculos_menores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] < q1]
    df_recuperacao_veiculos_maiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] > q3]

    print('\nUPPs com Menores números de Recuperações de veículos: ')
    print(70*'-')
    print(df_recuperacao_veiculos_menores.sort_values(by='recuperacao_veiculos', ascending=True))
    print('\nUPPs com Maiores números de Recuperações de veículos:')
    print(70*'-')
    print(df_recuperacao_veiculos_maiores.sort_values(by='recuperacao_veiculos', ascending=False))

    # ##### DESCOBRIR OUTLIERS #########
    # IQR (Intervalo interquartil)
    # q3 - q1
    # É a amplitude do intervalo dos 50% dos dados centrais
    # Ela ignora os valores extremos.
    # Não sofre a interferência dos valores extremos.
    # Quanto mais próximo de zero, mais homogêneo são os dados.
    # Quanto mais próximo do q3, mais heterogêneo são os dados.
    iqr = q3 - q1

    # Limite superior
    # Vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # Limite inferior
    # Vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

    print('\nLimites - Medidas de Posição')
    print(60*'-')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    # #### OUTLIERS
    # Obtendo os ouliers inferiores
    # Filtrar o dataframe df_recuperacao_veiculos para o UPPs com recuperação de veículo
    # abaixo limite inferior (OUTLIERS INFERIORES)
    df_recuperacao_veiculos_outliers_inferiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] < limite_inferior]
    
    # Obtendo os ouliers superiores
    # Filtrar o dataframe df_recuperacao_veiculos para as UPPs com recuperacao_veiculos
    # acima de limite superior (OUTLIERS SUPERIORES)
    df_recuperacao_veiculos_outliers_superiores = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(60*'-')
    if len(df_recuperacao_veiculos_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_recuperacao_veiculos_outliers_inferiores.sort_values(by='recuperacao_veiculos', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(60*'-')
    if len(df_recuperacao_veiculos_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_recuperacao_veiculos_outliers_superiores.sort_values(by='recuperacao_veiculos', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de recuperação de veiculos: {e}')
    exit()