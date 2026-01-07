"""Módulo simples para gerenciar sessão do usuário (estado in-memory)."""
_current_user = None

def login(usuario_dict):
    global _current_user
    _current_user = usuario_dict

def logout():
    global _current_user
    _current_user = None

def get_user():
    return _current_user

def get_user_id():
    if _current_user and isinstance(_current_user, dict):
        return _current_user.get("ID_Usuario")
    return None

def is_logged_in():
    return _current_user is not None
