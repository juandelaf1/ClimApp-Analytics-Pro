"""
API Key Authentication - ClimApp-Analytics-Pro
============================================
Simple API key authentication for protected endpoints.
"""

import os
import secrets
import hashlib
from functools import wraps
from flask import request, jsonify


class APIKeyAuth:
    """Simple API key authentication."""
    
    def __init__(self):
        self._keys = {}
    
    def generate_key(self, user_email: str) -> str:
        """Genera una nueva API key para un usuario."""
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        self._keys[key_hash] = {
            'email': user_email,
            'key': api_key,
            'created': __import__('datetime').datetime.now()
        }
        return api_key
    
    def validate_key(self, api_key: str) -> bool:
        """Valida una API key."""
        if not api_key:
            return False
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        return key_hash in self._keys
    
    def get_user(self, api_key: str) -> dict:
        """Obtiene usuario de una API key."""
        if not api_key:
            return None
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        return self._keys.get(key_hash)
    
    def revoke_key(self, api_key: str) -> bool:
        """Revoca una API key."""
        if not api_key:
            return False
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()[:16]
        if key_hash in self._keys:
            del self._keys[key_hash]
            return True
        return False


# Instancia global
_api_auth = None


def get_api_auth() -> APIKeyAuth:
    """Obtiene instancia singleton."""
    global _api_auth
    if _api_auth is None:
        _api_auth = APIKeyAuth()
    return _api_auth


def require_api_key(f):
    """Decorador para requerir API key."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        # Check header X-API-Key
        api_key = request.headers.get('X-API-Key')
        
        # Also check query param
        if not api_key:
            api_key = request.args.get('api_key')
        
        # Allow if no key required in config
        if not os.getenv('REQUIRE_API_KEY', 'false').lower() == 'true':
            return f(*args, **kwargs)
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'sugerencia': 'Incluye header X-API-Key o param ?api_key='
            }), 401
        
        auth = get_api_auth()
        if not auth.validate_key(api_key):
            return jsonify({
                'error': 'API key inválida'
            }), 403
        
        return f(*args, **kwargs)
    
    return wrapped


def require_admin(f):
    """Decorador para requerir rol admin."""
    @wraps(f)
    @require_api_key
    def wrapped(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        user = get_api_auth().get_user(api_key)
        
        if user.get('rol') != 'admin':
            return jsonify({
                'error': 'Se requiere rol admin'
            }), 403
        
        return f(*args, **kwargs)
    
    return wrapped