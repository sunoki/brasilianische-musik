from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Configuração dos caminhos para os arquivos estáticos
MAIN_SITE_PATH = '/var/www/html/brazilian-music-site'
ADMIN_SITE_PATH = '/var/www/html/brazilian-music-admin'
JSON_PATH = '/var/www/html/expanded-songs.json'

# Rota para o site principal
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_main_site(path):
    if path.startswith('admin'):
        return serve_admin_site(path[6:])
        
    if path != "" and os.path.exists(os.path.join(MAIN_SITE_PATH, path)):
        return send_from_directory(MAIN_SITE_PATH, path)
    else:
        return send_from_directory(MAIN_SITE_PATH, 'index.html')

# Rota para o painel administrativo
@app.route('/admin/', defaults={'path': ''})
@app.route('/admin/<path:path>')
def serve_admin_site(path):
    if path != "" and os.path.exists(os.path.join(ADMIN_SITE_PATH, path)):
        return send_from_directory(ADMIN_SITE_PATH, path)
    else:
        return send_from_directory(ADMIN_SITE_PATH, 'index.html')

# API para obter todas as músicas
@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {str(e)}")
        return jsonify({"error": str(e)}), 500

# API para salvar todas as músicas
@app.route('/api/songs', methods=['POST'])
def save_songs():
    try:
        data = request.json
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return jsonify({"success": True})
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.debug = True
    print(f"Servidor rodando em http://localhost:5000/")
    print(f"Site principal: http://localhost:5000/")
    print(f"Painel administrativo: http://localhost:5000/admin/")
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
        print(f"Criando um arquivo JSON de exemplo...")
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
        
        # Criar um arquivo JSON de exemplo
        exemplo_json = [
            {
                "artist": "Exemplo",
                "title": {
                    "original": "Música de Exemplo",
                    "translated": "Beispiellied"
                },
                "lyrics": {
                    "original": "Letra de exemplo em português",
                    "translated": "Beispieltext auf Deutsch"
                },
                "links": {
                    "youtube": "https://www.youtube.com/watch?v=exemplo",
                    "spotify": "https://open.spotify.com/track/exemplo"
                },
                "description": "Esta é uma música de exemplo",
                "tags": ["exemplo", "teste"]
            }
        ]
        
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(exemplo_json, file, ensure_ascii=False, indent=2)
        print(f"Arquivo JSON de exemplo criado em {JSON_PATH}")
    
    app.run(host='0.0.0.0', port=5000)
