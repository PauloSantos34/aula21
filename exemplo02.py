import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    df_ocorrencias.loc[df_ocorrencias['regiao'].str.contains('Grande Niter', na=False), 'regiao'] = 'Grande Niterói'
    print(df_ocorrencias)

    # delimitando as variáveis
    
    # df_roubo_veiculo = df_ocorrencias[['regiao', 'munic', 'roubo_veiculo']]
    df_roubo_veiculo = df_ocorrencias[['regiao', 'munic', 'roubo_veiculo']]
    
    # agrupando

    df_roubo_veiculo = df_roubo_veiculo.groupby(['regiao', 'munic']).sum(['roubo_veiculo']).reset_index()

    df_regiao = df_roubo_veiculo[df_roubo_veiculo['regiao'] == 'Interior' ]

    print(df_regiao)

except Exception as e:
    print(f"Erro ao obter dados {e}")

# Medidas

try:
    
    array_roubo_veiculo = np.array(df_regiao['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia_media_mediana = abs(media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo

    # Quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)
    
    # IQR
    iqr = q3 - q1

    # limite inferior
    limite_inferior = q1 - (iqr * 1.5)

    # limite superior
    limite_superior = q3 + (iqr * 1.5)


    # ***** IMPLEMENTAR AS LINHAS (ROUBOS MAIS E MENOS) *****
    # menores roubos
    df_roubo_veiculo_menores = df_regiao[df_regiao['roubo_veiculo'] < q1]

    # maiores roubos
    df_roubo_veiculo_maiores = df_regiao[df_regiao['roubo_veiculo'] > q3]

    # Medidas de dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    variancia = np.var(array_roubo_veiculo)
    distancia_variancia_media = variancia / (media_roubo_veiculo ** 2)
    desvio_padrao = np.std(array_roubo_veiculo)
    coeficiente_variacao = desvio_padrao / media_roubo_veiculo

    assimetria = df_regiao['roubo_veiculo'].skew()
    curtose = df_regiao['roubo_veiculo'].kurtosis()
    
    # ***** IMPLEMENTAR AS LINHAS (OUTLIERS MAIORES E MENORES) *****
    # outliers inferiores
    df_roubo_veiculo_outliers_inferiores = df_regiao[df_regiao['roubo_veiculo'] < limite_inferior]
    # outiliers superiores
    df_roubo_veiculo_outliers_superiores = df_regiao[df_regiao['roubo_veiculo'] > limite_superior]


    # MEDIDAS
    print("\nMEDIAS DE TENDÊNCIA CENTRAL")
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância entre média e mediana: {distancia_media_mediana}')

    # QUARTIS
    print("\nQUARTIS")
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    # MEIDADAS DE DISPERSÃO
    print("\nMEDIDAS DE DISPERSÃO")
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude total: {amplitude_total}')
    print(f'Variancia: {variancia}')
    print(f'Distância entre variância e média: {distancia_variancia_media}')
    print(f'Desvio padrão: {desvio_padrao}')
    print(f'Coeficiente de variação: {coeficiente_variacao}')

    # MEIDADAS DE DISTRIBUIÇÃO
    print('\nMEDIDAS DE DISTRIBUIÇÃO: ')
    print(30*'-')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')


    # MAIORES E MENORES ROUBOS
    print("\nMENORES ROUBOS")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print("\nMAIORES ROUBOS")
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    
    # OUTLIERS
    # OUTLIERS INFERIORES
    print("\nOUTLIERS INFERIORES")
    if len(df_roubo_veiculo_outliers_inferiores) > 0:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=False))
    else:
        print("Não há outliers inferiores")
    
    # OUTLIERS SUPERIORES
    print("\nOUTLIERS SUPERIORES")
    if len(df_roubo_veiculo_outliers_superiores) > 0:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
    else:
        print("Não há outliers superiores")

except Exception as e:
    print(f"Erro ao obter dados {e}")

# PLOTANDO PAINEL
try:
    plt.subplots(2, 2, figsize=(18, 10))

    # "-----------------------------------------------------------"
    # Boxplot
    # "-----------------------------------------------------------"
    plt.subplot(2, 2, 1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)


    # "-----------------------------------------------------------"
    # Barras
    # Outliers superiores ou Municípios com Menores Roubos
    # "-----------------------------------------------------------"
    plt.subplot(2, 2, 2)
    if not df_roubo_veiculo_outliers_superiores.empty:
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True).head(10)
        barras = plt.barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='green')
        plt.bar_label(barras, label_type='edge', fontsize=8, padding=2)
        plt.title('Outliers Superiores')

    elif len(df_roubo_veiculo_maiores) > 1:
        dados_superiores = df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=True).head(10)
        barras = plt.barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='red')
        plt.bar_label(barras, label_type='edge', fontsize=8, padding=2)
        plt.title('Municípios com Maiores Roubos')

    else:
        # Obtém os dados da única linha
        if len(df_roubo_veiculo_maiores) == 1:
            munic = df_roubo_veiculo_maiores.iloc[0]['munic']
            roubos = df_roubo_veiculo_maiores.iloc[0]['roubo_veiculo']

            # String para printar
            texto = f"Município: {munic}\nRoubos: {roubos}"
            
            plt.text(0.5, 0.5, texto, ha='center', va='center', fontsize=12)
        
        else:
            munic = df_regiao.iloc[0]['munic']
            roubos = df_regiao.iloc[0]['roubo_veiculo']

            # String para printar
            texto = f"Município: {munic}\nRoubos: {roubos}"
            
            plt.text(0.5, 0.5, texto, ha='center', va='center', fontsize=12)
            
            # Desabilita os Eixos
            plt.xticks([])
            plt.yticks([])

            plt.title('Município com Maior Roubo')

    # "-----------------------------------------------------------"
    # Colunas
    # Outliers Iferiores ou Municípios com Menores Roubos
    # "-----------------------------------------------------------"
    plt.subplot(2, 2, 3)
    if not df_roubo_veiculo_outliers_inferiores.empty:
        dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=False).head(10)
        colunas = plt.bar(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'], color='gray')
        plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)
        # Remove os eixos originais
        plt.xticks([])

        for i, nome in enumerate(dados_inferiores['munic']):
            deslocamento = 0.7
            plt.text(i, deslocamento, nome, rotation=90, ha='center', va='bottom', fontsize=8, color='black')
        plt.title('Outliers Inferiores')

    elif len(df_roubo_veiculo_menores) > 1:
        dados_inferiores = df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True).head(10)
        colunas = plt.bar(dados_inferiores['munic'], dados_inferiores['roubo_veiculo'], color='gray')
        plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)
        # Remove os eixos originais
        plt.xticks([])

        for i, nome in enumerate(dados_inferiores['munic']):
            deslocamento = 0.7
            plt.text(i, deslocamento, nome, rotation=90, ha='center', va='bottom', fontsize=8, color='black')
        plt.title('Municípios com Menores Roubos')

    else:
        # Gráfico de colunas com todos os municípios
        df_municipios = df_regiao.sort_values(by='roubo_veiculo', ascending=False)
        colunas = plt.bar(df_municipios['munic'], df_municipios['roubo_veiculo'], color='gray')
        plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)
        # Remove os eixos originais
        plt.xticks([])

        for i, nome in enumerate(df_municipios['munic']):
            deslocamento = 0.7
            plt.text(i, deslocamento, nome, rotation=90, ha='center', va='bottom', fontsize=8, color='black')
        plt.title('Todos os Municípios')

    # "-----------------------------------------------------------"
    # Medidas
    # "-----------------------------------------------------------"
    plt.subplot(2, 2, 4)
    plt.title('Medidas Estatísticas')
    plt.text(0.1, 0.9, f'Limite inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.8, f'Menor valor: {minimo}', fontsize=10) 
    plt.text(0.1, 0.7, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.6, f'Mediana: {mediana_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.4, f'Média: {media_roubo_veiculo:.3f}', fontsize=10)
    plt.text(0.1, 0.3, f'Maior valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=10)

    plt.text(0.5, 0.9, f'Distância Média e Mediana: {distancia_media_mediana:.4f}', fontsize=10)
    plt.text(0.5, 0.8, f'IQR: {iqr}', fontsize=10)
    plt.text(0.5, 0.7, f'Amplitude Total: {amplitude_total}', fontsize=10)
    plt.text(0.5, 0.6, f'Variância: {variancia:.5f}', fontsize=10)
    plt.text(0.5, 0.5, f'Desvio Padrão: {desvio_padrao:.5f}', fontsize=10)
    plt.text(0.5, 0.4, f'Distância Média para Variância: {distancia_variancia_media:.5f}', fontsize=10)
    plt.text(0.5, 0.3, f'Coeficiente de Variação: {coeficiente_variacao:.5f}')
    plt.text(0.5, 0.2, f'Assimetria: {assimetria:.5f}')
    plt.text(0.5, 0.1, f'Curtose: {curtose:.5f}')
    
    plt.xticks([])
    plt.yticks([])
        
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro plotar painel: {e}')