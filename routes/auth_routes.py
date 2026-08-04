import os
import jwt
import datetime
import mysql.connector
from banco import obter_conexao
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth',__name__, url_prefix='/auth')

@auth_bp.post('/cadastro')
def cadastrar_aluno():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro":"Nenhum dado enviado."}),400
        if "login" not in dados or "senha" not in dados:
            return jsonify({"Erro":"Campos obrigatórios faltando."}),400
        if not str(dados.get("login")).strip() or not str(dados.get("senha")).strip():
            return jsonify({"Erro":"Login e senha são obrigatórios."}),400

        login = dados.get("login").strip()
        senha = dados.get("senha").strip()
        aluno_id = dados.get("aluno_id")
        nivel_acesso = dados.get("nivel_acesso","aluno")

        senha_hash = generate_password_hash(senha)

        conn = obter_conexao()
        cursor = conn.cursor()
        sql = "insert into usuarios (login, senha, aluno_id, nivel_acesso) values (%s, %s, %s, %s)"
        cursor.execute(sql, (login, senha_hash, aluno_id, nivel_acesso))
        conn.commit()
        return jsonify({"Mensagem": "Usuário cadastrado com sucesso."}),201

    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        if erro_banco.errno == 1062:
            return jsonify({"erro": "Este login já está cadastrado."}),409
        return jsonify({"Erro": f"Erro com o banco de dados : {erro_banco} ."}),500

    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro inesperado encontrado : {erro}."}),500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@auth_bp.post('/login')
def login():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados or not dados.get('login') or not dados.get('senha'):
            return jsonify({"Erro":"Login e senha são dados obrigatórios."}),400

        login_usuario = dados.get('login').strip()
        senha_digitada = dados.get('senha').strip()

        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        sql = "select * from usuarios where login = %s "
        cursor.execute(sql, (login_usuario,))
        usuario = cursor.fetchone()

        if not usuario or not check_password_hash(usuario['senha'], senha_digitada):
            return jsonify({"Erro":"Credenciais inválidas."}),401

        tempo_expiracao = datetime.datetime.now(datetime.timezone.utc) + (datetime.timedelta(hours = 8))
        payload = {
            'sub': usuario['id'],
            'login':usuario['login'],
            'nivel_acesso': usuario['nivel_acesso'],
            'exp': tempo_expiracao
        }

        chave_secreta = os.getenv('JWT_SECRET_KEY', 'chave_secreta_padrao')
        token = jwt.encode(payload, chave_secreta, algorithm='HS256')

        return jsonify({"Mensagem": "Login realizado com sucesso!", "token" : token }),200

    except mysql.connector.Error as erro_banco:
        return jsonify({"Erro": f"Erro na base de dados: {erro_banco}"}),500
    except Exception as erro:
        return jsonify({"Erro":f"Erro inesperado: {erro}"}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()








