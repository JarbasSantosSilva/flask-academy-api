import jwt
import os
from functools import wraps
from flask import request, jsonify

def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"Erro": "Token ausente!"}),401

        try:
            token_limpo = token.replace('Bearer', '').strip()
            chave_secreta = os.getenv('JWT_SECRET_KEY','chave_secreta_padrao')
            dados_payload = jwt.decode(token_limpo, chave_secreta , algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return jsonify({"Erro": "Token expirado!"}),401
        except jwt.InvalidTokenError:
            return jsonify({"Erro":"Token inválido!"}),401

        return f(dados_payload, *args, **kwargs)
    return decorated