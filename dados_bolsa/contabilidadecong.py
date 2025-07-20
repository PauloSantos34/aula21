import pandas as pd
from tabulate import tabulate

def carregar_dados():
    gastos = pd.read_csv("gastos_parlamentares.csv", sep=';', encoding='utf-8')
    receitas = pd.read_csv("receitas_orcamentarias.csv", sep=';', encoding='utf-8')
    return gastos, receitas

def gerar_dre(gastos, receitas):
    dre = {}
    dre['Receita Total'] = receitas['VALOR'].sum()
    dre['Receita - Transferência da União'] = receitas[receitas['FONTE'] == 'Transferência da União']['VALOR'].sum()
    dre['Receita - Outras'] = dre['Receita Total'] - dre['Receita - Transferência da União']

    dre['Despesa com Pessoal'] = gastos[gastos['TIPO_DESPESA'].str.contains("Salário|Remuneração", case=False, na=False)]['VALOR_REEMBOLSADO'].sum()
    dre['Verbas Parlamentares'] = gastos[gastos['TIPO_DESPESA'].str.contains("verba|gabinete", case=False, na=False)]['VALOR_REEMBOLSADO'].sum()
    dre['Auxílios e Benefícios'] = gastos[gastos['TIPO_DESPESA'].str.contains("auxílio|moradia", case=False, na=False)]['VALOR_REEMBOLSADO'].sum()
    dre['Despesas com Serviços'] = gastos[~gastos['TIPO_DESPESA'].str.contains("salário|verba|auxílio", case=False, na=False)]['VALOR_REEMBOLSADO'].sum()
    dre['Resultado Orçamentário'] = dre['Receita Total'] - (
        dre['Despesa com Pessoal'] +
        dre['Verbas Parlamentares'] +
        dre['Auxílios e Benefícios'] +
        dre['Despesas com Serviços']
    )
    return dre

def exibir_dre(dre):
    print("\n🔹 Demonstração do Resultado do Exercício (DRE):")
    tabela = [[k, f"R$ {v:,.2f}"] for k, v in dre.items()]
    print(tabulate(tabela, headers=["Rubrica", "Valor"], tablefmt="grid", stralign="right"))

def main():
    gastos, receitas = carregar_dados()
    dre = gerar_dre(gastos, receitas)
    exibir_dre(dre)

if __name__ == "__main__":
    main()