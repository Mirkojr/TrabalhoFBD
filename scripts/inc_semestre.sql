CREATE OR REPLACE PROCEDURE inc_semestre(target_semestre INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Atualizar o semestre dos alunos para target_semestre + 1
    UPDATE Aluno
    SET semestre = semestre + 1
    WHERE semestre = target_semestre;

    RAISE NOTICE 'Semestre incrementado para todos os alunos no semestre %.', target_semestre;
END;
$$;
