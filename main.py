import os
from flask_cors import CORS
from flask import Flask
from banco import testar_conexao 

from routes.alunos_routes import alunos_bp
from routes.cursos_routes import cursos_bp
from routes.professor_routes import professor_bp
from routes.matricula_routes import matricula_bp
from routes.auth_routes import auth_bp


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_secreta_padrao_dev')

@app.route('/')
def saudar():
    return 'Vamos Codar'

app.register_blueprint(alunos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(matricula_bp)
app.register_blueprint(auth_bp)





if __name__ == "__main__":

    testar_conexao()

    app.run(debug=True)