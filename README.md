Flask Academy API

API desenvolvida com Python, Flask e MySQL para praticar conceitos de desenvolvimento backend e gerenciamento de uma plataforma acadêmica.


Status: projeto de estudo em evolução.

Sobre o projeto

A Flask Academy API organiza informações acadêmicas relacionadas a alunos, cursos, professores e matrículas.
O projeto foi desenvolvido para praticar a criação de aplicações web com Flask, integração com banco de dados relacional, organização de rotas, autenticação e operações CRUD.

A aplicação utiliza Blueprints para separar as rotas por domínio e protege os principais recursos com autenticação baseada em token JWT.

Funcionalidades atuais

•
Cadastro e login de usuários.

•
Geração de token JWT após o login.

•
Proteção de rotas com token no formato Bearer.

•
Cadastro, consulta, atualização completa, atualização parcial e exclusão de alunos.

•
Cadastro, consulta, atualização completa, atualização parcial e exclusão de cursos.

•
Cadastro, consulta, atualização e exclusão de professores.

•
Criação, consulta, atualização completa, atualização parcial e exclusão de matrículas.

•
Integração com banco de dados MySQL.

•
Hash de senhas utilizando Werkzeug.

•
Configuração de variáveis de ambiente com python-dotenv.

•
Compartilhamento de recursos entre origens por meio do Flask-CORS.

Tecnologias utilizadas

Tecnologia
Utilização
Python
Linguagem principal do projeto.
Flask
Criação da aplicação web e das rotas.
MySQL
Persistência dos dados acadêmicos.
mysql-connector-python
Conexão entre a aplicação e o MySQL.
JWT
Autenticação baseada em tokens.
Werkzeug
Geração e validação de hash de senhas.
python-dotenv
Leitura das configurações definidas no arquivo .env.
Flask-CORS
Configuração de acesso entre origens.
Git/GitHub
Versionamento e hospedagem do código.




Estrutura do projeto

Plain Text


flask-academy-api/
├── routes/
│   ├── alunos_routes.py
│   ├── auth_routes.py
│   ├── cursos_routes.py
│   ├── matricula_routes.py
│   └── professor_routes.py
├── templates/
│   └── index.html
├── .env.example
├── .gitignore
├── banco.py
├── decorators.py
├── main.py
└── requirements.txt



Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

•
Python 3.11 ou superior;

•
MySQL Server;

•
Git;

•
pip, gerenciador de pacotes do Python.

Instalação

Clone o repositório e entre na pasta do projeto:

Bash


git clone https://github.com/JarbasSantosSilva/flask-academy-api.git
cd flask-academy-api



Crie e ative um ambiente virtual:

Bash


python -m venv venv



No Linux ou macOS:

Bash


source venv/bin/activate



No Windows PowerShell:

Plain Text


venv\Scripts\Activate.ps1



Instale as dependências disponíveis no projeto:

Bash


pip install -r requirements.txt



Configuração do ambiente

O projeto utiliza variáveis de ambiente para as configurações do banco de dados e das chaves da aplicação.

Crie uma cópia do arquivo de exemplo:

Bash


cp .env.example .env



No Windows PowerShell, utilize:

Plain Text


Copy-Item .env.example .env



Depois, preencha o arquivo .env com as configurações da sua máquina:

Plain Text


DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=nome_do_banco
JWT_SECRET_KEY=defina_uma_chave_jwt_segura
SECRET_KEY=defina_uma_chave_da_aplicacao_segura




Nunca publique o arquivo .env real no GitHub. Utilize apenas o .env.example para compartilhar os nomes das variáveis necessárias, sem credenciais verdadeiras.

Banco de dados

Crie um banco de dados MySQL e configure o nome correspondente na variável DB_NAME do arquivo .env.


Observação: o script de criação das tabelas ainda será adicionado ao projeto. Por isso, nesta versão, a estrutura inicial das tabelas precisa ser criada conforme o modelo utilizado pela aplicação.

A aplicação utiliza as seguintes entidades:

Entidade
Finalidade
usuarios
Armazena dados de login e nível de acesso.
alunos
Armazena nome e e-mail dos alunos.
cursos
Armazena nome, carga horária, descrição e professor responsável.
professor
Armazena nome e especialidade dos professores.
matriculas
Relaciona alunos e cursos, incluindo a data da matrícula.




Execução

Com o ambiente virtual ativado e o arquivo .env configurado, execute:

Bash


python main.py



A aplicação será iniciada localmente no endereço:

Plain Text


http://127.0.0.1:5000



A rota inicial está disponível em:

Plain Text


GET /



Autenticação

As rotas de autenticação estão disponíveis no prefixo /auth.

Cadastro de usuário

Plain Text


POST /auth/cadastro
Content-Type: application/json



Corpo da requisição:

JSON


{
  "login": "usuario",
  "senha": "senha-forte",
  "aluno_id": null,
  "nivel_acesso": "aluno"
}



Os campos login e senha são obrigatórios. Os campos aluno_id e nivel_acesso podem ser utilizados conforme a configuração do usuário.

Login

Plain Text


POST /auth/login
Content-Type: application/json



Corpo da requisição:

JSON


{
  "login": "usuario",
  "senha": "senha-forte"
}



Após o login, a API retorna um token JWT. Utilize o token nas rotas protegidas:

Plain Text


Authorization: Bearer SEU_TOKEN



Principais endpoints

As rotas de alunos, cursos, professores e matrículas exigem autenticação por token Bearer.

Recurso
Prefixo
Métodos disponíveis
Alunos
/alunos/
GET, POST, PUT, PATCH, DELETE
Cursos
/cursos/
GET, POST, PUT, PATCH, DELETE
Professores
/professor/
GET, POST, PUT, DELETE, PATCH
Matrículas
/matricula/
GET, POST, PUT, PATCH, DELETE




Exemplo: cadastrar aluno

Plain Text


POST /alunos/
Authorization: Bearer SEU_TOKEN
Content-Type: application/json



JSON


{
  "nome": "Maria da Silva",
  "email": "maria@example.com"
}



Exemplo: consultar alunos

Plain Text


GET /alunos/
Authorization: Bearer SEU_TOKEN



Exemplo: atualizar parcialmente um aluno

Plain Text


PATCH /alunos/1
Authorization: Bearer SEU_TOKEN
Content-Type: application/json



JSON


{
  "email": "novo-email@example.com"
}



Os exemplos acima seguem a estrutura atual das rotas. Para explorar todos os campos aceitos, consulte os arquivos correspondentes dentro da pasta routes/.

Tratamento de erros

A aplicação valida a presença de dados nas requisições e retorna respostas JSON com códigos HTTP para situações como dados ausentes, credenciais inválidas, token ausente ou inválido, registro não encontrado e erros de conexão com o banco de dados.

Próximos passos

As melhorias abaixo fazem parte da evolução planejada do projeto e ainda não devem ser consideradas funcionalidades concluídas:

•
Adicionar um script SQL ou migrações para criação automática das tabelas.

•
Atualizar e revisar as dependências do requirements.txt.

•
Criar testes automatizados com Pytest.

•
Documentar a API com OpenAPI ou Swagger.

•
Padronizar mensagens de erro e respostas JSON.

•
Implementar regras de autorização por nível de acesso.

•
Restringir o CORS para origens específicas.

•
Separar regras de negócio em camadas de serviço e repositório.

•
Configurar lint, formatação e integração contínua.

•
Criar uma versão de produção sem debug=True.

Objetivo de aprendizagem

Este projeto faz parte da minha jornada de transição para o desenvolvimento backend. Por meio dele, estou praticando Python, Flask, SQL/MySQL, autenticação, organização de código, tratamento de exceções e versionamento com Git/GitHub.

Autor

Jarbas Santos Silva

•
LinkedIn: linkedin.com/in/jarbassantossilva

•
GitHub: github.com/JarbasSantosSilva

