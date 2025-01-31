-- Função do gatilho para verificar a capacidade máxima da turma
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

-- Gatilho para verificar a capacidade máxima da turma antes da inserção
CREATE TRIGGER trigger_verificar_max_disciplina_por_aluno
        BEFORE INSERT ON Aluno_Turma
        FOR EACH ROW EXECUTE FUNCTION verificar_max_disciplina_por_aluno();

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
   