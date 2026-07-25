from flask import Flask
from routes.alunos_routes import alunos_bp
from routes.cursos_routes import cursos_bp
from routes.professor_routes import professor_bp
from routes.matricula_routes import matricula_bp


app = Flask(__name__)

@app.route('/')
def saudar():
    return 'Vamos Codar '

app.register_blueprint(alunos_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(matricula_bp)




if __name__ == "__main__":
    app.run(debug=True)