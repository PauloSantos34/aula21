# bibliotecas necessárias
# pandas numpy matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # TODAS AS REGIÕES
# # ANÁLISE DE DADOS POR REGIÃO (CISP e MUNICÍPIO)
try:
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    # Substitui os textos com erros por 'Grande Niterói'
    df_ocorrencias.loc[df_ocorrencias['regiao'].str.contains('Grande Niter', na=False), 'regiao'] = 'Capital'

    # Delimitando as variáveis
    df_roubos_veiculos = df_ocorrencias[['munic', 'cisp', 'regiao', 'roubo_veiculo']]
    
    # Agrupando por cisp região e município
    df_roubos_veiculos = df_roubos_veiculos.groupby(['munic', 'cisp', 'regiao']).sum(['roubo_veiculo']).reset_index()

    df_roubos_veiculos = df_roubos_veiculos.sort_values(by='regiao', ascending=False)
    
    print(df_roubos_veiculos.to_string())

except Exception as e:
    print(f'Erro ao obter dados: {e}')


# Medidas
try:
    # Obtendo as regiões. Apenas valores únicos
    regioes = df_ocorrencias['regiao'].unique()

    for regiao in regioes:
        df_regiao = df_roubos_veiculos[df_roubos_veiculos['regiao'] == regiao]

        # Array Numpy
        array_roubo_veiculo = np.array(df_regiao['roubo_veiculo'])

        # Medidas de Tendência Central
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


        # menores roubos
        df_roubos_veiculos_menores = df_regiao[df_regiao['roubo_veiculo'] < q1]

        # maiores roubos
        df_roubos_veiculos_maiores = df_regiao[df_regiao['roubo_veiculo'] > q3]

        # Medidas de dispersão
        maximo = np.max(array_roubo_veiculo)
        minimo = np.min(array_roubo_veiculo)
        amplitude_total = maximo - minimo

        variancia = np.var(array_roubo_veiculo)
        distancia_variancia_media = variancia / (media_roubo_veiculo ** 2)
        desvio_padrao = np.std(array_roubo_veiculo)
        coeficiente_variacao = desvio_padrao / media_roubo_veiculo

        assimetria = df_roubos_veiculos['roubo_veiculo'].skew()
        curtose = df_roubos_veiculos['roubo_veiculo'].kurtosis()

        # outliers inferiores
        df_roubo_veiculo_outliers_inferiores = df_regiao[df_regiao['roubo_veiculo'] < limite_inferior]
        # superiores
        df_roubo_veiculo_outliers_superiores = df_regiao[df_regiao['roubo_veiculo'] > limite_superior]

        # imprime os dados
        print(30*"-")
        print(f'REGIÃO {regiao}')
        print(30*"-")
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
        print(df_roubos_veiculos_menores.sort_values(by='roubo_veiculo', ascending=True))
        print("\nMAIORES ROUBOS")
        print(df_roubos_veiculos_maiores.sort_values(by='roubo_veiculo', ascending=False))
        
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

        print('.................. Fim ........................\n')

        # ####### PLOTANDO PAINEL ##############
        try:
            # Define a variável qualitativa (munic ou cisp) e os títulos dos plots
            # com base na região, que o For está iterando.
            # Se for Capital ou Grande Niterói, os Gráficos serão criados 
            # com CISPs. As outras regiões serão com munic.
            if regiao in ['Capital', 'Grande Niterói']:
                cisp_or_munic = 'cisp'
                titulo_maiores = 'Delegacias com Maiores Registros de Roubos'
                titulo_menores = 'Delegacias com Menores Registros de Roubos'
            else:
                cisp_or_munic = 'munic'
                titulo_maiores = 'Municípios com Maiores Roubos'
                titulo_menores = 'Municípios com Menores Roubos'
            

            # Plotando o painel de 4 Plots p/ Gráfico
            plt.subplots(2, 2, figsize=(18, 10))
            # Título do Painel pega a variável regiao
            plt.suptitle(f'Análise - Região: {regiao}', fontsize=16, fontweight='bold')

            # "-----------------------------------------------------------"
            # PLOT 1: Boxplot
            # "-----------------------------------------------------------"
            plt.subplot(2, 2, 1)
            plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)


            # "-----------------------------------------------------------"
            # PLOT 2: Barras
            # "-----------------------------------------------------------"
            plt.subplot(2, 2, 2)
            # Se não estiver vazio entra no If e tenta plotar os OUTLIERS
            if not df_roubo_veiculo_outliers_superiores.empty:
                # Ordena os 5 maiores outliers em ordem decrescente
                dados_superiores_ordenados = df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False).head(5)
                dados_superiores = dados_superiores_ordenados.sort_values(by='roubo_veiculo', ascending=True)

                # Cria o gráfico de barras horizontais e garda na variável barras
                # .astype(str) Converte o número da delegacia, que é uma
                # variável qualitativa para string p/ não confundir o python
                barras = plt.barh(dados_superiores[cisp_or_munic].astype(str), dados_superiores['roubo_veiculo'], color='green')

                # .bar_label() Adiciona os rótulos (roubos_veiculos) no fim 
                # das barras, através do método com label_type='edge'.
                # fontsize e padding Formatam os rótulos tamanho da fonte e
                # afastamento da borda
                plt.bar_label(barras, label_type='edge', fontsize=8, padding=2)

                # Título que aparecerá no Plot
                plt.title('Outliers Superiores')

            # Se o dataframe tiver mais de 1 registro, entra no If
            # e desta vez, Tenta plotar os 10 maiores roubos de veículos.
            # O método len() é usado para verificar o tamanho do dataframe,
            # Se roubos_maiores for maior que 1, entra no if
            elif len(df_roubos_veiculos_maiores) > 1:
                # Ordena os maiores roubos em ordem crescente
                dados_superiores_ordenados = df_roubos_veiculos_maiores.sort_values(by='roubo_veiculo', ascending=False).head(5)
                dados_superiores = dados_superiores_ordenados.sort_values(by='roubo_veiculo', ascending=True)

                # Cria o gráfico horizontal e grava em uma variável chamada barras
                # .astype(str) serve para converter os valores a identificação
                # numérica das delegacias cisp, em string. Se não, o Python irá
                # tentar plotar os valores numéricos como se fossem medidas
                # cisp_or_munic = é uma variável de controle que servirá para determinar
                # se o gráfico será plotado com cisp ou nos munic. 
                barras = plt.barh(dados_superiores[cisp_or_munic].astype(str), dados_superiores['roubo_veiculo'], color='red')

                # .bar_label() Adiciona os rótulos (roubos_veiculos) no fim 
                # das barras, através do método com label_type='edge'.
                # fontsize e padding Formatam os rótulos tamanho da fonte e afastamento da borda
                plt.bar_label(barras, label_type='edge', fontsize=8, padding=2)
                plt.title(titulo_maiores)

            else:
                # Caso contrário,
                # Verifica se o dataframe tem apenas 1 registro
                # se o dataframe tiver apenas 1 registro, a ideia não seria
                # plotar um gráfico, mas simplesmente exibir os dados deste registro
                if len(df_roubos_veiculos_maiores) == 1:
                    # .loc é usado para acessar os dados de uma linha específica.
                    # Se, só existe uma .iloc[0]['nome_da_série'] é suficiente.
                    # Obs: Série em pandas é como se fosse uma Coluna de uma tabela
                    munic = df_roubos_veiculos_maiores.iloc[0][cisp_or_munic]
                    roubos = df_roubos_veiculos_maiores.iloc[0]['roubo_veiculo']

                    # String para printar
                    texto = f"Município: {munic}\nRoubos: {roubos}"
                    
                    # Plotar o texto no centro do gráfico. 
                    # ha e va são comandos para alinhamento horizontal e vertical
                    # O ponto (0.5, 0.5) é relativo à área do gráfico, não a pixels
                    # ha - Alinhamento Horizontal
                    # va - Alinhamento Vertical
                    plt.text(0.5, 0.5, texto, ha='center', va='center', fontsize=12)
                
                else:
                    # se o dataframe não tiver apenas um registro, então
                    # recuperamos as informações para mostrar os
                    # dados do dataframe regiao 
                    munic = df_regiao.iloc[0][cisp_or_munic]
                    roubos = df_regiao.iloc[0]['roubo_veiculo']

                    # Criando nossa String para usar como título e guardando na 
                    # variável texto
                    texto = f"Município: {munic}\nRoubos: {roubos}"
                    
                    # Plotar a variável texto no centro do gráfico.
                    # O ponto (0.5, 0.5) é relativo à área do gráfico, não a pixels
                    plt.text(0.5, 0.5, texto, ha='center', va='center', fontsize=12)
                    
                    # Desabilita os Eixos
                    plt.xticks([])
                    plt.yticks([])

                    plt.title('Município com Maior Roubo')

            # "-----------------------------------------------------------"
            # Colunas
            # "-----------------------------------------------------------"
            plt.subplot(2, 2, 3)
            # Se não estiver vazio entra no If e tenta plotar os 10 menores OUTLIERS
            if not df_roubo_veiculo_outliers_inferiores.empty:
                # Ordena os menores outliers em ordem decrescente
                dados_inferiores = df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=False)
                colunas = plt.bar(dados_inferiores[cisp_or_munic].astype(str), dados_inferiores['roubo_veiculo'], color='gray')
                plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)
                # Remove os eixos originais para exibir os novos
                plt.xticks([])

                # Percorre cada barra desenhada no gráfico de colunas (subplot 3)
                for i, bar in enumerate(colunas):
                    # Obtém a altura da barra atual (quantidade de roubos)
                    y = bar.get_height()

                    # Escreve o nome (do município ou da delegacia) dentro das barras correspondentes
                    # i → posição horizontal da barra (x)
                    # y * 0.03 → posiciona o texto pouco acima da base da barra (y baixo)
                    # rotation=90 → gira o texto na vertical
                    # ha - Alinhamento Horizontal
                    # va - Alinhamento Vertical
                    # fontsize - Tamanho da fonte
                    # padding - Espaço entre o texto e a borda da barra
                    plt.text(i, y * 0.03, dados_inferiores[cisp_or_munic].iloc[i],
                            rotation=90, ha='center', va='bottom', fontsize=8, color='black')
                plt.title('Outliers Inferiores')

            # verifica se em roubo de veículo existe mais de 1 elemento,
            # se existir, entra no if
            elif len(df_roubos_veiculos_menores) > 1:
                # Ordena os menores registros de forma decrescente
                dados_inferiores = df_roubos_veiculos_menores.sort_values(by='roubo_veiculo', ascending=True)
                # Cria o gráfico de Colunas com os dados ordenados e joga na variável colunas.
                # .astype(str) converte os dados do rótulo para string
                colunas = plt.bar(dados_inferiores[cisp_or_munic].astype(str), dados_inferiores['roubo_veiculo'], color='gray')

                # .bar_label() Adiciona os rótulos (roubos_veiculos) no fim
                # das colunas, através do método com label_type='edge'.
                # fontsize e padding Formatam os rótulos tamanho da fonte e afastamento da borda
                plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)
                
                # Remove os eixos originais
                plt.xticks([])

                # Percorre todas as colunas do gráfico (cada barra )
                for i, bar in enumerate(colunas):
                    # Obtém a altura da barra atual (quantidade de roubos registrada)
                    y = bar.get_height()

                # i → posição horizontal da barra (x)
                # y * 0.03 → posiciona o texto pouco acima da base da barra (y baixo)
                # rotation=90 → gira o texto na vertical
                # .iloc[i] retorna o nome do município ou o número da
                # delegacia cisp correspondente àquela barra específica.
                    plt.text(i, y * 0.03, dados_inferiores[cisp_or_munic].astype(str).iloc[i],
                            rotation=90, ha='center', va='bottom', fontsize=8, color='black')
                plt.title(titulo_menores)

            else:
                # Caso contrário, entra no else para mostrar todos municípios
                # Ordena em ordem decrescente e guarda em df_municipios
                df_municipios = df_regiao.sort_values(by='roubo_veiculo', ascending=False)

                # usa o df_municipios para criar o gráfico ...
                colunas = plt.bar(df_municipios[cisp_or_munic].astype(str), df_municipios['roubo_veiculo'], color='gray')

                # .bar_label() Adiciona os rótulos (roubos_veiculos) no final
                # das colunas, através do método com label_type='edge'.
                # fontsize e padding formatam os rótulos com tam da fonte
                # e afastamento das bordas
                plt.bar_label(colunas, label_type='edge', fontsize=8, padding=2)

                # Remove os eixos originais
                plt.xticks([])

                for i, bar in enumerate(colunas):
                    y = bar.get_height()
                    plt.text(i, y * 0.03, dados_inferiores[cisp_or_munic].astype(str).iloc[i],
                            rotation=90, ha='center', va='bottom', fontsize=8, color='black')
                plt.title('Todos os Municípios')

            # "-----------------------------------------------------------"
            # Medidas
            # "-----------------------------------------------------------"
            plt.subplot(2, 2, 4)

            # Plotando as medidas estatísticas
            plt.title('Medidas Estatísticas')

            # Os valores decimais são coordenadas x e y, q irão posicionar
            # os as medidas em pontos específicos do gráfico.
            # Coordenada x, é o eixo horizontal.
            # Coordenada y, é o eixo vertical.
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
            
            # Retira os eixos normais do gráfico
            plt.xticks([])
            plt.yticks([])
            
            # Ajusta os graficos dentro do layout
            plt.tight_layout()

            # Esta linha é responsável por mostrar o gráfico
            plt.show()

        except Exception as e:
            print(f'Erro plotar painel: {e}')

except Exception as e:
    print(f'Erro ao calcular medidas: {e}')
