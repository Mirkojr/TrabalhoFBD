
-- Trabalho de Banco de Dados da Faculdade

CREATE TABLE curso (
    cod_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    coordenador VARCHAR(100) NOT NULL,
    regime VARCHAR(20) CHECK (regime IN ('semestral', 'anual')) NOT NULL,
    duracao  SMALLINT NOT NULL
    );

CREATE TABLE avaliacao (
    cod_id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) CHECK (tipo IN ('prova', 'trabalho')) NOT NULL,
    dt_aplicacao DATE NOT NULL,
    peso INT NOT NULL
);

CREATE TABLE professor(
    cod_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(50) NOT NULL,
    especializacao VARCHAR(50) NOT NULL,
    curso_cod_id INT NOT NULL,
    FOREIGN KEY (curso_cod_id) REFERENCES curso(cod_id)
);

CREATE TABLE material_didatico(
    cod_id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    formato VARCHAR(20) CHECK(formato IN ('PDF', 'video', 'audio', 'material', 'externo')) NOT NULL
);

CREATE TABLE aluno(
    cod_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ano_entrada DATE NOT NULL,
    prev_conclusao DATE NOT NULL,
    idade TINYINT NOT NULL,
    curso_cod_id INT NOT NULL,
    FOREIGN KEY (curso_cod_id) REFERENCES curso(cod_id)
);

CREATE TABLE nota(
    cod_id SERIAL PRIMARY KEY,
    valor DECIMAL(5, 2) NOT NULL,
    aluno_cod_id INT NOT NULL,
    avaliacao_cod_id INT NOT NULL,
    FOREIGN KEY (aluno_cod_id) REFERENCES aluno(cod_id),
    FOREIGN KEY (avaliacao_cod_id) REFERENCES avaliacao(cod_id)
);

CREATE TABLE projeto_de_pesquisa(
    cod_id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    especializacao VARCHAR(100) NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    prev_conclusao  DATE NOT NULL,
    orçamento_re DECIMAL(10, 2) NOT NULL,
    orçamento_pl DECIMAL(10, 2) NOT NULL,
    professor_cod_id INT NOT NULL,
    aluno_cod_id INT NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('planejado', 'andamento', 'finalizado')) NOT NULL
);

CREATE TABLE turma(
    cod_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    curso_cod_id INT NOT NULL,
    semestre VARCHAR(20) NOT NULL,
    capacidade INT NOT NULL,
    estado VARCHAR(50) CHECK (estado IN ('aberta', 'fechada')) NOT NULL,
    FOREIGN KEY (curso_cod_id) REFERENCES curso(cod_id)
);

CREATE TABLE sala_de_aula(
    cod_id SERIAL PRIMARY KEY,
    localizacao VARCHAR(100) NOT NULL,
    capacidade INT NOT NULL,
    tp_lousa VARCHAR(50) NOT NULL,
    tp_estrutura VARCHAR(50) CHECK (tp_estrutura IN ('audio', 'tradicional', 'laboratorio')) NOT NULL
);

CREATE TABLE disciplina(
    codigo VARCHAR(10) PRIMARY KEY,  -- Ex.: "CS101"
    nome VARCHAR(100) NOT NULL,
    especializacao VARCHAR(50) NOT NULL,
    carga_horaria INT NOT NULL,
    ementa TEXT NOT NULL
);

CREATE TABLE alunoProjeto(
    aluno_cod_id INT NOT NULL,
    projeto_cod_id INT NOT NULL,
    funcao VARCHAR(500) NOT NULL,
    PRIMARY KEY (aluno_cod_id, projeto_cod_id),
    FOREIGN KEY (aluno_cod_id) REFERENCES aluno(cod_id),
    FOREIGN KEY (projeto_cod_id) REFERENCES projeto_de_pesquisa(cod_id)
);

CREATE TABLE alunoTurma(
    aluno_cod_id INT NOT NULL,
    turma_cod_id INT NOT NULL,
    PRIMARY KEY (aluno_cod_id,turma_cod_id),
    FOREIGN KEY (aluno_cod_id) REFERENCES aluno(cod_id),
    FOREIGN KEY (turma_cod_id) REFERENCES turma(cod_id)
);

CREATE TABLE professorTurma(
    professor_cod_id INT NOT NULL,
    turma_cod_id INT NOT NULL,
    PRIMARY KEY (professor_cod_id, turma_cod_id),
    FOREIGN KEY (professor_cod_id) REFERENCES professor(cod_id),
    FOREIGN KEY (turma_cod_id) REFERENCES turma(cod_id)
);

CREATE TABLE professorProjeto(
    professor_cod_id INT NOT NULL,
    projeto_cod_id INT NOT NULL,
    funcao VARCHAR(500) NOT NULL,
    PRIMARY KEY (professor_cod_id, projeto_cod_id),
    FOREIGN KEY (professor_cod_id) REFERENCES professor(cod_id),
    FOREIGN KEY (projeto_cod_id) REFERENCES projeto_de_pesquisa(cod_id)
);

CREATE TABLE professorMaterial_didatico(
    professor_cod_id INT NOT NULL,
    material_didatico_cod_id INT NOT NULL,
    PRIMARY KEY (professor_cod_id, material_didatico_cod_id),
    FOREIGN KEY (professor_cod_id) REFERENCES professor(cod_id),
    FOREIGN KEY (material_didatico_cod_id) REFERENCES material_didatico(cod_id)
);

CREATE TABLE material_didaticoTurma(
    turma_cod_id INT NOT NULL,
    material_didatico_cod_id INT NOT NULL,
    PRIMARY KEY (turma_cod_id,material_didatico_cod_id),
    FOREIGN KEY (turma_cod_id) REFERENCES turma(cod_id),
    FOREIGN KEY (material_didatico_cod_id) REFERENCES material_didatico(cod_id)
);

CREATE TABLE TurmaDisciplina(
    turma_cod_id INT NOT NULL,
    disciplina_cod_id VARCHAR(10) NOT NULL,
    PRIMARY KEY (disciplina_cod_id, turma_cod_id),
    FOREIGN KEY (disciplina_cod_id) REFERENCES disciplina(codigo),
    FOREIGN KEY (turma_cod_id) REFERENCES turma(cod_id)
);

CREATE TABLE TurmaAvaliacao(
    turma_cod_id INT NOT NULL,
    avaliacao_cod_id INT NOT NULL,
    PRIMARY KEY (avaliacao_cod_id, turma_cod_id),
    FOREIGN KEY (avaliacao_cod_id) REFERENCES avaliacao(cod_id),
    FOREIGN KEY (turma_cod_id) REFERENCES turma(cod_id)
);