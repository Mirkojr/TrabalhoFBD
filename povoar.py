from faker import Faker
import psycopg2
import string

class CodigoIdentificadorGenerator:
    def __init__(self):
        self.contador = 1  # Inicializa o contador

    def gerar_codigo_identificador(self, area_especializacao):
        #Pega os dois primeiros caracteres da área de especialização em maiúsculo
        prefixo = area_especializacao[:2].upper()

        #Gera o número único, usando o contador e adiciona zeros à esquerda para ter 4 dígitos
        numero = str(self.contador).zfill(4)

        #Cria o código identificador concatenando o prefixo e o número
        codigo_identificador = f"{prefixo}{numero}"

        #Incrementa o contador para o próximo código
        self.contador += 1

        return codigo_identificador

class Povoar:

    def __init__(self):
        self.fake = Faker('pt_BR')

    def criar_curso(self):
        cursos = []
        
        conn = psycopg2.connect(
            dbname="496563",
            user="496563",
            password="496563",
            host="200.129.44.249",
            port="5432"
        )
        cur = conn.cursor()
        
        for _ in range(10):
            curso = {
                'nome': self.fake.job(),
                'coordenador': self.fake.name(),
                'regime': self.fake.random_element(['semestral', 'anual']),
                'duracao': self.fake.random_int(min=6, max=12)
            }
            print(curso)
            cur.execute("""
                INSERT INTO curso (nome, coordenador, regime, duracao)
                VALUES (%s, %s, %s, %s)
            """, (curso['nome'], curso['coordenador'], curso['regime'], curso['duracao']))
            
            cursos.append(curso)
        
        return cursos
        
    def criar_aluno(self, cur):
        alunos = []
        

        for _ in range(10):
            #pegar um curso_cod_id aleatorio da tabela do curso
            cur.execute("SELECT cod_id FROM curso ORDER BY RANDOM() LIMIT 1")
            curso_id = cur.fetchone()[0]

            aluno = {
                'nome': self.fake.name(),
                'ano_entrada': self.fake.date_between(start_date='-5y', end_date='today'),
                'idade': self.fake.random_int(min=17, max=60),
                'curso_cod_id': curso_id
            }

            #Calcular prev_conclusao baseado no ano_entrada
            cur.execute("SELECT duracao FROM curso WHERE cod_id = %s", (curso_id,))
            duracao = cur.fetchone()[0]
            aluno['prev_conclusao'] = aluno['ano_entrada'].replace(year=aluno['ano_entrada'].year + (duracao // 2))

            print(aluno)
            cur.execute("""
                INSERT INTO aluno (nome, ano_entrada, prev_conclusao, idade, curso_cod_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (aluno['nome'], aluno['ano_entrada'], aluno['prev_conclusao'], aluno['idade'], aluno['curso_cod_id']))

            alunos.append(aluno)
        
    def criar_professor(self, cur):
        professores = []

        for _ in range(10):
            cur.execute("SELECT cod_id FROM curso ORDER BY RANDOM() LIMIT 1")
            curso_id = cur.fetchone()[0]

            professor = {
                'nome': self.fake.name(),
                'contato': self.fake.phone_number(),
                'especializacao': self.fake.job(),
                'curso_cod_id': curso_id
            }

            print(professor)
            cur.execute("""
                INSERT INTO professor (nome, contato, especializacao, curso_cod_id)
                VALUES (%s, %s, %s, %s)
            """, (professor['nome'], professor['contato'], professor['especializacao'], professor['curso_cod_id']))

            professores.append(professor)

    def criar_material_didatico(self, cur):
        materiais = []

        for _ in range(10):
            material = {
                'titulo': self.fake.catch_phrase(),
                'descricao': self.fake.text(max_nb_chars=400),
                'formato': self.fake.random_element(['PDF', 'video', 'audio', 'material', 'externo'])
            }

            print(material)
            cur.execute("""
                INSERT INTO material_didatico (titulo, descricao, formato)
                VALUES (%s, %s, %s)
            """, (material['titulo'], material['descricao'], material['formato']))

            materiais.append(material)
    def criar_nota(self, cur):
        notas = []
        for _ in range(10):
            cur.execute("SELECT cod_id FROM aluno ORDER BY RANDOM() LIMIT 1")
            aluno_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM avaliacao ORDER BY RANDOM() LIMIT 1")
            avaliacao_id = cur.fetchone()[0]

            nota = {
                'valor': round(self.fake.random.uniform(0, 10), 2),
                'aluno_cod_id': aluno_id,
                'avaliacao_cod_id': avaliacao_id
            }

            print(nota)
            cur.execute("""
                INSERT INTO nota (valor, aluno_cod_id, avaliacao_cod_id)
                VALUES (%s, %s, %s)
            """, (nota['valor'], nota['aluno_cod_id'], nota['avaliacao_cod_id']))

            notas.append(nota)

    def criar_projeto_pesquisa(self, cur):
        projetos = []
        for _ in range(10):
            cur.execute("SELECT cod_id FROM professor ORDER BY RANDOM() LIMIT 1")
            professor_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM aluno ORDER BY RANDOM() LIMIT 1")
            aluno_id = cur.fetchone()[0]

            projeto = {
                'titulo': self.fake.catch_phrase(),
                'especializacao': self.fake.job(),
                'descricao': self.fake.text(max_nb_chars=400),
                'prev_conclusao': self.fake.date_between(start_date='today', end_date='+2y'),
                'orçamento_re': round(self.fake.random.uniform(1000, 50000), 2),
                'orçamento_pl': round(self.fake.random.uniform(1000, 50000), 2),
                'professor_cod_id': professor_id,
                'aluno_cod_id': aluno_id,
                'estado': self.fake.random_element(['planejado', 'andamento', 'finalizado'])
            }

            print(projeto)
            cur.execute("""
                INSERT INTO projeto_de_pesquisa (titulo, especializacao, descricao, prev_conclusao, 
                orçamento_re, orçamento_pl, professor_cod_id, aluno_cod_id, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (projeto['titulo'], projeto['especializacao'], projeto['descricao'], 
                  projeto['prev_conclusao'], projeto['orçamento_re'], projeto['orçamento_pl'],
                  projeto['professor_cod_id'], projeto['aluno_cod_id'], projeto['estado']))

            projetos.append(projeto)

    def criar_turma(self, cur):
        turmas = []
        for _ in range(10):
            cur.execute("SELECT cod_id FROM curso ORDER BY RANDOM() LIMIT 1")
            curso_id = cur.fetchone()[0]

            turma = {
                'nome': self.fake.word() + ' ' + str(self.fake.random_int(min=1, max=10)),
                'curso_cod_id': curso_id,
                'semestre': str(self.fake.random_int(min=1, max=2)) + '/' + str(self.fake.random_int(min=2020, max=2023)),
                'capacidade': self.fake.random_int(min=20, max=60),
                'estado': self.fake.random_element(['aberta', 'fechada'])
            }

            print(turma)
            cur.execute("""
                INSERT INTO turma (nome, curso_cod_id, semestre, capacidade, estado)
                VALUES (%s, %s, %s, %s, %s)
            """, (turma['nome'], turma['curso_cod_id'], turma['semestre'], 
                  turma['capacidade'], turma['estado']))

            turmas.append(turma)

    def criar_sala_aula(self, cur):
        salas = []
        for _ in range(10):
            sala = {
                'localizacao': self.fake.street_address(),
                'capacidade': self.fake.random_int(min=20, max=100),
                'tp_lousa': self.fake.random_element(['digital', 'tradicional', 'ambas']),
                'tp_estrutura': self.fake.random_element(['audio', 'tradicional', 'laboratorio'])
            }

            print(sala)
            cur.execute("""
                INSERT INTO sala_de_aula (localizacao, capacidade, tp_lousa, tp_estrutura)
                VALUES (%s, %s, %s, %s)
            """, (sala['localizacao'], sala['capacidade'], sala['tp_lousa'], sala['tp_estrutura']))

            salas.append(sala)

    def criar_disciplina(self, cur):
        disciplinas = []
        codigo_gen = CodigoIdentificadorGenerator()
        for _ in range(10):
            especializacao = self.fake.job()
            disciplina = {
            'codigo': codigo_gen.gerar_codigo_identificador(especializacao),
            'nome': self.fake.catch_phrase(),
            'especializacao': especializacao,
            'carga_horaria': self.fake.random_element([30, 45, 60, 75, 90]),
            'ementa': self.fake.text(max_nb_chars=500)
            }

            print(disciplina)
            cur.execute("""
            INSERT INTO disciplina (codigo, nome, especializacao, carga_horaria, ementa)
            VALUES (%s, %s, %s, %s, %s)
            """, (disciplina['codigo'], disciplina['nome'], disciplina['especializacao'],
              disciplina['carga_horaria'], disciplina['ementa']))

            disciplinas.append(disciplina)

    def criar_avaliacao(self, cur):
        avaliacoes = []
        for _ in range(10):
            avaliacao = {
                'tipo': self.fake.random_element(['prova', 'trabalho']),
                'dt_aplicacao': self.fake.date_between(start_date='-1y', end_date='+1y'),
                'peso': self.fake.random_int(min=1, max=10)
            }

            print(avaliacao)
            cur.execute("""
                INSERT INTO avaliacao (tipo, dt_aplicacao, peso)
                VALUES (%s, %s, %s)
            """, (avaliacao['tipo'], avaliacao['dt_aplicacao'], avaliacao['peso']))

            avaliacoes.append(avaliacao)

    def criar_aluno_projeto(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM aluno ORDER BY RANDOM() LIMIT 1")
            aluno_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM projeto_de_pesquisa ORDER BY RANDOM() LIMIT 1")
            projeto_id = cur.fetchone()[0]

            relacao = {
                'aluno_cod_id': aluno_id,
                'projeto_cod_id': projeto_id,
                'funcao': self.fake.job()
            }

            cur.execute("""
                INSERT INTO alunoProjeto (aluno_cod_id, projeto_cod_id, funcao)
                VALUES (%s, %s, %s)
            """, (relacao['aluno_cod_id'], relacao['projeto_cod_id'], relacao['funcao']))

    def criar_aluno_turma(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM aluno ORDER BY RANDOM() LIMIT 1")
            aluno_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM turma ORDER BY RANDOM() LIMIT 1")
            turma_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO alunoTurma (aluno_cod_id, turma_cod_id)
                VALUES (%s, %s)
            """, (aluno_id, turma_id))

    def criar_professor_turma(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM professor ORDER BY RANDOM() LIMIT 1")
            professor_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM turma ORDER BY RANDOM() LIMIT 1")
            turma_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO professorTurma (professor_cod_id, turma_cod_id)
                VALUES (%s, %s)
            """, (professor_id, turma_id))

    def criar_professor_projeto(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM professor ORDER BY RANDOM() LIMIT 1")
            professor_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM projeto_de_pesquisa ORDER BY RANDOM() LIMIT 1")
            projeto_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO professorProjeto (professor_cod_id, projeto_cod_id, funcao)
                VALUES (%s, %s, %s)
            """, (professor_id, projeto_id, self.fake.job()))

    def criar_professor_material(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM professor ORDER BY RANDOM() LIMIT 1")
            professor_id = cur.fetchone()[0]
            cur.execute("SELECT cod_id FROM material_didatico ORDER BY RANDOM() LIMIT 1")
            material_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO professorMaterial_didatico (professor_cod_id, material_didatico_cod_id)
                VALUES (%s, %s)
            """, (professor_id, material_id))

    def criar_material_turma(self, cur):
        for _ in range(10):
            while True:
                cur.execute("SELECT cod_id FROM turma ORDER BY RANDOM() LIMIT 1")
                turma_id = cur.fetchone()[0]
                cur.execute("SELECT cod_id FROM material_didatico ORDER BY RANDOM() LIMIT 1")
                material_id = cur.fetchone()[0]

                #checa se a combinaçao ja existe
                cur.execute("""
                    SELECT 1 FROM material_didaticoTurma 
                    WHERE turma_cod_id = %s AND material_didatico_cod_id = %s
                """, (turma_id, material_id))
                
                if cur.fetchone() is None:
                    break

            cur.execute("""
                INSERT INTO material_didaticoTurma (turma_cod_id, material_didatico_cod_id)
                VALUES (%s, %s)
            """, (turma_id, material_id))

    def criar_turma_disciplina(self, cur):
        for _ in range(10):
            cur.execute("SELECT cod_id FROM turma ORDER BY RANDOM() LIMIT 1")
            turma_id = cur.fetchone()[0]
            cur.execute("SELECT codigo FROM disciplina ORDER BY RANDOM() LIMIT 1")
            disciplina_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO TurmaDisciplina (turma_cod_id, disciplina_cod_id)
                VALUES (%s, %s)
            """, (turma_id, disciplina_id))

    def criar_turma_avaliacao(self, cur):
        for _ in range(10):
            while True:
                cur.execute("SELECT cod_id FROM turma ORDER BY RANDOM() LIMIT 1")
                turma_id = cur.fetchone()[0]
                cur.execute("SELECT cod_id FROM avaliacao ORDER BY RANDOM() LIMIT 1")
                avaliacao_id = cur.fetchone()[0]

                # Check if combination already exists
                cur.execute("""
                    SELECT 1 FROM TurmaAvaliacao 
                    WHERE turma_cod_id = %s AND avaliacao_cod_id = %s
                """, (turma_id, avaliacao_id))
                
                if cur.fetchone() is None:
                    break

            cur.execute("""
                INSERT INTO TurmaAvaliacao (turma_cod_id, avaliacao_cod_id)
                VALUES (%s, %s)
            """, (turma_id, avaliacao_id))

povoar = Povoar()
try:
    conn = psycopg2.connect(
            #poe aqui as config pra conectar no banco de dados
            dbname="suaMatricula",
            user="suaMatricula",
            password="suaMatricula",
            host="200.1.2...",
            port="5432"
        )
    cur = conn.cursor() 
    # povoar.criar_curso()
    # povoar.criar_aluno(cur)
    # povoar.criar_professor(cur)
    # povoar.criar_material_didatico(cur)
    # povoar.criar_nota(cur)
    # povoar.criar_disciplina(cur)
    # povoar.criar_avaliacao(cur)
    # povoar.criar_projeto_pesquisa(cur)
    # povoar.criar_turma(cur)
    # povoar.criar_sala_aula(cur)

    # povoar.criar_aluno_projeto(cur)
    # povoar.criar_aluno_turma(cur)
    # povoar.criar_professor_turma(cur)
    # povoar.criar_professor_projeto(cur)
    # povoar.criar_professor_material(cur)
    # povoar.criar_material_turma(cur)
    # povoar.criar_turma_disciplina(cur)
    # povoar.criar_turma_avaliacao(cur)


except Exception as e:
    print(e)
    print('Error in connection')
finally:
    conn.commit()
    cur.close()
    conn.close()


    