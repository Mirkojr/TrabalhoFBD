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
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar o gatilho que limita a capacidade da turma
def create_trigger_capacidade_turma():
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        # Criar a função do gatilho
        cursor.execute("""
        CREATE OR REPLACE FUNCTION verificar_capacidade_turma()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Verifica o número de alunos matriculados na turma
            IF (SELECT COUNT(*) FROM Aluno_Turma WHERE turma_id = NEW.turma_id) >= 
               (SELECT capacidade_maxima FROM Turma WHERE id = NEW.turma_id) THEN
                RAISE EXCEPTION 'Capacidade máxima da turma excedida';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)

        # Criar o gatilho
        cursor.execute("""
        CREATE TRIGGER trigger_verificar_capacidade_turma
        BEFORE INSERT ON Aluno_Turma
        FOR EACH ROW EXECUTE FUNCTION verificar_capacidade_turma();
        """)

        connection.commit()
        print("Gatilho de capacidade da turma criado com sucesso.")

    except Exception as e:
        print(f"Erro ao criar o gatilho: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Função para criar o gatilho que limita o número de disciplinas por aluno
def create_trigger_max_disciplina_por_aluno():
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        # Criar a função do gatilho
        cursor.execute("""
        CREATE OR REPLACE FUNCTION verificar_max_disciplina_por_aluno()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Verifica o número de disciplinas que o aluno já está matriculado no semestre
            IF (SELECT COUNT(*) FROM Aluno_Turma AT
                JOIN Turma T ON AT.turma_id = T.id
                WHERE AT.aluno_id = NEW.aluno_id AND T.semestre = 
                (SELECT semestre FROM Turma WHERE id = NEW.turma_id)
            ) >= 4 THEN
                RAISE EXCEPTION 'Aluno já está matriculado em 4 disciplinas no semestre';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """)

        # Criar o gatilho
        cursor.execute("""
        CREATE TRIGGER trigger_verificar_max_disciplina_por_aluno
        BEFORE INSERT ON Aluno_Turma
        FOR EACH ROW EXECUTE FUNCTION verificar_max_disciplina_por_aluno();
        """)

        connection.commit()
        print("Gatilho de limite de disciplinas por aluno criado com sucesso.")

    except Exception as e:
        print(f"Erro ao criar o gatilho: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Função para inserir os dados na tabela Aluno_Turma
def insert_aluno_turma(dados):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        for aluno_id, turma_id in dados:
            cursor.execute("INSERT INTO Aluno_Turma (aluno_id, turma_id) VALUES (%s, %s)", (aluno_id, turma_id))
        
        connection.commit()
        print("Dados inseridos com sucesso na tabela Aluno_Turma.")

    except Exception as e:
        print(f"Erro ao inserir dados na tabela Aluno_Turma: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Função para chamar o procedimento armazenado
def call_stored_procedure(semestre):
    connection = connect_to_db()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        # Alterar para chamar a função com CALL
        cursor.execute(f"CALL inc_semestre({semestre})")
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

# Dados a serem inseridos nas tabelas
dados_tabela7 = [(3, 1), (5, 1), (4, 1)]
dados_tabela8 = [(1, 2), (1, 3), (1, 4)]

if __name__ == "__main__":
    # Criar os gatilhos
    create_trigger_capacidade_turma()
    create_trigger_max_disciplina_por_aluno()

    # Inserir dados na tabela "Aluno_Turma"
    print("Inserindo dados na Tabela 7...")
    insert_aluno_turma(dados_tabela7)
    
    print("Inserindo dados na Tabela 8...")
    insert_aluno_turma(dados_tabela8)
    
    # Chamar o procedimento armazenado para incrementar o semestre dos alunos
    call_stored_procedure(1)
