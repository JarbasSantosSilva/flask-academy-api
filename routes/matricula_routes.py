import mysql.connector
from banco import obter_conexao
from flask import Blueprint, request,jsonify

matricula_bp = Blueprint('matricula', __name__, url_prefix='/matricula')

@matricula_bp.get('/')
def listar_matriculas():
    conn = None
    cursor = None
    try:
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""select
                m.id AS matricula_id,
                a.nome AS nome_aluno,
                c.nome AS nome_curso,
                m.data_matricula
            FROM matriculas m
            JOIN alunos a ON m.aluno_id = a.id
            JOIN cursos c ON m.curso_id = c.id;""")
        matriculas = cursor.fetchall()
        return jsonify(matriculas),200

    except mysql.connector.Error as erro_banco:
        return jsonify({"Erro":f"Erro com o banco de dados: {erro_banco}"}),500
    except Exception as erro:
        return jsonify({"Erro": f"Erro inesperado: {erro}"}),500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()