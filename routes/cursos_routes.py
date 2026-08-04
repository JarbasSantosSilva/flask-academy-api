from flask import Blueprint, request, jsonify
from banco import obter_conexao
import mysql.connector
from decorators import token_requerido

cursos_bp = Blueprint('cursos',__name__, url_prefix='/cursos')

@cursos_bp.get('/')
@token_requerido
def listar_cursos():
    conn = None
    cursor = None
    try:

        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from cursos")
        cursos = cursor.fetchall()
        
        return jsonify(cursos)
    except mysql.connector.Error as erro_banco:
        return jsonify({"ERRO": "Erro com o banco de dados.", "Detalhes": str(erro_banco)}),500
    except Exception as erro :
        return jsonify({"Erro": f"Erro inesperado {str(erro)}"}),500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@cursos_bp.post('/')
@token_requerido
def cadastrar_curso():
    cursor = None
    conn = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "Nenhum dado enviado."}),400
        
        if "nome" not in dados or "carga_horaria" not in dados or "descricao" not in dados or "professor_id" not in dados:
            return jsonify({"Erro": "Envio de dados incompletos."}),400
        
        nome = dados.get("nome")
        carga_horaria = dados.get("carga_horaria")
        professor_id = dados.get("professor_id")
        descricao = dados.get("descricao")

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("insert into cursos (nome, carga_horaria, professor_id,  descricao) values (%s, %s, %s,%s);",(nome, carga_horaria, professor_id, descricao))
        conn.commit()
        
        return jsonify({"Aviso": f'Novo curso : {nome} adicionado!'}), 201
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro com banco de dados."}),500
    except Exception as erro :
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro inesperado encontrado. {str(erro)}"}),500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@cursos_bp.put('/<int:id>')
@token_requerido
def atualizar_cursos(id):
    cursor = None
    conn = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "Nenhum dado enviado."}),400
        
        if "nome" not in dados or "carga_horaria" not in dados or "professor_id" not in dados or "descricao" not in dados:
            return jsonify({"Erro": "Dados enviados insuficientes."}),400
        
        nome_novo = dados.get("nome")
        carga_nova = dados.get("carga_horaria")
        professor_id_novo = dados.get("professor_id")
        descricao_nova = dados.get("descricao")



        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("update cursos set nome = %s, carga_horaria = %s, professor_id = %s, descricao = %s where  id = %s;",(nome_novo, carga_nova, professor_id_novo, descricao_nova, id))

        if cursor.rowcount == 0:
            return jsonify({"Erro": " Curso inexistente."}),400

        conn.commit()
        return jsonify({"Aviso" : f' Curso {nome_novo} atualizado com sucesso!'}), 200
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro com o banco de dados : {str(erro_banco)}."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro inesperado encontrado: {str(erro)}."}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@cursos_bp.delete('/<int:id>')
@token_requerido
def excluir_curso(id):
    conn = None
    cursor = None

    try:

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("delete from cursos where id = %s;", (id,))

        if cursor.rowcount == 0:
            return jsonify({"Erro": "Usuário inexistente."}),400
        conn.commit()
        return jsonify({"Aviso" : f'Curso com ID {id} excluido com sucesso ! '}), 200
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro com o banco de dados: {str(erro_banco)}."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro inesperado encontrado: {str(erro)}."}),500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    

@cursos_bp.patch('/<int:id>')
@token_requerido
def atualizar_cursos_parcial(id):
    conn = None
    cursor = None
    try:
        dados = request.get_json()

        if not dados :
            return jsonify({"Erro": "Nenhum dado enviado!"}),400

        campos_para_atualizar = []
        valores = []

        if "nome" in dados:
            campos_para_atualizar.append("nome = %s")
            valores.append(dados.get("nome"))
        if "carga_horaria" in dados:
            campos_para_atualizar.append("carga_horaria = %s")
            valores.append(dados.get("carga_horaria"))
        if "professor_id" in dados:
            campos_para_atualizar.append("professor_id = %s")
            valores.append(dados.get("professor_id"))
        if "descricao" in dados:
            campos_para_atualizar.append("descricao = %s")
            valores.append(dados.get("descricao"))
        if not campos_para_atualizar:
            return jsonify({"Erro": "Nenhum dado enviado para atualizar!"}),400


        valores.append(id)

        comando_sql = f"update cursos set {',' .join(campos_para_atualizar)} where id = %s ;"

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(comando_sql, tuple(valores) )

        if cursor.rowcount == 0:
            return jsonify({"Erro": "Usuário inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem": f"Curso com id : {id} atualizado com sucesso!"}), 200
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro com o banco de dados: {str(erro_banco)}."}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro inesperado encontrado: {str(erro)}."}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    
                    

