import json

try:
    with open('./teste/fones.json', 'r') as file:
        dados_carros = json.load(file)

except:
    dados_carros = []

print(f'\033[1;32m \n Existem {len(dados_carros)} carros salvos! \n \033[m')