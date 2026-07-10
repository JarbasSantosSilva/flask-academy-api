from flask import Flask
from routes.alunos_routes import alunos_bp
from routes.cursos_routes import cursos_bp

app = Flask(__name__)

@app.route('/')
def saudar():
    return 'Vamos Codar '

app.register_blueprint(alunos_bp)
app.register_blueprint(cursos_bp)




if __name__ == "__main__":
    app.run(debug=True)