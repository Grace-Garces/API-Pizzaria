from flask import Flask, jsonify

app = Flask(__name__)

# Rota simples de exemplo
@app.route('/')
def hello_world():
    return "Hello, World!"

# Endpoint de exemplo com dados fictícios
@app.route('/vendas', methods=['GET'])
def vendas():
    data = {
        "mes": "dezembro",
        "vendas_totais": 1500,
        "itens_vendidos": 300,
        "lucro": 1200
    }
    return jsonify(data)

# Se o arquivo for executado diretamente, o servidor é iniciado
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)

