import pyodbc

def executar_comando_sql(server, database, username, password, comando_sql):
    try:
        # Conecta ao servidor SQL Server
        conn = pyodbc.connect(
            f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        conn.autocommit = True  # Permitir execução fora de transações

        # Executa o comando SQL
        cursor = conn.cursor()
        cursor.execute(comando_sql)
        
        print("Comando SQL executado com sucesso!")

        # Fecha a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print("Erro ao executar o comando SQL:", e)


# 🔥 **Criação do Banco de Dados com Filegroups**  
comando_sql = """
-- 📌 Decisão sobre tamanhos e crescimento:
-- - O tamanho inicial dos arquivos de dados (500MB) permite acomodar um volume razoável de informações sem expansões frequentes.
-- - O crescimento fixo (100MB para dados e 500MB para log) evita fragmentação excessiva e melhora o desempenho.
-- - O log tem um tamanho inicial maior (1GB) e um crescimento maior (500MB) porque transações intensivas podem gerar um grande volume de logs rapidamente.
-- - A separação dos Filegroups permite distribuir a carga de I/O e otimizar a recuperação e manutenção do banco.

CREATE DATABASE MeuBancoAvancado
ON PRIMARY (
    NAME = MeuBanco_Primary,
    FILENAME = 'C:\\SQLServer\\MeuBanco_Primary.mdf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
FILEGROUP FileGroup1 (
    NAME = FileGroup1_File1,
    FILENAME = 'C:\\SQLServer\\FileGroup1_File1.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
(
    NAME = FileGroup1_File2,
    FILENAME = 'C:\\SQLServer\\FileGroup1_File2.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
FILEGROUP FileGroup2 (
    NAME = FileGroup2_File1,
    FILENAME = 'C:\\SQLServer\\FileGroup2_File1.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
(
    NAME = FileGroup2_File2,
    FILENAME = 'C:\\SQLServer\\FileGroup2_File2.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
FILEGROUP FileGroup3 (
    -- Filegroup que pode ser usado para futuras expansões ou tabelas menos acessadas.
    NAME = FileGroup3_File1,
    FILENAME = 'C:\\SQLServer\\FileGroup3_File1.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
(
    NAME = FileGroup3_File2,
    FILENAME = 'C:\\SQLServer\\FileGroup3_File2.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
FILEGROUP IndexFileGroup (
    -- Filegroup específico para armazenar índices e otimizar desempenho.
    NAME = Index_File1,
    FILENAME = 'C:\\SQLServer\\Index_File1.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
),
(
    NAME = Index_File2,
    FILENAME = 'C:\\SQLServer\\Index_File2.ndf',
    SIZE = 500MB, MAXSIZE = 5GB, FILEGROWTH = 100MB
)
LOG ON (
    NAME = MeuBanco_Log,
    FILENAME = 'C:\\SQLServer\\MeuBanco_Log.ldf',
    SIZE = 1GB, MAXSIZE = 10GB, FILEGROWTH = 500MB
);

USE MeuBancoAvancado;

-- Removendo tabelas se existirem para garantir recriação sem conflitos.
DROP TABLE IF EXISTS Aluno_Turma;
DROP TABLE IF EXISTS Turma;
DROP TABLE IF EXISTS Disciplina;
DROP TABLE IF EXISTS Professor;
DROP TABLE IF EXISTS Aluno;
DROP TABLE IF EXISTS Curso;

-- 📌 Criando tabelas distribuídas entre os filegroups definidos para melhor desempenho e organização.
CREATE TABLE Curso (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    regime VARCHAR(20),
    duracao INT
) ON FileGroup1;

CREATE TABLE Aluno (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    curso_id INT REFERENCES Curso(id),
    semestre INT
) ON FileGroup1;

CREATE TABLE Professor (
    id INT PRIMARY KEY,
    nome VARCHAR(100),
    area_especializacao VARCHAR(100),
    contato VARCHAR(100),
    curso_id INT REFERENCES Curso(id)
) ON FileGroup1;

CREATE TABLE Disciplina (
    id INT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    nome VARCHAR(100),
    area_especializacao VARCHAR(100),
    carga_horaria INT,
    curso_id INT REFERENCES Curso(id)
) ON FileGroup1;

CREATE TABLE Turma (
    id INT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE,
    disciplina_id INT REFERENCES Disciplina(id),
    semestre VARCHAR(20),
    capacidade_maxima INT,
    estado VARCHAR(20),
    prof_id INT REFERENCES Professor(id)
) ON FileGroup2;

CREATE TABLE Aluno_Turma (
    aluno_id INT REFERENCES Aluno(id),
    turma_id INT REFERENCES Turma(id),
    PRIMARY KEY (aluno_id, turma_id)
) ON FileGroup2;


-- Criando índices no filegroup específico para índices com ajustes de desempenho
-- 📌 Decisão sobre índices:
-- - Os índices são CLUSTERED para otimizar buscas ordenadas e joins frequentes.
-- - PAD_INDEX = ON para reservar espaço nos nós intermediários, evitando reequilíbrios frequentes.
-- - FILLFACTOR = 80 para deixar espaço para inserções, já que há mudanças semestrais estruturais.

    CREATE CLUSTERED INDEX idx_aluno_nome ON Aluno (nome) 
    WITH (PAD_INDEX = ON, FILLFACTOR = 80) ON IndexFileGroup;

    CREATE CLUSTERED INDEX idx_professor_nome ON Professor (nome) 
    WITH (PAD_INDEX = ON, FILLFACTOR = 80) ON IndexFileGroup;

    CREATE CLUSTERED INDEX idx_disciplina_nome ON Disciplina (nome) 
    WITH (PAD_INDEX = ON, FILLFACTOR = 80) ON IndexFileGroup;

    CREATE CLUSTERED INDEX idx_turma_codigo ON Turma (codigo) 
    WITH (PAD_INDEX = ON, FILLFACTOR = 80) ON IndexFileGroup;

"""

# Executa a criação do banco e das tabelas
executar_comando_sql(
    server='server',        # Servidor ou IP
    database = 'database',
    username='user',             # Nome de usuário
    password='pwd',  # Senha
    comando_sql=comando_sql
)
