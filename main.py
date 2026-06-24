from flask import Flask
from banco import obter_conexao

app = Flask(__name__)

@app.route('/')
def saudar():
    return 'PARABÉNS JARBAS'

@app.route('/alunos')
def listar_alunos():
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("select nome, profissao from gafanhotos;")
    alunos = cursor.fetchall()

    cursor.close()
    conn.close()

    resposta = "<h2>Alunos Cadastrados:</h2>"
    for aluno in alunos:
        resposta += f"Nome: {aluno['nome']} | Profissão: {aluno['profissao']} <br>"
        
    return resposta if len(alunos) > 0 else "Nenhum aluno encontrado."


if __name__ == "__main__":
    app.run(debug=True)