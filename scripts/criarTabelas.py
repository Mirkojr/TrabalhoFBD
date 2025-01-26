import psycopg2

#conexão com o banco de dados
HOST = "1"
DATABASE = "1"  
USER = "1"  
PASSWORD = "1"

#script para criar as tabelas
create_tables_script = """
DROP TABLE IF EXISTS Aluno_Turma CASCADE;
DROP TABLE IF EXISTS Turma CASCADE;
DROP TABLE IF EXISTS Disciplina CASCADE;
DROP TABLE IF EXISTS Professor CASCADE;
DROP TABLE IF EXISTS Aluno CASCADE;
DROP TABLE IF EXISTS Curso CASCADE;

CREATE TABLE Curso (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    regime VARCHAR(20),
    duracao INT
);

CREATE TABLE Aluno (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    curso_id INT REFERENCES Curso(id),
    semestre INT
);

CREATE TABLE Professor (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    area_especializacao VARCHAR(100),
    contato VARCHAR(100),
    curso_id INT REFERENCES Curso(id)
);

CREATE TABLE Disciplina (
    id INT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    nome VARCHAR(100),
    area_especializacao VARCHAR(100),
    carga_horaria INT,
    curso_id INT REFERENCES Curso(id)
);

CREATE TABLE Turma (
    id INT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    disciplina_id INT REFERENCES Disciplina(id),
    semestre VARCHAR(20),
    capacidade_maxima INT,
    estado VARCHAR(20),
    prof_id INT REFERENCES Professor(id)
);

CREATE TABLE Aluno_Turma (
    aluno_id INT REFERENCES Aluno(id),
    turma_id INT REFERENCES Turma(id),
    PRIMARY KEY (aluno_id, turma_id)
);
"""

#função para criar as tabelas
def create_tables():
    try:
        #conectar ao banco de dados
        with psycopg2.connect(
            host=HOST,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD
        ) as conn:
            with conn.cursor() as cur:
                #executar o script para criar as tabelas
                cur.execute(create_tables_script)
                print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")

# Executa a função
if __name__ == "__main__":
    create_tables()
