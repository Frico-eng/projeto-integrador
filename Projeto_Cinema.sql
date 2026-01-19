CREATE DATABASE IF NOT EXISTS cineplus;
USE cineplus;

-- Tabela de Filmes
DROP TABLE IF EXISTS Filmes;
CREATE TABLE Filmes (
    ID_Filme INT AUTO_INCREMENT PRIMARY KEY,
    Titulo_Filme VARCHAR(255) NOT NULL,
    Genero VARCHAR(50),
    Duracao VARCHAR(8),
    Classificacao VARCHAR(10),
    Cartaz_Path VARCHAR(500),
    Direcao VARCHAR(255),
    Sinopse TEXT
);

-- Inserir os filmes com os caminhos dos cartazes, direção e sinopses
INSERT INTO Filmes (Titulo_Filme, Genero, Duracao, Classificacao, Cartaz_Path, Direcao, Sinopse) VALUES
('Predador terras selvagens', 'terror, suspense, Aventura, Ficção científica', '1h 47m', '12', 'utilidades/images/predador.jpg', 'Dan Trachtenberg', 'Um jovem guerreiro Comanche embarca em uma missão perigosa para proteger sua tribo de uma ameaça alienígena mortal conhecida como Predador. Enquanto luta pela sobrevivência, ele descobre que o caçador extraterrestre está mais avançado e letal do que qualquer inimigo que já enfrentou.'),
('Zootopia', 'Ficção policial, infantil, animação, Aventura, Animação', '1h 50m', 'LIVRE', 'utilidades/images/zootopia.jpg', 'Byron Howard, Rich Moore', 'Em uma cidade habitada por animais antropomórficos, a coelha Judy Hopps se torna a primeira policial coelho e precisa provar seu valor. Ela se une à raposa falastrona Nick Wilde para desvendar um caso misterioso que abala os alicerces de Zootopia, descobrindo uma conspiração que ameaça a harmonia entre as espécies.'),
('Sonic 3', 'animação, ação, aventura, filme familiar', '1h 50m', '12', 'utilidades/images/sonic 3.jpg', 'Jeff Fowler', 'Sonic, Knuckles e Tails se juntam para enfrentar Shadow, um novo e misterioso inimigo com poderes diferentes de tudo que já enfrentaram antes. As habilidades do trio são superadas em todos os aspectos e eles precisam buscar uma improvável aliança.'),
('Interstellar', 'Ficção científica, Ação, Suspense, Aventura', '2h 49m', '10', 'utilidades/images/interstellar.jpg', 'Christopher Nolan', 'Em um futuro onde a Terra está morrendo, um grupo de exploradores embarca na mais importante missão da história da humanidade: viajar através de um buraco de minhoca no espaço em busca de um novo lar para a espécie humana. O ex-piloto Cooper precisa enfrentar os limites do possível para salvar o futuro da humanidade.'),
('Jumanji', 'Comédia, Infantil, Aventura, Ação','1h 59m', 'LIVRE', 'utilidades/images/jumanji.jpg', 'Joe Johnston', 'Dois crianças descobrem um jogo de tabuleiro mágico chamado Jumanji e, ao começarem a jogar, liberam um homem que estava preso no jogo há décadas. Juntos, eles precisam completar a partida para reverter o caos causado pelas perigosas criaturas e fenômenos que escaparam do jogo para o mundo real.'),
('Demon Slayer - Castelo Infinito', 'Ação, Aventura, Fantasia Sombria e Artes Marciais','2h 36m', '18', 'utilidades/images/Demon Slayer.jpg', 'Haruo Sotozaki', 'Tanjiro Kamado e seus companheiros do Corpo de Caçadores de Demônios invadem o Castelo Infinito para enfrentar os Quatro Lunares Superiores e o próprio Muzan Kibutsuji. Nesta batalha épica, eles precisa usar todas as suas habilidades para derrotar os demônios mais poderosos e salvar a irmã de Tanjiro, Nezuko.'),
('Homem-Aranha Sem Volta Para Casa', 'Filme super-herói, Ação, Aventura, Comédia, Suspense', '2h 48m', '12', 'utilidades/images/Homem-aranha Sem volta para casa.jpg', 'Jon Watts', 'Peter Parker pede ao Dr. Estranho para fazer o mundo esquecer que ele é o Homem-Aranha, mas quando o feitiço dá errado, multiversos são abertos trazendo vilões e heróis de outras realidades. Agora, Peter deve enfrentar ameaças de universos alternativos enquanto lida com consequências devastadoras para seu mundo.'),
('Invocação do Mal', 'Terror, Sobrenatural, Mistério, Suspense', '2h 28m', '14', 'utilidades/images/invocação do mal.jpg', 'James Wan', 'Baseado em uma história real, os investigadores paranormais Ed e Lorraine Warren são chamados para ajudar uma família aterrorizada por uma presença obscura em sua fazenda. Eles descobrem que a casa está assombrada por uma entidade demoníaca que ameaça não apenas a família, mas todos que se aproximam do local.'),
('Avatar', 'Ficção Científica, Aventura', '2h 17m', '12', 'utilidades/images/Avata.jpg', 'James Cameron', 'Em um futuro distante, um ex-marine paraplégico é enviado a Pandora, um mundo extraterrestre habitado por seres azuis chamados Navi. Ele deve navegar por este mundo estranho e ameaçador para cumprir sua missão.'),
('Vingadores: Ultimato', 'Ação, Aventura, Ficção Científica', '3h 1m', '12', 'utilidades/images/vingadores.jpg', 'Anthony Russo, Joe Russo', 'Após os eventos devastadores de \'Vingadores: Guerra Infinita\', o universo está em ruínas. Com a ajuda de aliados remanescentes, os Vingadores se reúnem para reverter as ações de Thanos e restaurar a ordem no universo.'),
('Jurassic Park', 'Aventura, Ficção Científica, Suspense', '2h 7m', '10', 'utilidades/images/jurassic_park.jpg', 'Steven Spielberg', 'Um parque temático com dinossauros clonados se torna um pesadelo quando os sistemas de segurança falham, libertando as criaturas pré-históricas.'),
('Halloween', 'Terror, Suspense, ficção Policial, Drama, slashe','1h 46m', '18', 'utilidades/images/halloween.jpg', 'David Gordon Green', '(Halloween (2018) é uma sequência direta do filme original de 1978, onde Laurie Strode (Jamie Lee Curtis) deve enfrentar novamente o serial killer Michael Myers, que escapa de uma instituição psiquiátrica para aterrorizar Haddonfield 40 anos após seu primeiro ataque, agora com uma Laurie preparada e paranoica, que se armou para proteger sua família de seu algoz.'),
('Batman O Cavaleiro das Trevas', 'Ação, Crime, Drama', '2h 32m', '14', 'utilidades/images/batman_cavaleiro.jpg', 'Christopher Nolan', 'Batman enfrenta o Coringa, um criminoso psicótico que deseja mergulhar Gotham City no caos. Enquanto luta contra o vilão, Bruce Wayne também lida com questões pessoais.'),
('it a coisa', 'terror, sobrenatural, mistério, suspense','2h 15m' , '18', 'utilidades/images/it-coisa.jpg', 'Andy Muschietti', 'Um grupo de crianças se une para investigar o misterioso desaparecimento de vários jovens em sua cidade. Eles descobrem que o culpado é Pennywise, um palhaço cruel que se alimenta de seus medos e cuja violência teve origem há vários séculos.'),
('jogos mortais X', 'terror, drama, mistério, suspense, crime', '1h 58m', '18', 'utilidades/images/saw.jpg', 'Kevin Greutert', 'Esperando por uma cura milagrosa, o adoecido John Kramer viaja para o México para um procedimento médico arriscado e experimental. Mas ao chegar no destino, se depara com um ambiente macabro, e descobre que toda a operação é uma farsa para enganar pessoas já vulneráveis. Agora armado com um novo propósito, o infame serial killer usa armadilhas insanas e engenhosas para virar o jogo contra os vigaristas, relembrando o motivo de ser conhecido como o terrível vilão Jigsaw.');

-- Tabela de Sal
DROP TABLE IF EXISTS Salas;
CREATE TABLE Salas (
    ID_Sala INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Sala VARCHAR(50) NOT NULL,
    Capacidade INT
);

-- Tabela de Usuários
DROP TABLE IF EXISTS Usuarios;
CREATE TABLE Usuarios (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Usuario VARCHAR(100) NOT NULL,
    Nome_Login VARCHAR(50) NOT NULL UNIQUE,
    Senha VARCHAR(255) NOT NULL,
    Email VARCHAR(100),
    Telefone VARCHAR(20),
    Genero ENUM('M', 'F', 'Outro'),
    Data_Nascimento DATE,
    Tipo_Usuario ENUM('admin', 'funcionario', 'cliente') DEFAULT 'cliente'
);

-- Tabela de Sessões
DROP TABLE IF EXISTS Sessoes;
CREATE TABLE Sessoes (
    ID_Sessao INT AUTO_INCREMENT PRIMARY KEY,
    ID_Filme INT,
    ID_Sala INT,
    Data_Sessao DATE,
    Hora_Sessao TIME,
    Tipo_Sessao ENUM('dublado', 'legendado') NOT NULL,
    FOREIGN KEY (ID_Filme) REFERENCES Filmes(ID_Filme),
    FOREIGN KEY (ID_Sala) REFERENCES Salas(ID_Sala)
);

-- Tabela de Assentos Base (configuração física das salas)
DROP TABLE IF EXISTS Assentos;
CREATE TABLE Assentos (
    ID_Assento INT AUTO_INCREMENT PRIMARY KEY,
    ID_Sala INT,
    Linha VARCHAR(1),
    Coluna INT,
    FOREIGN KEY (ID_Sala) REFERENCES Salas(ID_Sala)
);

-- Tabela de junção para relacionar assentos com sessões
DROP TABLE IF EXISTS Assentos_Sessao;
CREATE TABLE Assentos_Sessao (
    ID_Assento_Sessao INT AUTO_INCREMENT PRIMARY KEY,
    ID_Sessao INT,
    ID_Assento INT,
    Status ENUM('disponivel', 'ocupado', 'reservado') DEFAULT 'disponivel',
    ID_Cliente INT NULL,
    Data_Hora_Reserva DATETIME NULL,
    FOREIGN KEY (ID_Sessao) REFERENCES Sessoes(ID_Sessao),
    FOREIGN KEY (ID_Assento) REFERENCES Assentos(ID_Assento),
    FOREIGN KEY (ID_Cliente) REFERENCES Usuarios(ID_Usuario),
    UNIQUE KEY unique_assento_sessao (ID_Sessao, ID_Assento)
);

-- Tabela de Ingressos
DROP TABLE IF EXISTS Ingressos;
CREATE TABLE Ingressos (
    ID_Ingresso INT AUTO_INCREMENT PRIMARY KEY,
    ID_Sessao INT,
    ID_Cliente INT,
    ID_Assento_Sessao INT,
    Valor DECIMAL(10,2),
    Data_Compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Sessao) REFERENCES Sessoes(ID_Sessao),
    FOREIGN KEY (ID_Cliente) REFERENCES Usuarios(ID_Usuario),
    FOREIGN KEY (ID_Assento_Sessao) REFERENCES Assentos_Sessao(ID_Assento_Sessao)
);

-- Inserir salas
INSERT INTO Salas (Nome_Sala, Capacidade) VALUES
('Sala 1', 56),
('Sala 2', 56),
('Sala 3', 56),
('Sala 4', 56),
('Sala 5', 56),
('Sala 6', 56),
('Sala 7', 56),
('Sala 8', 56);

-- Procedure para inserir assentos base
DELIMITER //
CREATE PROCEDURE InserirAssentosBase()
BEGIN
    DECLARE sala_id INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT ID_Sala FROM Salas;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO sala_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Inserir assentos para esta sala (7 linhas x 8 colunas = 56 assentos)
        INSERT INTO Assentos (ID_Sala, Linha, Coluna) VALUES
        (sala_id, 'A', 1), (sala_id, 'A', 2), (sala_id, 'A', 3), (sala_id, 'A', 4), 
        (sala_id, 'A', 5), (sala_id, 'A', 6), (sala_id, 'A', 7), (sala_id, 'A', 8),
        (sala_id, 'B', 1), (sala_id, 'B', 2), (sala_id, 'B', 3), (sala_id, 'B', 4), 
        (sala_id, 'B', 5), (sala_id, 'B', 6), (sala_id, 'B', 7), (sala_id, 'B', 8),
        (sala_id, 'C', 1), (sala_id, 'C', 2), (sala_id, 'C', 3), (sala_id, 'C', 4), 
        (sala_id, 'C', 5), (sala_id, 'C', 6), (sala_id, 'C', 7), (sala_id, 'C', 8),
        (sala_id, 'D', 1), (sala_id, 'D', 2), (sala_id, 'D', 3), (sala_id, 'D', 4), 
        (sala_id, 'D', 5), (sala_id, 'D', 6), (sala_id, 'D', 7), (sala_id, 'D', 8),
        (sala_id, 'E', 1), (sala_id, 'E', 2), (sala_id, 'E', 3), (sala_id, 'E', 4), 
        (sala_id, 'E', 5), (sala_id, 'E', 6), (sala_id, 'E', 7), (sala_id, 'E', 8),
        (sala_id, 'F', 1), (sala_id, 'F', 2), (sala_id, 'F', 3), (sala_id, 'F', 4), 
        (sala_id, 'F', 5), (sala_id, 'F', 6), (sala_id, 'F', 7), (sala_id, 'F', 8),
        (sala_id, 'G', 1), (sala_id, 'G', 2), (sala_id, 'G', 3), (sala_id, 'G', 4), 
        (sala_id, 'G', 5), (sala_id, 'G', 6), (sala_id, 'G', 7), (sala_id, 'G', 8);
        
    END LOOP;
    
    CLOSE cur;
END//
DELIMITER ;

-- Procedure para popular assentos por sessão
DELIMITER //
CREATE PROCEDURE PopularAssentosSessao()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE sessao_id INT;
    DECLARE sala_id INT;
    DECLARE cur CURSOR FOR 
        SELECT s.ID_Sessao, s.ID_Sala 
        FROM Sessoes s;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO sessao_id, sala_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Inserir todos os assentos da sala para esta sessão
        INSERT INTO Assentos_Sessao (ID_Sessao, ID_Assento, Status)
        SELECT sessao_id, a.ID_Assento, 'disponivel'
        FROM Assentos a
        WHERE a.ID_Sala = sala_id;
        
    END LOOP;
    
    CLOSE cur;
END//
DELIMITER ;

-- Executar procedures para criar assentos
CALL InserirAssentosBase();

-- Inserir sessões para os filmes
INSERT INTO Sessoes (ID_Filme, ID_Sala, Data_Sessao, Hora_Sessao, Tipo_Sessao) VALUES
-- Predador Terras Selvagens - Sala 1 (Dublado)
(1, 1, '2025-11-06', '14:50', 'dublado'), (1, 1, '2025-11-06', '17:00', 'dublado'), 
(1, 1, '2025-11-06', '20:00', 'dublado'), (1, 1, '2025-11-06', '22:15', 'dublado'),
-- Predador Terras Selvagens - Sala 1 (Legendado)
(1, 1, '2025-11-06', '17:30', 'legendado'), (1, 1, '2025-11-06', '20:45', 'legendado'), 
(1, 1, '2025-11-06', '21:15', 'legendado'),

-- Zootopia - Sala 2 (Dublado)
(2, 2, '2025-03-17', '14:15', 'dublado'), (2, 2, '2025-03-17', '18:00', 'dublado'), 
(2, 2, '2025-03-17', '20:30', 'dublado'), (2, 2, '2025-03-17', '21:00', 'dublado'),
-- Zootopia - Sala 2 (Legendado)
(2, 2, '2025-03-17', '17:00', 'legendado'), (2, 2, '2025-03-17', '20:45', 'legendado'), 
(2, 2, '2025-03-17', '21:15', 'legendado'),

-- Matrix - Sala 3 (Dublado)
(3, 3, '2025-09-11', '14:45', 'dublado'), (3, 3, '2025-09-11', '17:30', 'dublado'), 
(3, 3, '2025-09-11', '19:30', 'dublado'), (3, 3, '2025-09-11', '22:30', 'dublado'),
-- Matrix - Sala 3 (Legendado)
(3, 3, '2025-09-11', '16:50', 'legendado'), (3, 3, '2025-09-11', '19:00', 'legendado'), 
(3, 3, '2025-09-11', '21:30', 'legendado'),

-- Interstellar - Sala 4 (Dublado)
(4, 4, '2025-09-04', '13:00', 'dublado'), (4, 4, '2025-09-04', '16:45', 'dublado'), 
(4, 4, '2025-09-04', '20:30', 'dublado'),
-- Interstellar - Sala 4 (Legendado)
(4, 4, '2025-09-04', '17:00', 'legendado'), (4, 4, '2025-09-04', '20:00', 'legendado'), 
(4, 4, '2025-09-04', '22:30', 'legendado'),

-- Jumanji - Sala 5 (Dublado)
(5, 5, '2025-09-11', '11:30', 'dublado'), (5, 5, '2025-09-11', '15:00', 'dublado'), 
(5, 5, '2025-09-11', '18:00', 'dublado'), (5, 5, '2025-09-11', '21:00', 'dublado'),
-- Jumanji - Sala 5 (Legendado)
(5, 5, '2025-09-11', '18:30', 'legendado'), (5, 5, '2025-09-11', '21:30', 'legendado'),

-- Demon Slayer - Sala 6 (Dublado)
(6, 6, '2025-09-11', '12:00', 'dublado'), (6, 6, '2025-09-11', '16:00', 'dublado'), 
(6, 6, '2025-09-11', '19:45', 'dublado'), (6, 6, '2025-09-11', '22:45', 'dublado'),
-- Demon Slayer - Sala 6 (Legendado)
(6, 6, '2025-09-11', '19:00', 'legendado'), (6, 6, '2025-09-11', '20:45', 'legendado'),

-- Homem-Aranha - Sala 7 (Dublado)
(7, 7, '2025-09-18', '13:30', 'dublado'), (7, 7, '2025-09-18', '17:15', 'dublado'), 
(7, 7, '2025-09-18', '21:00', 'dublado'),
-- Homem-Aranha - Sala 7 (Legendado)
(7, 7, '2025-09-18', '16:20', 'legendado'), (7, 7, '2025-09-18', '19:00', 'legendado'), 
(7, 7, '2025-09-18', '22:30', 'legendado'),

-- Invocação do Mal - Sala 8 (Dublado)
(8, 8, '2025-09-04', '13:00', 'dublado'), (8, 8, '2025-09-04', '16:00', 'dublado'), 
(8, 8, '2025-09-04', '22:00', 'dublado'), (8, 8, '2025-09-04', '23:30', 'dublado'),
-- Invocação do Mal - Sala 8 (Legendado)
(8, 8, '2025-09-04', '17:00', 'legendado'), (8, 8, '2025-09-04', '19:45', 'legendado'), 
(8, 8, '2025-09-04', '23:00', 'legendado'),

-- Avatar - Sala 1 (Dublado)
(9, 1, '2026-01-15', '14:00', 'dublado'), (9, 1, '2026-01-15', '17:30', 'dublado'), 
(9, 1, '2026-01-15', '21:00', 'dublado'),
-- Avatar - Sala 1 (Legendado)
(9, 1, '2026-01-15', '16:00', 'legendado'), (9, 1, '2026-01-15', '19:30', 'legendado'), 
(9, 1, '2026-01-15', '23:00', 'legendado'),

-- Vingadores: Ultimato - Sala 2 (Dublado)
(10, 2, '2026-01-16', '13:30', 'dublado'), (10, 2, '2026-01-16', '17:00', 'dublado'), 
(10, 2, '2026-01-16', '20:30', 'dublado'),
-- Vingadores: Ultimato - Sala 2 (Legendado)
(10, 2, '2026-01-16', '15:30', 'legendado'), (10, 2, '2026-01-16', '19:00', 'legendado'), 
(10, 2, '2026-01-16', '22:30', 'legendado'),

-- Jurassic Park - Sala 3 (Dublado)
(11, 3, '2026-01-17', '14:15', 'dublado'), (11, 3, '2026-01-17', '17:45', 'dublado'), 
(11, 3, '2026-01-17', '21:15', 'dublado'),
-- Jurassic Park - Sala 3 (Legendado)
(11, 3, '2026-01-17', '16:00', 'legendado'), (11, 3, '2026-01-17', '19:30', 'legendado'), 
(11, 3, '2026-01-17', '23:00', 'legendado'),

-- O Senhor dos Anéis - Sala 4 (Dublado)
(12, 4, '2026-01-18', '13:00', 'dublado'), (12, 4, '2026-01-18', '16:30', 'dublado'), 
(12, 4, '2026-01-18', '20:00', 'dublado'),
-- O Senhor dos Anéis - Sala 4 (Legendado)
(12, 4, '2026-01-18', '15:00', 'legendado'), (12, 4, '2026-01-18', '18:30', 'legendado'), 
(12, 4, '2026-01-18', '22:00', 'legendado'),

-- Batman: O Cavaleiro das Trevas - Sala 5 (Dublado)
(13, 5, '2026-01-19', '14:30', 'dublado'), (13, 5, '2026-01-19', '18:00', 'dublado'), 
(13, 5, '2026-01-19', '21:30', 'dublado'),
-- Batman: O Cavaleiro das Trevas - Sala 5 (Legendado)
(13, 5, '2026-01-19', '16:30', 'legendado'), (13, 5, '2026-01-19', '20:00', 'legendado'), 
(13, 5, '2026-01-19', '23:30', 'legendado'),

-- Star Wars - Sala 6 (Dublado)
(14, 6, '2026-01-20', '13:15', 'dublado'), (14, 6, '2026-01-20', '16:45', 'dublado'), 
(14, 6, '2026-01-20', '20:15', 'dublado'),
-- Star Wars - Sala 6 (Legendado)
(14, 6, '2026-01-20', '15:00', 'legendado'), (14, 6, '2026-01-20', '18:30', 'legendado'), 
(14, 6, '2026-01-20', '22:00', 'legendado'),

-- Mad Max: Estrada da Fúria - Sala 7 (Dublado)
(15, 7, '2026-01-21', '14:45', 'dublado'), (15, 7, '2026-01-21', '18:15', 'dublado'), 
(15, 7, '2026-01-21', '21:45', 'dublado'),
-- Mad Max: Estrada da Fúria - Sala 7 (Legendado)
(15, 7, '2026-01-21', '16:45', 'legendado'), (15, 7, '2026-01-21', '20:15', 'legendado'), 
(15, 7, '2026-01-21', '23:45', 'legendado');

-- Popular assentos para todas as sessões
CALL PopularAssentosSessao();

-- Inserir usuário administrador
INSERT INTO Usuarios (Nome_Usuario, Nome_Login, Senha, Email, Telefone, Genero, Data_Nascimento, Tipo_Usuario) VALUES
('Frederico Lopes', 'frico_admin', '@Caligula10', 'fhrl@cineplus.com', '(91)981731270', 'M', '1996-08-19', 'funcionario');

-- Limpar as procedures após uso
DROP PROCEDURE InserirAssentosBase;
DROP PROCEDURE PopularAssentosSessao;

-- Consulta exemplo para verificar assentos disponíveis por sessão
SELECT 
    s.ID_Sessao,
    f.Titulo_Filme,
    sa.Nome_Sala,
    s.Data_Sessao,
    s.Hora_Sessao,
    s.Tipo_Sessao,
    a.Linha,
    a.Coluna,
    ass.Status
FROM Sessoes s
JOIN Filmes f ON s.ID_Filme = f.ID_Filme
JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
JOIN Assentos_Sessao ass ON s.ID_Sessao = ass.ID_Sessao
JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
WHERE s.ID_Sessao = 1
ORDER BY a.Linha, a.Coluna;
ALTER TABLE Usuarios 
MODIFY Tipo_Usuario ENUM('admin', 'gerente', 'funcionario', 'cliente') 
DEFAULT 'cliente';

INSERT INTO Usuarios (Nome_Usuario, Nome_Login, Senha, Email, Telefone, Genero, Data_Nascimento, Tipo_Usuario) VALUES
('Gerente Cinema', 'gerente', 'senha', 'gerente', '(11)99999-0002', 'M', '1985-05-15', 'gerente'),
('Atendente 1', 'func', 'senha', 'func', '(11)99999-0003', 'F', '1995-08-20', 'funcionario'),
('Cliente Regular', 'cliente1', 'senha', 'cliente', '(11)99999-0005', 'F', '2000-07-25', 'cliente');


-- Configuração inicial
SET @id_atual = (SELECT COALESCE(MAX(ID_Ingresso), 0) FROM ingressos);
SET @data_base = '2026-01-19';
SET @ano_dias = 365;
SET @max_sessoes = (SELECT MAX(ID_Sessao) FROM sessoes);

-- Inserir ingressos para um ano inteiro
INSERT INTO ingressos (ID_Ingresso, ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra)
SELECT 
    @id_atual := @id_atual + 1,
    -- Distribuir sessões uniformemente (todas as sessões disponíveis)
    FLOOR(1 + (RAND() * (@max_sessoes - 0.999999))),
    
    -- Clientes existentes (ajuste conforme sua tabela clientes)
    FLOOR(4 + (RAND() * 96)),
    
    -- Assentos disponíveis (ajuste conforme sua capacidade)
    FLOOR(1 + (RAND() * 500)),
    
    -- Valor variável com base no tipo de sessão (exemplo)
    CASE 
        WHEN RAND() < 0.3 THEN 25.00  -- Sessão normal
        WHEN RAND() < 0.6 THEN 35.00  -- 3D
        ELSE 45.00                    -- VIP/IMAX
    END,
    
    -- Data de compra (horários distribuídos ao longo do dia)
    TIMESTAMPADD(SECOND, FLOOR(RAND() * 86400), 
                DATE_ADD(@data_base, INTERVAL n.day_offset DAY))
FROM (
    -- Gerar todos os dias do ano
    SELECT n AS day_offset
    FROM (
        SELECT @row := @row + 1 AS n
        FROM 
            (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) a,
            (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) b,
            (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) c,
            (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) d,
            (SELECT @row := -1) r
        WHERE @row < @ano_dias - 1
    ) days
) n
CROSS JOIN (
    -- Gerar múltiplos ingressos por dia
    -- Mais ingressos nos fins de semana e feriados
    SELECT a.N + b.N * 10 + c.N * 100 + 1 as seq
    FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 
         UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 
         UNION SELECT 8 UNION SELECT 9) a,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 
         UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 
         UNION SELECT 8 UNION SELECT 9) b,
        (SELECT 0 AS N UNION SELECT 1) c
) seq
WHERE seq.seq <= (
    -- Quantidade variável de ingressos por dia
    CASE 
        -- Fins de semana: mais ingressos
        WHEN DAYOFWEEK(DATE_ADD(@data_base, INTERVAL n.day_offset DAY)) IN (1, 7) 
        THEN FLOOR(100 + (RAND() * 150))
        
        -- Sexta-feira: movimento médio-alto
        WHEN DAYOFWEEK(DATE_ADD(@data_base, INTERVAL n.day_offset DAY)) = 6 
        THEN FLOOR(80 + (RAND() * 120))
        
        -- Dias de semana normais
        ELSE FLOOR(30 + (RAND() * 70))
    END
)
-- Limitar para evitar sobrecarga (ajuste conforme necessário)
LIMIT 100000;