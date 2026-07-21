from flask import Blueprint, request, jsonify
from banco import obter_conexao
import mysql.connector

alunos_bp = Blueprint('alunos',__name__,url_prefix='/alunos')

@alunos_bp.get('/')
def listar_alunos():
    conn = None
    cursor = None


    try:
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("select * from alunos;")
        alunos = cursor.fetchall()

        return jsonify(alunos)
    except mysql.connector.Error as erro_banco:
        return jsonify({"Erro": "Erro no banco de dados", "Detalhes": str(erro_banco)}),500
    
    except Exception as erro_generico:
        return jsonify({"Erro": "Ocorreu um erro inesperado no servidor", "Detalhes": str(erro_generico)}),500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
@alunos_bp.post('/')
def cadastrar_aluno():
    conn = None
    cursor = None



    try:
        dados = request.get_json()

        if dados is None:
            return jsonify({"Erro": "O corpo da requisição precisa ser um JSON válido."}),400

        nome = dados.get("nome")
        email = dados.get("email")
        data_cadastro = dados.get("data_cadastro")
        
        if "nome" not in dados or "email" not in dados or "data_cadastro" not in dados:
            return jsonify({"Erro": "Campo obrigatório faltando para o cadastro."}),400
        
        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute(
            "insert into alunos (nome, email, data_cadastro) values (%s, %s, %s)",
            (nome, email, data_cadastro) )
        conn.commit()
        return jsonify({"mensagem": f'Aluno {nome} cadastrado com sucesso!'}), 201
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"Erro": "Erro no banco de dados ao inserir.", "Detalhes": str(erro_banco)}),500
    
    except Exception as erro_generico:
        if conn:
            conn.rollback()
        return jsonify({"Erro ": "Erro interno encontrado ","Detalhes": str(erro_generico) }),500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@alunos_bp.put('/<int:id>')
def atualizar_aluno(id):
    conn = None
    cursor = None

    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"ERRO": "Nenhum dado foi enviado."}),400
        
        if "nome" not in dados or "email" not in dados or "data_cadastro" not in dados:
            return jsonify({"ERRO": "Dados insuficientes"}),400
        
        nome_novo = dados.get("nome")
        email_novo = dados.get("email")
        data_cadastro_novo = dados.get("data_cadastro")

        conn = obter_conexao()
        cursor = conn.cursor()

        cursor.execute("update alunos set nome = %s, email = %s, data_cadastro = %s where id = %s ;",(nome_novo, email_novo, data_cadastro_novo, id))

        if cursor.rowcount == 0:
            return jsonify({"ERRO": "Aluno inexistente"})
        
        conn.commit()
        return jsonify({"Mensagem": f'Aluno com nome {nome_novo} atualizado.'}),200
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"ERRO": f"Houve um erro com o banco de Dados.{str(erro_banco)}"}),500
    
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"ERRO": f"Erro inesperado , Detalhes : {str(erro)}"}),500
    

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@alunos_bp.delete('/<int:id>')
def deletar_aluno(id):
    cursor = None
    conn = None
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("delete from alunos where id = %s;",(id,))

        linhas_deletadas = cursor.rowcount
        print(f'{linhas_deletadas} Linhas deletadas.')

        if  linhas_deletadas == 0:
            return jsonify({"ERRO": "Aluno inexistente."}),400
        
        conn.commit()
        return jsonify({"Aviso": f'Aluno {id} excluido com sucesso!'}), 200
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"ERRO": "Erro com o banco de dados", "Detalhes": str(erro_banco)}),500
    
    except Exception as erro:
        if conn :
            conn.rollback()
        return jsonify({"ERRO": "Erro inesperado ","Detalhes": str(erro)}),500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@alunos_bp.patch('/<int:id>')
def atualizacao_parcial(id):
    conn = None
    cursor = None
    try:

        dados = request.get_json()

        if not dados:
            return jsonify({"ERRO": "Nenhum dado encontrado."}),400
        
        campo_para_atualizar = []
        valores = []

        if "nome" in dados:
            campo_para_atualizar.append("nome = %s")
            valores.append(dados.get("nome"))
        
        if "email" in dados:
            campo_para_atualizar.append("email = %s")
            valores.append(dados.get("email"))
        
        if "data_cadastro" in dados:
            campo_para_atualizar.append("data_cadastro = %s")
            valores.append(dados.get("data_cadastro"))
        
        if not campo_para_atualizar :
            return jsonify({"ERRO": "Nenhum campo para atualizar."}),400
        
        valores.append(id)

        comando_sql = f"update alunos set {','.join(campo_para_atualizar)} where id = %s;"

        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(comando_sql, tuple(valores) )
        if cursor.rowcount == 0:
            return jsonify({"ERRO": f"Aluno ID {id} Inexistente."}),400
        
        conn.commit()


        
        
        return jsonify({"Aviso": f"Aluno ID {id} atualizado com sucesso."})
    
    except mysql.connector.Error as erro_banco:
        if conn:
            conn.rollback()
        return jsonify({"ERRO": f"Erro com o banco de dados: {erro_banco}"}),500
        
    except Exception as erro:
        if conn:
            conn.rollback()
        return jsonify({"Erro": f"Erro Inesperado : {erro}"}),500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


    
