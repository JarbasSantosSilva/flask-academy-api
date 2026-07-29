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

@matricula_bp.post('/')
def criar_matricula():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro":"Nenhum dado encontrado."}),400
        if "aluno_id" not in dados or "curso_id" not in dados or "data_matricula" not in dados:
            return jsonify({"Erro":"Dados enviados insuficientes."}),400
        aluno_id = dados.get("aluno_id")
        curso_id = dados.get("curso_id")
        data_matricula = dados.get("data_matricula")

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("insert into matriculas (aluno_id, curso_id, data_matricula) values (%s, %s, %s)",(aluno_id, curso_id, data_matricula))

        conn.commit()
        return jsonify({"Mensagem": "Matricula criada."}),201

    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro com o banco de dados : {erro_banco} ."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro inesperado : {erro} ."}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@matricula_bp.put('/<int:id>')
def atualizar_matricula(id):
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro":"Dados não enviados."}),400
        if "aluno_id" not in dados or "curso_id" not in dados or "data_matricula" not in dados:
            return jsonify({"Erro":"Dados enviados insuficientes."}),400
        
        novo_aluno_id = dados.get("aluno_id")
        novo_curso_id = dados.get("curso_id")
        nova_data_matricula = dados.get("data_matricula")

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("update matriculas set aluno_id = %s, curso_id = %s, data_matricula = %s where id = %s",(novo_aluno_id, novo_curso_id, nova_data_matricula, id))

        if cursor.rowcount == 0:
            return jsonify({"Erro": "Matricula inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem": "Matricula atualizada."}),200

    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro com o banco de dados : {erro_banco} ."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro inesperado : {erro}"}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@matricula_bp.delete('/<int:id>')
def deletar_matricula(id):
    conn = None
    cursor = None
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("delete from matriculas where id = %s",(id,))
        if cursor.rowcount == 0:
            return jsonify({"Erro": "Matricula inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem": "Matricula excluida. "}),200
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro com o banco de dados : {erro_banco}."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro inesperado : {erro} ."}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@matricula_bp.patch('/<int:id>')
def atualizar_parcial(id):
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro":"Nenhum dado enviado pra atualizar."}),400
        campo_para_atualizar = []
        valores = []

        if "aluno_id" in dados:
            campo_para_atualizar.append("aluno_id = %s")
            valores.append(dados.get("aluno_id"))
        if "curso_id" in dados:
            campo_para_atualizar.append("curso_id = %s")
            valores.append(dados.get("curso_id"))
        if "data_matricula" in dados:
            campo_para_atualizar.append("data_matricula = %s")
            valores.append(dados.get("data_matricula"))
        if not campo_para_atualizar:
            return jsonify({"Erro": "Nenhum dado enviado."}),400
        valores.append(id)
        comando_sql = f"update matriculas set {','.join(campo_para_atualizar)} where id = %s"

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(comando_sql, tuple(valores))
        if cursor.rowcount == 0:
            return jsonify({"Erro":"Matricula inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem":"Matricula atualizada."}),200
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro com o banco de dados : {erro_banco}."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro":f"Erro inesperado : {erro}"}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    
    





