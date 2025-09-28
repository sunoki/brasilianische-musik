from flask import Flask, request, jsonify, send_from_directory
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir acesso à API

# Configuração dos caminhos para os arquivos estáticos
MAIN_SITE_PATH = './brazilian-music-site'
ADMIN_SITE_PATH = './brazilian-music-admin'
JSON_PATH = './expanded-songs.json'

# Rota para o site principal
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_main_site(path):
    if path != "" and os.path.exists(os.path.join(MAIN_SITE_PATH, path)):
        return send_from_directory(MAIN_SITE_PATH, path)
    else:
        return send_from_directory(MAIN_SITE_PATH, 'index.html')

# API para obter todas as músicas (somente leitura)
@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.debug = True
    print(f"Servidor do site principal rodando em http://localhost:5000/")
    print(f"Caminho do site principal: {MAIN_SITE_PATH}")
    print(f"Caminho do arquivo JSON: {JSON_PATH}")
    
    # Verificar se o arquivo JSON existe e é acessível
    if os.path.exists(JSON_PATH):
        print(f"Arquivo JSON encontrado!")
        try:
            with open(JSON_PATH, 'r', encoding='utf-8') as file:
                json.load(file)
            print(f"Arquivo JSON válido e pode ser lido!")
        except Exception as e:
            print(f"ERRO: Arquivo JSON existe mas não pode ser lido: {str(e)}")
    else:
        print(f"AVISO: Arquivo JSON não encontrado em {JSON_PATH}")
        print(f"O arquivo JSON será criado pelo painel administrativo quando necessário.")
    
    app.run(host='0.0.0.0', port=5000)
