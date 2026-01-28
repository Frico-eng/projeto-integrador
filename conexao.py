import os
from pathlib import Path
import mysql.connector
from mysql.connector import Error

_conexao_global = None
_senha_nuvem = None
_tipo_conexao_funcionando = None
_env_loaded = False

def conectar(usar_global=False, reutilizar=False):
    global _conexao_global, _senha_nuvem, _tipo_conexao_funcionando
    _load_env()
    if usar_global and reutilizar and _conexao_global is not None:
        try:
            _conexao_global.ping()
            return _conexao_global
        except:
            _conexao_global = None
    if _tipo_conexao_funcionando == "nuvem":
        con = _tentar_nuvem(usar_global)
        if con is not None:
            return con
        _tipo_conexao_funcionando = None
    
    if _tipo_conexao_funcionando == "local":
        con = _tentar_local(usar_global)
        if con is not None:
            return con
        _tipo_conexao_funcionando = None
    con = _tentar_nuvem(usar_global)
    if con is not None:
        _tipo_conexao_funcionando = "nuvem"
        return con
    
    # Se falhar na nuvem, tenta local
    con = _tentar_local(usar_global)
    if con is not None:
        _tipo_conexao_funcionando = "local"
        return con
    
    return None

def _tentar_nuvem(usar_global=False):
    """Tenta conectar à nuvem"""
    global _conexao_global, _senha_nuvem
    
    try:
        print("🌐 Tentando conexão com a nuvem...")
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASS")
        database = os.environ.get("DB_NAME")
        ssl_disabled = os.environ.get("DB_SSLD")
        ssl_verify = os.environ.get("DB_SSLV")
        ssl_ca = os.environ.get("DB_SSL_CA")
        print(host,port,user,password,database,ssl_disabled,ssl_verify,ssl_ca)
        try:
            port = int(port) if port is not None else None
        except ValueError:
            port = None

        def _bool_of(v):
            if v is None:
                return None
            return str(v).strip().lower() in ("1", "true", "yes", "y")

        ssl_disabled = _bool_of(ssl_disabled)
        ssl_verify = _bool_of(ssl_verify)

        # Se não há host/usuário/banco, não tenta nuvem
        if not host or not user or not database:
            raise ValueError("Configurações de nuvem incompletas (DB_HOST/DB_USER/DB_NAME)")

        conn_kwargs = dict(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        if port is not None:
            conn_kwargs["port"] = port
        if ssl_disabled is not None:
            conn_kwargs["ssl_disabled"] = bool(ssl_disabled)
        if ssl_verify is not None:
            conn_kwargs["ssl_verify_cert"] = bool(ssl_verify)
        if ssl_ca:
            conn_kwargs["ssl_ca"] = ssl_ca

        con = mysql.connector.connect(**conn_kwargs)
        print("✓ Conectado à nuvem com sucesso!")
        
        # Se quer usar global, armazena
        if usar_global:
            _conexao_global = con
        
        return con
    except Exception as e_cloud:
        print(f"✗ Falha na conexão com a nuvem: {e_cloud}")
        _senha_nuvem = None  # Reseta para pedir novamente
        return None

def _tentar_local(usar_global=False):
    global _conexao_global
    
    try:
        print("💾 Tentando conexão local...")
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cineplus"
        )
        print("✓ Conectado localmente com sucesso!")
        
        # Se quer usar global, armazena
        if usar_global:
            _conexao_global = con
        
        return con
    except Exception as e_local:
        print(f"✗ Falha na conexão local: {e_local}")
        return None

def fechar_conexao_global():
    global _conexao_global
    if _conexao_global is not None:
        try:
            _conexao_global.close()
            _conexao_global = None
            print("✓ Conexão global fechada")
        except Error as e:
            print(f"Erro ao fechar conexão: {e}")


def _load_env():
    """Carrega variáveis do arquivo .env para os.environ (não sobrescreve variáveis já definidas)."""
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True

    # Procura por arquivos .env em locais prováveis
    candidates = [
        Path.cwd() / '.env',
        Path.cwd() / 'telas' / '.env',
        Path.cwd() / 'utilidades' / '.env',
    ]
    env_path = None
    for p in candidates:
        if p.exists():
            env_path = p
            break
    if env_path is None:
        return

    try:
        for line in env_path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip()
            # Remove optional surrounding quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            # Só define se não existir
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception:
        # Falhar silenciosamente; fallback continuará funcionando
        return