import mysql.connector
from banco import obter_conexao
from flask import Blueprint, request, jsonify

professor_bp = Blueprint('professor',__name__, url_prefix='/professor')

@professor_bp.get('/')
def listar_professores():
    conn = None
    cursor = None
    try:
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from professor;")
        professor = cursor.fetchall()
        return jsonify(professor),200
    
    except mysql.connector.Error as erro_banco:
        return jsonify({"Erro": "Erro com o banco de dados." ,"Detalhes": str(erro_banco)}),500
    
    except Exception as erro:
        return jsonify({"Erro": "Erro inesperado encontrado.", "Detalhes": str(erro)}),500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
@professor_bp.post('/')
def cadastrar_professor():
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro":"Nenhum dado enviado."}),400
        
        nome = dados.get("nome")
        especialidade = dados.get("especialidade")

        if "nome" not in dados or "especialidade" not in dados:
            return jsonify({"Erro": "Dados enviados insuficientes."}),400
        
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("insert into professor (nome, especialidade) values ( %s, %s);",(nome, especialidade))
        conn.commit()
        return jsonify({"Mensagem": f"Professor {nome} , cadastrado. "}),201
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro com o banco de dados.","Detalhes": str(erro_banco)}),500
    
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro inesperado encontrado", "Detalhes": str(erro)}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@professor_bp.put('/<int:id>')
def atualizar_professor(id):    
    conn = None
    cursor = None
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "Nenhum dado enviado."}),400
        
        if "nome" not in dados or "especialidade" not in dados:
            return jsonify({"Erro": "Dados enviados insuficientes."}),400
        
        nome_novo = dados.get("nome")
        especialidade_nova = dados.get("especialidade")
        
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("update professor set nome = %s, especialidade = %s where id = %s;",(nome_novo, especialidade_nova, id))

        if cursor.rowcount == 0:
            return jsonify({"Erro": "Cadastro professor inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem": f"Professor : {nome_novo} atualizado."}),200
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro com o banco de dados","Detalhes": str(erro_banco)}),500
    except Exception as erro :
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro inesperado encontrado." ,"Detalhes": str(erro)}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@professor_bp.delete('/<int:id>')
def excluir_professor(id):
    conn = None
    cursor = None
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("delete from professor where id = %s;",(id,))

        if cursor.rowcount == 0:
            return jsonify({"Erro": "Cadastro professor inexistente."}),400
        conn.commit()
        return jsonify({"Mensagem": "Professor excluido com sucesso ."}),200
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro com o banco de dados","Detalhes": str(erro_banco)}),500
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro inesperado encontrado.","Detalhes": str(erro)}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



    
        
        

    

    
