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

@cursos_bp.patch('/<int:id>')
def atualizar_cursos_parcial(id):
    dados = request.get_json()

    if not dados :
        return jsonify({"Erro": "Nenhum dado enviado!"}),400

    campos_para_atualizar = []
    valores = []

    if "nome" in dados:
        campos_para_atualizar.append("nome = %s")
        valores.append(dados.get("nome"))
    if "carga" in dados:
        campos_para_atualizar.append("carga = %s")
        valores.append(dados.get("carga"))
    if "ano" in dados:
        campos_para_atualizar.append("ano = %s")
        valores.append(dados.get("ano"))
    if "totaulas" in dados:
        campos_para_atualizar.append("totaulas = %s")
        valores.append(dados.get("totaulas"))
    if "descricao" in dados:
        campos_para_atualizar.append("descricao = %s")
        valores.append(dados.get("descricao"))
    if not campos_para_atualizar:
        return jsonify({"Erro": "Nenhum dado enviado para atualizar!"}),400


    valores.append(id)

    comando_sql = f"update cursos set {',' .join(campos_para_atualizar)} where idcurso = %s ;"

    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(comando_sql, tuple(valores) )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"Mensagem": f"Curso com id : {id} atualizado com sucesso!"}), 200


    
                    

