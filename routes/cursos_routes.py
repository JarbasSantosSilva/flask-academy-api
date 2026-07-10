from flask import Blueprint, request, jsonify
from banco import obter_conexao

cursos_bp = Blueprint('cursos',__name__, url_prefix='/cursos')

@cursos_bp.get('/')
def listar_cursos():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from cursos")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(cursos)

@cursos_bp.post('/')
def cadastrar_curso():
    dados = request.get_json()
    nome = dados.get("nome")
    carga = dados.get("carga")
    ano = dados.get("ano")
    totaulas = dados.get("totaulas")
    descricao = dados.get("descricao")

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("insert into cursos (nome, carga, ano, totaulas, descricao) values (%s, %s, %s,%s, %s);",(nome, carga, ano, totaulas, descricao))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"Aviso": f'Novo curso : {nome} adicionado!'}), 201

@cursos_bp.put('/<int:id>')
def atualizar_cursos(id):
    dados = request.get_json()
    nome_novo = dados.get("nome")
    carga_nova = dados.get("carga")
    ano_novo = dados.get("ano")
    totaulas_novo = dados.get("totaulas")
    descricao_nova = dados.get("descricao")

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("update cursos set nome = %s, carga = %s, ano = %s, totaulas = %s, descricao = %s where  idcurso = %s;",(nome_novo, carga_nova, ano_novo, totaulas_novo, descricao_nova, id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"Aviso" : f' Curso {nome_novo} atualizado com sucesso!'}), 200

@cursos_bp.delete('<int:id>')
def excluir_curso(id):

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("delete from cursos where idcurso = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"Aviso" : f'Curso com ID {id} excluido com sucesso ! '}), 200
    
                    

