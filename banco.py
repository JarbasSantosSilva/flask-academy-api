import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def obter_conexao():
    try:
        conexao = mysql.connector.connect (
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
            )
        return conexao
    except Error as erro:
        print(f"Erro ao conectar ao Mysql: {erro}")
        raise

def testar_conexao():
    try:
        conn = obter_conexao()
        if conn.is_connected():
            print("Conexão com o banco de dados MySQL estabelecida com sucesso!")
            conn.close()
    except Error as erro:
        print(f"Alerta: O servidor iniciou , mas não foi possível conectar ao banco de dados.")
        print(f"Detalhes do erro: {erro}")

