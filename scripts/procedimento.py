import psycopg2

#dados de conexão com o banco de dados
HOST = "1"
DATABASE = "1"  
USER = "1"  
PASSWORD = "1"

#função para conectar ao banco de dados
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host = HOST,
            database = DATABASE,
            user = USER,
            password = PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

#função para chamar o procedimento armazenado
def call_stored_procedure(semestre):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        #chamar o procedimento armazenado corretamente com CALL
        cursor.execute("CALL inc_semestre(%s)", (semestre,))
        connection.commit()

        print(f"Procedimento armazenado 'inc_semestre' chamado com sucesso para o semestre {semestre}.")

    except Exception as e:
        print(f"Erro ao executar o procedimento armazenado: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    #chamar o procedimento para incrementar alunos do 1º semestre
    call_stored_procedure(1)
