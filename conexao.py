# conexao.py
import os
import mysql.connector
from mysql.connector import Error

# Conexão global (pode ser reutilizada)
_conexao_global = None

# Armazena a senha digitada para não pedir novamente
_senha_nuvem = None

_tipo_conexao_funcionando = None  # "nuvem" ou "local"

def conectar(usar_global=False, reutilizar=False):
    global _conexao_global, _senha_nuvem, _tipo_conexao_funcionando
    if usar_global and reutilizar and _conexao_global is not None:
        try:
            _conexao_global.ping()
            return _conexao_global
        except:
            _conexao_global = None
    
    # Se já sabemos qual tipo funcionou, tenta esse primeiro
    if _tipo_conexao_funcionando == "nuvem":
        con = _tentar_nuvem(usar_global)
        if con is not None:
            return con
        # Se falhar, reseta o cache e tenta local
        _tipo_conexao_funcionando = None
    
    if _tipo_conexao_funcionando == "local":
        con = _tentar_local(usar_global)
        if con is not None:
            return con
        # Se falhar, reseta o cache
        _tipo_conexao_funcionando = None
    
    # Primeira vez: tenta nuvem primeiro
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
        
        # Se a senha ainda não foi digitada, pede agora
        if _senha_nuvem is None:
            _senha_nuvem = input("🔐 Digite a senha da nuvem (Aiven): ")
        
        con = mysql.connector.connect(
            host="cineplus-fhrl-eng.b.aivencloud.com",
            port=25144,
            user="avnadmin",
            password=_senha_nuvem,
            database="cineplus",
            ssl_disabled=False,
            ssl_verify_cert=True,
            ssl_ca="ca.pem"
        )
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
    """Tenta conectar localmente"""
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
    """Fecha a conexão global se existir"""
    global _conexao_global
    if _conexao_global is not None:
        try:
            _conexao_global.close()
            _conexao_global = None
            print("✓ Conexão global fechada")
        except Error as e:
            print(f"Erro ao fechar conexão: {e}")