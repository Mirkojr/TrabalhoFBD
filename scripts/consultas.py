import psycopg2

# Dados de conexão com o banco de dados
HOST = "1"
DATABASE = "1"  
USER = "1"  
PASSWORD = "1"

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

# Consulta 1: Retornar todas as turmas e a quantidade de alunos participantes de cada turma
def get_turmas_e_alunos(cursor):
    query = """
    SELECT 
        T.codigo AS turma_codigo, 
        COUNT(AT.aluno_id) AS qtd_alunos
    FROM 
        Turma T
    LEFT JOIN 
        Aluno_Turma AT ON T.id = AT.turma_id
    GROUP BY 
        T.codigo;
    """
    cursor.execute(query)
    return cursor.fetchall()

# Consulta 2: Retornar os alunos matriculados na disciplina "Fundamentos de Bancos de Dados"
def get_alunos_na_disciplina(cursor):
    query = """
    SELECT 
        A.nome AS aluno_nome
    FROM 
        Aluno A
    INNER JOIN 
        Aluno_Turma AT ON A.id = AT.aluno_id
    INNER JOIN 
        Turma T ON AT.turma_id = T.id
    INNER JOIN 
        Disciplina D ON T.disciplina_id = D.id
    WHERE 
        D.nome = 'Fundamentos de Bancos de Dados';
    """
    cursor.execute(query)
    return cursor.fetchall()

# Consulta 3: Retornar a quantidade de professores do curso "Ciências da Computação"
def get_qtd_professores_curso(cursor):
    query = """
    SELECT 
        COUNT(*) AS qtd_professores
    FROM 
        Professor P
    INNER JOIN 
        Curso C ON P.curso_id = C.id
    WHERE 
        C.nome = 'Ciências da Computação';
    """
    cursor.execute(query)
    return cursor.fetchone()[0]

# Função principal
def main():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Executar a consulta 1
            print("Turmas e quantidade de alunos:")
            turmas_e_alunos = get_turmas_e_alunos(cursor)
            for turma in turmas_e_alunos:
                print(f"Turma: {turma[0]}, Alunos: {turma[1]}")
            
            # Executar a consulta 2
            print("\nAlunos matriculados na disciplina 'Fundamentos de Bancos de Dados':")
            alunos_na_disciplina = get_alunos_na_disciplina(cursor)
            for aluno in alunos_na_disciplina:
                print(f"Aluno: {aluno[0]}")
            
            # Executar a consulta 3
            print("\nQuantidade de professores no curso 'Ciências da Computação':")
            qtd_professores = get_qtd_professores_curso(cursor)
            print(f"Quantidade: {qtd_professores}")
        
        except Exception as e:
            print(f"Erro ao executar consultas: {e}")
        
        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()