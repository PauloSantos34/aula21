# Importa a biblioteca Matplotlib para criar os gráficos
# pip install matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import seaborn as sns 

try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # Demilitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_ocorrencias = df_ocorrencias[['munic', 'roubo_veiculo']]

    # Totalizar roubo de veiculo por municipio (agrupar e somar)
    df_roubo_veiculo = df_ocorrencias.groupby('munic').sum(['roubo_veiculo']).reset_index()
    print(df_roubo_veiculo.head())

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Inicando a obtenção das medidas fundamentadas em estatística descritiva
try:
    print('Obtendo informações sobre padrão de roubo de veículos...')

    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    # Obtendo média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    # Obtendo mediana de roubo_veiculo
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    # Distânicia entre média e mediana
    distancia = abs((media_roubo_veiculo-mediana_roubo_veiculo) / mediana_roubo_veiculo)


    # QUARITIS
    # Podemos emos usar o método 'linear' ou 'hazen' também.
    q1 = np.quantile(array_roubo_veiculo, 0.25, method='weibull') # Q1 é 25% 
    q2 = np.quantile(array_roubo_veiculo, 0.50, method='weibull') # Q2 é 50% (mediana)
    q3 = np.quantile(array_roubo_veiculo, 0.75, method='weibull') # Q3 é 75%


    # A amplitude total é a diferença entre o maior e o menor valor de
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    # OBTENDO OS MUNÍCIPIOS COM MAIORES E MONORES NÚMEROS DE ROUBOS DE VEÍCULOS
    # Filtramos os registros do DataFrame df_roubo_veiculo para achar os municípios com menores e maiores números de roubos de veículos.
    df_roubo_veiculo_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < q1]
    df_roubo_veiculo_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > q3]


    # IQR (Intervalo interquartil)
    # É a amplitude do intervalo dos 50% dos dados centrais
    iqr = q3 - q1

    # Limite superior: Vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)

    # Limite inferior:  Vai identificar os outliers abaixo de q1
    limite_inferior = q1 - (1.5 * iqr)

    # MEDIDAS DE DISPERSÃO
    # Indicam a variabilidade de um conjunto de dados em relação à média aritmética
    # VARIÂNCIA: É a média dos quadrados das diferenças entre cada valor e a média
    variancia = np.var(array_roubo_veiculo)

    # Distância da variância p/ média
    distancia_var_media = variancia / (media_roubo_veiculo ** 2)

    # Desvio padrão: Quanto os dados estão afastados da média (p/ mais ou p/ menos)
    desvio_padrao = np.std(array_roubo_veiculo)

    # Coeficiente de Variação: É a magnitude do desvio padrão
    coef_variacao = desvio_padrao / media_roubo_veiculo

    # Assimetria
    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()




    print('\nMunicípios com Menores números de Roubos: ')
    print(70*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print('\nMunicípios com Maiores números de Roubos:')
    print(45*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))

    # PRINTANDO AS MEDIDAS
    print('\nPRINTANDO AS MEDIDAS: ')
    print(30*'-')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Mínimo: {minimo}')
    print(f'1º Quartil: {q1}')
    print(f'2º Quartil: {q2}')  # Mediana
    print(f'3º Quartil: {q3}')
    print(f'IQR: {iqr}')
    print(f'Máximo: {maximo}')
    print(f'Limite Superior: {limite_superior}')
    
    print('\nOUTRAS AS MEDIDAS: ')
    print(30*'-')
    print(f'Amplitude Total: {amplitude_total}')
    print(f'Média: {media_roubo_veiculo:.3f}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média e Mediana: {distancia:.4f}')

    print('\nPRINTANDO AS MEDIDAS: ')
    print(30*'-')
    print(f"Variância: {variancia}")
    print(f"Distância entre variância e média: {distancia_var_media}")
    print(f"Desvio Padrão: {desvio_padrao}")
    print(f"Coeficiente de Variação: {coef_variacao}")

    print('\nMedidas de Distribuição: ')
    print(30*'-')
    print(f"Assimetria: {assimetria}")
    print(f"Curtose: {curtose}")

    # #### OUTLIERS
    # abaixo limite inferior (OUTLIERS INFERIORES)
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    
    # Obtendo os ouliers superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]

    print('\nMunicípios com outliers inferiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
    else:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))

    print('\nMunicípios com outliers superiores: ')
    print(45*'-')
    if len(df_roubo_veiculo_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
    else:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))

except Exception as e:
    print(f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()




# try:
#     sns.kdeplot(df_roubo_veiculo['roubo_veiculo'], bw_adjust=3)
# except Exception as e:
#     print(f"Erro ao plotar {e}")

# PLOTANDO GRÁFICO
# Matplotlib
try:
    # import matplotlib.pyplot as plt    
    plt.subplots(2, 2, figsize=(18, 12))
    plt.suptitle('Análise de roubo de veículos no RJ') 

    # POSIÇÃO 01
    # BOXPLOT
    plt.subplot(2, 2, 1)  
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # POSIÇÃO 02
    # MEDIDAS 
    plt.subplot(2, 2, 2)
    plt.title('Medidas Estatísticas')
    plt.text(0.1, 0.9, f'Limite inferior: {limite_inferior}', fontsize=10)
    plt.text(0.1, 0.8, f'Menor valor: {minimo}', fontsize=10) 
    plt.text(0.1, 0.7, f'Q1: {q1}', fontsize=10)
    plt.text(0.1, 0.6, f'Mediana: {mediana_roubo_veiculo}', fontsize=10)
    plt.text(0.1, 0.5, f'Q3: {q3}', fontsize=10)
    plt.text(0.1, 0.4, f'Média: {media_roubo_veiculo:.3f}', fontsize=10)
    plt.text(0.1, 0.3, f'Maior valor: {maximo}', fontsize=10)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=10)

    plt.text(0.5, 0.9, f'Distância Média e Mediana: {distancia:.4f}', fontsize=10)
    plt.text(0.5, 0.8, f'IQR: {iqr}', fontsize=10)
    plt.text(0.5, 0.7, f'Amplitude Total: {amplitude_total}', fontsize=10)
    plt.text(0.5, 0.6, f'Variância: {variancia:.4f}', fontsize=10)
    plt.text(0.5, 0.5, f'Distancia da média e Variância: {distancia_var_media}', fontsize=10)
    plt.text(0.5, 0.4, f'Coeficiente de Variação: {coef_variacao}', fontsize=10)
    plt.text(0.5, 0.3, f'Desvio Padrão: {desvio_padrao:.4f}', fontsize=10)
    
    plt.xticks([])
    plt.yticks([])
    

    # POSIÇÃO 03
    # HISTOGRAMA DA DISTRIBUIÇÃO
    plt.subplot(2, 2, 3)
    plt.title('Concentração das Distribuições')
    # Histograma
    plt.hist(array_roubo_veiculo, bins=77, color='black')

    
    # POSIÇÃO 04
    # OUTLIERS SUPERIORES
    plt.subplot(2, 2, 4)
    plt.title('Outliers Superiores')
    if not df_roubo_veiculo_outliers_superiores.empty:
        dados_superiores = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=True)

        # Cria o gráfico e guarda as barras
        barras = plt.barh(dados_superiores['munic'], dados_superiores['roubo_veiculo'], color='black')
        # Adiciona rótulos nas barras
        plt.bar_label(barras, fmt='%.0f', label_type='edge', fontsize=8, padding=2)


        # Diminui o tamanho da fonte dos eixos
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)

        plt.title('Outliers Superiores')
        plt.xlabel('Total Roubos de Veículos')    
    else:
        # Se não houver outliers superiores, exibe uma mensagem no lugar.
        plt.text(0.5, 0.5, 'Sem outliers superiores', ha='center', va='center', fontsize=12)
        plt.title('Outliers Superiores')
        plt.xticks([])
        plt.yticks([])

    # Ajusta os espaços do layout para que os gráficos não fiquem espremidos
    plt.tight_layout()
    # Mostra o painel
    plt.show()
    
except Exception as e:
    print(f'Erro ao plotar {e}')
    exit()
