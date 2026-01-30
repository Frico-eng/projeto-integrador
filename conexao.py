import os
from pathlib import Path
import mysql.connector
from mysql.connector import Error

# Variáveis globais
_conn = None  # Conexão ativa
_last_successful_type = None  # Tipo da última conexão bem-sucedida
_env_loaded = False

def conectar(reutilizar=True):
    global _conn, _last_successful_type
    conn = _conectar_nuvem()
    if conn:
        return conn
    else:  # local
        conn = _conectar_local()
        if conn:
            return conn
        else:
            print("✗ Todas as tentativas de conexão falharam")
            return None

def _conectar_nuvem():
    try:
        # Timeouts curtos para tentativa rápida
        conn_params = {
            'host': os.environ.get('DB_HOST'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASS', ''),
            'database': os.environ.get('DB_NAME'),
            'port': int(os.environ.get('DB_PORT', 3306)),
            'connection_timeout': 5,
            'connect_timeout': 5,
        }
        
        # SSL configurado apenas se necessário
        ssl_disabled = os.environ.get('DB_SSLD', '').lower() in ('1', 'true', 'yes')
        if ssl_disabled:
            conn_params['ssl_disabled'] = True
        
        # Tenta conexão rápida
        return mysql.connector.connect(**conn_params)
    except Exception as e:
        # Log curto
        if "timeout" in str(e).lower():
            print("⏱️ Timeout nuvem")
        return None

def _conectar_local():
    """Tenta conectar ao banco local"""
    try:
        print("💻 Tentando conexão local...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cineplus"
        )
        return conn
    except Exception as e:
        print(f"✗ Falha na conexão local: {e}")
        return None

def fechar():
    """Fecha a conexão atual"""
    global _conn
    if _conn:
        try:
            _conn.close()
        except:
            pass
        finally:
            _conn = None
            _last_successful_type = None
    print("✓ Conexão fechada")

def _load_env():
    """Carrega variáveis do arquivo .env"""
    global _env_loaded
    if _env_loaded:
        return
    
    _env_loaded = True
    
    # Procura arquivo .env em diretórios comuns
    env_paths = [
        Path.cwd() / '.env',
        Path.cwd() / 'telas' / '.env',
        Path.cwd() / 'utilidades' / '.env',
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                for line in env_path.read_text(encoding='utf-8').splitlines():
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove aspas
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    # Só define se não existir
                    if key and key not in os.environ:
                        os.environ[key] = value
                
                print(f"✓ Variáveis carregadas de: {env_path}")
                return
            except Exception as e:
                print(f"⚠️ Erro ao ler {env_path}: {e}")

def resetar_conexao():
    """Reseta a conexão, forçando nova tentativa na próxima chamada"""
    global _conn, _last_successful_type
    fechar()
    _last_successful_type = None
    print("✓ Conexão resetada - próxima tentativa começará do início")

# Função auxiliar para verificar status
def status():
    """Retorna status atual da conexão"""
    if _conn is None:
        return "Desconectado"
    elif _conn.is_connected():
        return f"Conectado ({_last_successful_type})"
    else:
        return "Conexão inválida"