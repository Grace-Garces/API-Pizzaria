from flask import Flask, jsonify, request
import pandas as pd
import os
import json

# Defina 'dados' no escopo global
dados = {}

# Caminho da pasta onde estão os arquivos
caminho_pasta = r"C:\Users\Grace.Garces\Documents\Projeto Estudos\Dados\Relatório Vendas\DadosAPI-Pizzaria"

# Lista com os nomes dos arquivos (incluindo CSV e JSON)
arquivos = [
    "CARDAPIO - MENOS VENDIDO.json",
    "Cardápio 3 meses.csv",
    "Cardápio menos vendas 3 meses.csv",
    "COMPLEMTNO MENOS VENDID.json",
    "CONVERSÃO CARDAPIO MENOS VENDIDO.json",
    "Dias mais vendas 3 meses.csv",
    "excel2json-1734013232540.json",
    "excel2json-1734013237394.json",
    "excel2json-1734013241724.json",
    "Horario mais vendas 3 meses.csv",
    "Vendas 3 meses.csv",
    "excel2json-1734012907123.json",
    "excel2json-1734012912660.json",
    "excel2json-1734012915763.json"
]

# Função para carregar arquivos
def carregar_arquivo(arquivo):
    caminho_completo = os.path.join(caminho_pasta, arquivo)
    try:
        # Verificar a extensão do arquivo e carregar adequadamente
        if arquivo.endswith('.csv'):
            return pd.read_csv(caminho_completo)
        elif arquivo.endswith('.json'):
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                return pd.json_normalize(json.load(f))  # Normaliza o JSON em formato de DataFrame
        else:
            # Se o arquivo for Excel
            return pd.read_excel(caminho_completo, engine='openpyxl')
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")
        return None

# Carregar todos os arquivos
for arquivo in arquivos:
    nome_chave = os.path.splitext(arquivo)[0]  # Nome sem extensão
    dados[nome_chave] = carregar_arquivo(arquivo)

app = Flask(__name__)

# Rota para a raiz
@app.route('/')
def home():
    return "Bem-vindo ao servidor Flask!"

# Rota para listar os nomes dos arquivos disponíveis
@app.route('/arquivos', methods=['GET'])
def listar_arquivos():
    return jsonify(list(dados.keys()))

# Rota para acessar os dados de um arquivo específico
@app.route('/dados/<nome_arquivo>', methods=['GET'])
def obter_dados(nome_arquivo):
    if nome_arquivo not in dados:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    return jsonify(dados[nome_arquivo].to_dict(orient='records'))

# Rota para filtrar dados de um arquivo específico
@app.route('/dados/<nome_arquivo>/<coluna>/<valor>', methods=['GET'])
def filtrar_dados(nome_arquivo, coluna, valor):
    if nome_arquivo not in dados:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    df = dados[nome_arquivo]
    if coluna not in df.columns:
        return jsonify({"erro": f"Coluna '{coluna}' não encontrada no arquivo '{nome_arquivo}'"}), 400
    resultado = df[df[coluna].astype(str) == valor]
    return jsonify(resultado.to_dict(orient='records'))

# Rota para adicionar um dado a um arquivo específico
@app.route('/dados/<nome_arquivo>', methods=['POST'])
def adicionar_dado(nome_arquivo):
    if nome_arquivo not in dados:
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    novo_dado = request.json
    dados[nome_arquivo] = pd.concat([dados[nome_arquivo], pd.DataFrame([novo_dado])], ignore_index=True)
    return jsonify({"mensagem": "Dado adicionado com sucesso!"}), 201

# Rota para salvar alterações em todos os arquivos (agora suporta CSV e JSON)
@app.route('/salvar', methods=['POST'])
def salvar_arquivos():
    for nome_arquivo, df in dados.items():
        caminho_arquivo = os.path.join(caminho_pasta, f"{nome_arquivo}.xlsx")
        try:
            if nome_arquivo.endswith('.csv'):
                df.to_csv(caminho_arquivo.replace('.xlsx', '.csv'), index=False)
            elif nome_arquivo.endswith('.json'):
                df.to_json(caminho_arquivo.replace('.xlsx', '.json'), orient='records', lines=True)
            else:
                df.to_excel(caminho_arquivo, index=False, engine='openpyxl')  # Para arquivos Excel
        except Exception as e:
            print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")
    return jsonify({"mensagem": "Alterações salvas em todos os arquivos!"})

# Rota para o favicon (opcional)
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Resposta vazia com status 204 (Sem conteúdo)

if __name__ == '__main__':
    app.run(debug=True)
