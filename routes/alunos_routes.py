from flask import Blueprint, request, jsonify
from banco import obter_conexao

alunos_bp = Blueprint('gafanhotos',__name__,url_prefix='/gafanhotos')

@alunos_bp.get('/')
def listar_alunos():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("select nome, profissao, sexo from gafanhotos ;")
    gafanhotos = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(gafanhotos)
        
@alunos_bp.post('/')
def cadastrar_aluno():

    dados = request.get_json()

    nome = dados.get("nome")
    profissao = dados.get("profissao")
    sexo = dados.get("sexo")
    
    
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute(
        "insert into gafanhotos (nome, profissao, sexo) values (%s, %s, %s)",
          (nome, profissao, sexo) )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": f'Aluno {nome} cadastrado com sucesso!'}), 201

@alunos_bp.put('/<int:id>')
def atualizar_aluno(id):
    dados = request.get_json()
    nome_novo = dados.get("nome")
    profissao_nova = dados.get("profissao")
    sexo_novo = dados.get("sexo")

    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute("update gafanhotos set nome = %s, profissao = %s, sexo = %s where id = %s ;",(nome_novo, profissao_nova, sexo_novo,id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"Mensagem": f'Aluno com nome {nome_novo} atualizado.'}),200

@alunos_bp.delete('/<int:id>')
def deletar_aluno(id):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("delete from gafanhotos where id = %s;",(id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"Aviso": f'Aluno {id} excluido com sucesso!'}), 200
