# Instruções para Servidores Separados

Este pacote contém três componentes principais:

1. **brazilian-music-site**: O site principal de músicas brasileiras com traduções
2. **brazilian-music-admin**: O painel administrativo para gerenciar as músicas
3. **python-server**: Contém dois servidores Python separados para evitar conflitos

## Novidades nesta versão

**Importante**: Esta versão corrige completamente o problema onde músicas adicionadas no painel administrativo não apareciam no site principal. Agora:

1. O site principal carrega os dados **exclusivamente** da API `/api/songs`
2. O mesmo arquivo JSON é compartilhado entre o site principal e o painel administrativo
3. Qualquer música adicionada ou editada no painel administrativo aparecerá automaticamente no site principal
4. Foram removidas todas as referências a arquivos JSON estáticos no frontend

## Requisitos

- Python 3.6+
- Flask (`pip install flask flask-cors`)
- Servidor web (Apache ou Nginx) para produção

## Instalação

### 1. Configuração dos Servidores Python Separados

1. Copie os arquivos da pasta `python-server` para o diretório desejado em seu servidor
2. Ajuste os caminhos nos arquivos `server_main.py` e `server_admin.py`:
   ```python
   # Em server_main.py
   MAIN_SITE_PATH = '/caminho/para/brazilian-music-site'
   JSON_PATH = '/caminho/para/expanded-songs.json'
   
   # Em server_admin.py
   ADMIN_SITE_PATH = '/caminho/para/brazilian-music-admin'
   JSON_PATH = '/caminho/para/expanded-songs.json'
   ```
   
   **IMPORTANTE**: O caminho do JSON_PATH deve ser o mesmo em ambos os arquivos para garantir a sincronização!

3. Instale as dependências: `pip install flask flask-cors`
4. Execute os dois servidores em terminais separados:
   ```bash
   # Terminal 1 - Site Principal (porta 5000)
   python server_main.py
   
   # Terminal 2 - Painel Administrativo (porta 5001)
   python server_admin.py
   ```

### 2. Configuração como Serviços (Produção)

Crie dois arquivos de serviço systemd:

```
# /etc/systemd/system/brazilian-music-main.service
[Unit]
Description=Brazilian Music Main Site
After=network.target

[Service]
User=www-data
WorkingDirectory=/caminho/para/python-server
ExecStart=/usr/bin/python3 /caminho/para/python-server/server_main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```
# /etc/systemd/system/brazilian-music-admin.service
[Unit]
Description=Brazilian Music Admin Panel
After=network.target

[Service]
User=www-data
WorkingDirectory=/caminho/para/python-server
ExecStart=/usr/bin/python3 /caminho/para/python-server/server_admin.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ative e inicie os serviços:
```bash
sudo systemctl enable brazilian-music-main
sudo systemctl start brazilian-music-main
sudo systemctl enable brazilian-music-admin
sudo systemctl start brazilian-music-admin
```

### 3. Configuração do Proxy Reverso (Nginx)

```nginx
# Site principal
server {
    listen 80;
    server_name music.seudominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Painel administrativo
server {
    listen 80;
    server_name admin-music.seudominio.com;

    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Permissões

Certifique-se de que o arquivo JSON tenha permissões de leitura e escrita para o usuário que executa o servidor:

```bash
chown www-data:www-data /caminho/para/expanded-songs.json
chmod 664 /caminho/para/expanded-songs.json
```

## Uso

- Site principal: http://localhost:5000/
- Painel administrativo: http://localhost:5001/

## Segurança

Para produção, recomenda-se:
1. Configurar HTTPS com Let's Encrypt
2. Adicionar autenticação ao painel administrativo
3. Implementar backups regulares do arquivo JSON

## Notas sobre esta versão atualizada

Esta versão utiliza dois servidores separados para evitar conflitos de roteamento e problemas de MIME. Ambos os servidores agora acessam o mesmo arquivo JSON através de APIs HTTP, garantindo que as alterações feitas no painel administrativo sejam imediatamente refletidas no site principal.
