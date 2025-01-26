import psycopg2


# Dados de conexão com o banco de dados
HOST = "1"
DATABASE = "1"  
USER = "1"  
PASSWORD = "1"

# Função para conectar ao banco de dados
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

# Função para executar a transação
def execute_transaction():
    connection = connect_to_db()
    if not connection:
        return

    try:
        # iniciar a transação
        connection.autocommit = False
        cursor = connection.cursor()

        # 1. atualizar o estado da turma "CC2024DS1" para "Fechado"
        update_turma_query = """
        UPDATE Turma
        SET estado = 'Fechado'
        WHERE codigo = 'CC2024DS1';
        """
        cursor.execute(update_turma_query)

        # 2. remover todas as matrículas de alunos na turma "CC2024DS1"
        delete_matriculas_query = """
        DELETE FROM Aluno_Turma
        WHERE turma_id = (
            SELECT id FROM Turma WHERE codigo = 'CC2024DS1'
        );
        """
        cursor.execute(delete_matriculas_query)

        #confirmar a transação
        connection.commit()
        print("Transação concluída com sucesso.")

    except Exception as e:
        #reverter a transação em caso de erro
        connection.rollback()
        print(f"Erro ao executar a transação: {e}")

    finally:
        #fechar o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    execute_transaction()
