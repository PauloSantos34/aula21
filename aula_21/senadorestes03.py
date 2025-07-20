import csv

def print_arquivo(caminho, num_linhas=15):
    print(f"\n--- Primeiras {num_linhas} linhas do arquivo: {caminho} ---\n")
    with open(caminho, encoding='latin1') as f:
        reader = csv.reader(f, delimiter=';')
        for i, row in enumerate(reader):
            print(f"Linha {i}: {row}")
            if i + 1 >= num_linhas:
                break

arquivo_ceaps = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\gastos_ceaps_2022.csv"
arquivo_inst = r"C:\Users\User\Documents\PauloSantos\aula_21\codigo\aula_21\despesas_institucional.csv"

print_arquivo(arquivo_ceaps)
print_arquivo(arquivo_inst)