CREATE DATABASE IF NOT EXISTS cineplus;
USE cineplus;

-- Tabela de Filmes
DROP TABLE IF EXISTS Filmes;
CREATE TABLE Filmes (
    ID_Filme INT AUTO_INCREMENT PRIMARY KEY,
    Titulo_Filme VARCHAR(255) NOT NULL,
    Genero VARCHAR(50),
    Duracao INT,
    Classificacao VARCHAR(10),
    Cartaz_Path VARCHAR(500),
    Direcao VARCHAR(255),
    Sinopse TEXT
);

-- Inserir os filmes com os caminhos dos cartazes, direção e sinopses
INSERT INTO Filmes (Titulo_Filme, Genero, Duracao, Classificacao, Cartaz_Path, Direcao, Sinopse) VALUES
('predador terras selvagens', 'terror, suspense, Aventura, Ficção científica', 98, '12', 'utilidades/images/predador.jpg', 'Dan Trachtenberg', 'Um jovem guerreiro Comanche embarca em uma missão perigosa para proteger sua tribo de uma ameaça alienígena mortal conhecida como Predador. Enquanto luta pela sobrevivência, ele descobre que o caçador extraterrestre está mais avançado e letal do que qualquer inimigo que já enfrentou.'),
('zootopia', 'Ficção policial, infantil, animação, Aventura, Animação', 108, 'LIVRE', 'utilidades/images/zootopia.jpg', 'Byron Howard, Rich Moore', 'Em uma cidade habitada por animais antropomórficos, a coelha Judy Hopps se torna a primeira policial coelho e precisa provar seu valor. Ela se une à raposa falastrona Nick Wilde para desvendar um caso misterioso que abala os alicerces de Zootopia, descobrindo uma conspiração que ameaça a harmonia entre as espécies.'),
('Matrix', 'Ação, Aventura, Ficção científica, Cyberpunk', 109, '14', 'utilidades/images/matrix.jpg', 'Lana Wachowski, Lilly Wachowski', 'Um hacker de computador chamado Neo descobre que a realidade como conhecemos é na verdade uma simulação chamada Matrix, criada por máquinas inteligentes para subjugar a humanidade. Ele se junta a um grupo de rebeldes liderados por Morpheus e Trinity para lutar contra o sistema e descobrir seu verdadeiro destino como "O Escolhido".'),
('Interstellar', 'Ficção científica, Ação, Suspense, Aventura', 87, '10', 'utilidades/images/interstellar.jpg', 'Christopher Nolan', 'Em um futuro onde a Terra está morrendo, um grupo de exploradores embarca na mais importante missão da história da humanidade: viajar através de um buraco de minhoca no espaço em busca de um novo lar para a espécie humana. O ex-piloto Cooper precisa enfrentar os limites do possível para salvar o futuro da humanidade.'),
('Jumanji', 'Comédia, Infantil, Aventura, Ação', 90, 'LIVRE', 'utilidades/images/jumanji.jpg', 'Joe Johnston', 'Dois crianças descobrem um jogo de tabuleiro mágico chamado Jumanji e, ao começarem a jogar, liberam um homem que estava preso no jogo há décadas. Juntos, eles precisam completar a partida para reverter o caos causado pelas perigosas criaturas e fenômenos que escaparam do jogo para o mundo real.'),
('Demon Slayer - Castelo Infinito', 'Ação, Aventura, Fantasia Sombria e Artes Marciais', 156, '18', 'utilidades/images/Demon Slayer.jpg', 'Haruo Sotozaki', 'Tanjiro Kamado e seus companheiros do Corpo de Caçadores de Demônios invadem o Castelo Infinito para enfrentar os Quatro Lunares Superiores e o próprio Muzan Kibutsuji. Nesta batalha épica, eles precisa usar todas as suas habilidades para derrotar os demônios mais poderosos e salvar a irmã de Tanjiro, Nezuko.'),
('Homem-Aranha Sem Volta Para Casa', 'Filme super-herói, Ação, Aventura, Comédia, Suspense', 98, '12', 'utilidades/images/Homem-aranha Sem volta para casa.jpg', 'Jon Watts', 'Peter Parker pede ao Dr. Estranho para fazer o mundo esquecer que ele é o Homem-Aranha, mas quando o feitiço dá errado, multiversos são abertos trazendo vilões e heróis de outras realidades. Agora, Peter deve enfrentar ameaças de universos alternativos enquanto lida com consequências devastadoras para seu mundo.'),
('Invocação do Mal', 'Terror, Sobrenatural, Mistério, Suspense', 135, '14', 'utilidades/images/invocação do mal.jpg', 'James Wan', 'Baseado em uma história real, os investigadores paranormais Ed e Lorraine Warren são chamados para ajudar uma família aterrorizada por uma presença obscura em sua fazenda. Eles descobrem que a casa está assombrada por uma entidade demoníaca que ameaça não apenas a família, mas todos que se aproximam do local.');

-- Tabela de Salas
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
(8, 8, '2025-09-04', '23:00', 'legendado');

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



-- Inserir ingressos de exemplo para um ano inteiro (5 dias por mês)
INSERT INTO Ingressos (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra) VALUES
-- Janeiro 2025 (Dias 5, 10, 15, 20, 25)
(1, 4, 1, 35.00, '2025-01-05 10:30:00'), (1, 4, 2, 35.00, '2025-01-05 10:31:00'),
(2, 4, 9, 35.00, '2025-01-05 11:15:00'), (2, 4, 10, 35.00, '2025-01-05 11:16:00'),
(5, 4, 33, 35.00, '2025-01-10 14:20:00'), (5, 4, 34, 35.00, '2025-01-10 14:21:00'),
(10, 4, 89, 35.00, '2025-01-10 16:45:00'), (10, 4, 90, 35.00, '2025-01-10 16:46:00'),
(15, 4, 145, 35.00, '2025-01-15 19:10:00'), (15, 4, 146, 35.00, '2025-01-15 19:11:00'),
(20, 4, 201, 35.00, '2025-01-15 21:30:00'), (20, 4, 202, 35.00, '2025-01-15 21:31:00'),
(25, 4, 257, 35.00, '2025-01-20 13:15:00'), (25, 4, 258, 35.00, '2025-01-20 13:16:00'),
(30, 4, 313, 35.00, '2025-01-20 15:40:00'), (30, 4, 314, 35.00, '2025-01-20 15:41:00'),
(35, 4, 369, 35.00, '2025-01-25 18:20:00'), (35, 4, 370, 35.00, '2025-01-25 18:21:00'),
(40, 4, 425, 35.00, '2025-01-25 20:50:00'), (40, 4, 426, 35.00, '2025-01-25 20:51:00'),

-- Fevereiro 2025 (Dias 3, 8, 13, 18, 23)
(1, 4, 3, 35.00, '2025-02-03 11:45:00'), (1, 4, 4, 35.00, '2025-02-03 11:46:00'),
(2, 4, 11, 35.00, '2025-02-03 12:30:00'), (2, 4, 12, 35.00, '2025-02-03 12:31:00'),
(5, 4, 35, 35.00, '2025-02-08 15:10:00'), (5, 4, 36, 35.00, '2025-02-08 15:11:00'),
(10, 4, 91, 35.00, '2025-02-08 17:35:00'), (10, 4, 92, 35.00, '2025-02-08 17:36:00'),
(15, 4, 147, 35.00, '2025-02-13 20:00:00'), (15, 4, 148, 35.00, '2025-02-13 20:01:00'),
(20, 4, 203, 35.00, '2025-02-13 22:20:00'), (20, 4, 204, 35.00, '2025-02-13 22:21:00'),
(25, 4, 259, 35.00, '2025-02-18 14:05:00'), (25, 4, 260, 35.00, '2025-02-18 14:06:00'),
(30, 4, 315, 35.00, '2025-02-18 16:30:00'), (30, 4, 316, 35.00, '2025-02-18 16:31:00'),
(35, 4, 371, 35.00, '2025-02-23 19:10:00'), (35, 4, 372, 35.00, '2025-02-23 19:11:00'),
(40, 4, 427, 35.00, '2025-02-23 21:40:00'), (40, 4, 428, 35.00, '2025-02-23 21:41:00'),

-- Março 2025 (Dias 2, 7, 12, 17, 22)
(1, 4, 5, 35.00, '2025-03-02 13:00:00'), (1, 4, 6, 35.00, '2025-03-02 13:01:00'),
(2, 4, 13, 35.00, '2025-03-02 13:45:00'), (2, 4, 14, 35.00, '2025-03-02 13:46:00'),
(5, 4, 37, 35.00, '2025-03-07 16:00:00'), (5, 4, 38, 35.00, '2025-03-07 16:01:00'),
(10, 4, 93, 35.00, '2025-03-07 18:25:00'), (10, 4, 94, 35.00, '2025-03-07 18:26:00'),
(15, 4, 149, 35.00, '2025-03-12 20:50:00'), (15, 4, 150, 35.00, '2025-03-12 20:51:00'),
(20, 4, 205, 35.00, '2025-03-12 23:10:00'), (20, 4, 206, 35.00, '2025-03-12 23:11:00'),
(25, 4, 261, 35.00, '2025-03-17 14:55:00'), (25, 4, 262, 35.00, '2025-03-17 14:56:00'),
(30, 4, 317, 35.00, '2025-03-17 17:20:00'), (30, 4, 318, 35.00, '2025-03-17 17:21:00'),
(35, 4, 373, 35.00, '2025-03-22 20:00:00'), (35, 4, 374, 35.00, '2025-03-22 20:01:00'),
(40, 4, 429, 35.00, '2025-03-22 22:30:00'), (40, 4, 430, 35.00, '2025-03-22 22:31:00'),

-- Abril 2025 (Dias 1, 6, 11, 16, 21)
(1, 4, 7, 35.00, '2025-04-01 14:15:00'), (1, 4, 8, 35.00, '2025-04-01 14:16:00'),
(2, 4, 15, 35.00, '2025-04-01 15:00:00'), (2, 4, 16, 35.00, '2025-04-01 15:01:00'),
(5, 4, 39, 35.00, '2025-04-06 16:50:00'), (5, 4, 40, 35.00, '2025-04-06 16:51:00'),
(10, 4, 95, 35.00, '2025-04-06 19:15:00'), (10, 4, 96, 35.00, '2025-04-06 19:16:00'),
(15, 4, 151, 35.00, '2025-04-11 21:40:00'), (15, 4, 152, 35.00, '2025-04-11 21:41:00'),
(20, 4, 207, 35.00, '2025-04-12 00:00:00'), (20, 4, 208, 35.00, '2025-04-12 00:01:00'),
(25, 4, 263, 35.00, '2025-04-16 15:45:00'), (25, 4, 264, 35.00, '2025-04-16 15:46:00'),
(30, 4, 319, 35.00, '2025-04-16 18:10:00'), (30, 4, 320, 35.00, '2025-04-16 18:11:00'),
(35, 4, 375, 35.00, '2025-04-21 20:50:00'), (35, 4, 376, 35.00, '2025-04-21 20:51:00'),
(40, 4, 431, 35.00, '2025-04-21 23:20:00'), (40, 4, 432, 35.00, '2025-04-21 23:21:00'),

-- Maio 2025 (Dias 5, 10, 15, 20, 25)
(1, 4, 17, 35.00, '2025-05-05 15:30:00'), (1, 4, 18, 35.00, '2025-05-05 15:31:00'),
(2, 4, 25, 35.00, '2025-05-05 16:15:00'), (2, 4, 26, 35.00, '2025-05-05 16:16:00'),
(5, 4, 49, 35.00, '2025-05-10 17:40:00'), (5, 4, 50, 35.00, '2025-05-10 17:41:00'),
(10, 4, 105, 35.00, '2025-05-10 20:05:00'), (10, 4, 106, 35.00, '2025-05-10 20:06:00'),
(15, 4, 161, 35.00, '2025-05-15 22:30:00'), (15, 4, 162, 35.00, '2025-05-15 22:31:00'),
(20, 4, 217, 35.00, '2025-05-16 00:50:00'), (20, 4, 218, 35.00, '2025-05-16 00:51:00'),
(25, 4, 273, 35.00, '2025-05-20 16:35:00'), (25, 4, 274, 35.00, '2025-05-20 16:36:00'),
(30, 4, 329, 35.00, '2025-05-20 19:00:00'), (30, 4, 330, 35.00, '2025-05-20 19:01:00'),
(35, 4, 385, 35.00, '2025-05-25 21:40:00'), (35, 4, 386, 35.00, '2025-05-25 21:41:00'),
(40, 4, 441, 35.00, '2025-05-26 00:10:00'), (40, 4, 442, 35.00, '2025-05-26 00:11:00'),

-- Junho 2025 (Dias 4, 9, 14, 19, 24)
(1, 4, 19, 35.00, '2025-06-04 16:45:00'), (1, 4, 20, 35.00, '2025-06-04 16:46:00'),
(2, 4, 27, 35.00, '2025-06-04 17:30:00'), (2, 4, 28, 35.00, '2025-06-04 17:31:00'),
(5, 4, 51, 35.00, '2025-06-09 18:30:00'), (5, 4, 52, 35.00, '2025-06-09 18:31:00'),
(10, 4, 107, 35.00, '2025-06-09 20:55:00'), (10, 4, 108, 35.00, '2025-06-09 20:56:00'),
(15, 4, 163, 35.00, '2025-06-14 23:20:00'), (15, 4, 164, 35.00, '2025-06-14 23:21:00'),
(20, 4, 219, 35.00, '2025-06-15 01:40:00'), (20, 4, 220, 35.00, '2025-06-15 01:41:00'),
(25, 4, 275, 35.00, '2025-06-19 17:25:00'), (25, 4, 276, 35.00, '2025-06-19 17:26:00'),
(30, 4, 331, 35.00, '2025-06-19 19:50:00'), (30, 4, 332, 35.00, '2025-06-19 19:51:00'),
(35, 4, 387, 35.00, '2025-06-24 22:30:00'), (35, 4, 388, 35.00, '2025-06-24 22:31:00'),
(40, 4, 443, 35.00, '2025-06-25 01:00:00'), (40, 4, 444, 35.00, '2025-06-25 01:01:00'),

-- Julho 2025 (Dias 3, 8, 13, 18, 23)
(1, 4, 21, 35.00, '2025-07-03 18:00:00'), (1, 4, 22, 35.00, '2025-07-03 18:01:00'),
(2, 4, 29, 35.00, '2025-07-03 18:45:00'), (2, 4, 30, 35.00, '2025-07-03 18:46:00'),
(5, 4, 53, 35.00, '2025-07-08 19:20:00'), (5, 4, 54, 35.00, '2025-07-08 19:21:00'),
(10, 4, 109, 35.00, '2025-07-08 21:45:00'), (10, 4, 110, 35.00, '2025-07-08 21:46:00'),
(15, 4, 165, 35.00, '2025-07-14 00:10:00'), (15, 4, 166, 35.00, '2025-07-14 00:11:00'),
(20, 4, 221, 35.00, '2025-07-14 02:30:00'), (20, 4, 222, 35.00, '2025-07-14 02:31:00'),
(25, 4, 277, 35.00, '2025-07-18 18:15:00'), (25, 4, 278, 35.00, '2025-07-18 18:16:00'),
(30, 4, 333, 35.00, '2025-07-18 20:40:00'), (30, 4, 334, 35.00, '2025-07-18 20:41:00'),
(35, 4, 389, 35.00, '2025-07-23 23:20:00'), (35, 4, 390, 35.00, '2025-07-23 23:21:00'),
(40, 4, 445, 35.00, '2025-07-24 01:50:00'), (40, 4, 446, 35.00, '2025-07-24 01:51:00'),

-- Agosto 2025 (Dias 2, 7, 12, 17, 22)
(1, 4, 23, 35.00, '2025-08-02 19:15:00'), (1, 4, 24, 35.00, '2025-08-02 19:16:00'),
(2, 4, 31, 35.00, '2025-08-02 20:00:00'), (2, 4, 32, 35.00, '2025-08-02 20:01:00'),
(5, 4, 55, 35.00, '2025-08-07 20:10:00'), (5, 4, 56, 35.00, '2025-08-07 20:11:00'),
(10, 4, 111, 35.00, '2025-08-07 22:35:00'), (10, 4, 112, 35.00, '2025-08-07 22:36:00'),
(15, 4, 167, 35.00, '2025-08-12 01:00:00'), (15, 4, 168, 35.00, '2025-08-12 01:01:00'),
(20, 4, 223, 35.00, '2025-08-12 03:20:00'), (20, 4, 224, 35.00, '2025-08-12 03:21:00'),
(25, 4, 279, 35.00, '2025-08-17 19:05:00'), (25, 4, 280, 35.00, '2025-08-17 19:06:00'),
(30, 4, 335, 35.00, '2025-08-17 21:30:00'), (30, 4, 336, 35.00, '2025-08-17 21:31:00'),
(35, 4, 391, 35.00, '2025-08-22 00:10:00'), (35, 4, 392, 35.00, '2025-08-22 00:11:00'),
(40, 4, 447, 35.00, '2025-08-22 02:40:00'), (40, 4, 448, 35.00, '2025-08-22 02:41:00'),

-- Setembro 2025 (Dias 1, 6, 11, 16, 21)
(1, 4, 41, 35.00, '2025-09-01 20:30:00'), (1, 4, 42, 35.00, '2025-09-01 20:31:00'),
(2, 4, 49, 35.00, '2025-09-01 21:15:00'), (2, 4, 50, 35.00, '2025-09-01 21:16:00'),
(5, 4, 73, 35.00, '2025-09-06 21:00:00'), (5, 4, 74, 35.00, '2025-09-06 21:01:00'),
(10, 4, 129, 35.00, '2025-09-06 23:25:00'), (10, 4, 130, 35.00, '2025-09-06 23:26:00'),
(15, 4, 185, 35.00, '2025-09-11 01:50:00'), (15, 4, 186, 35.00, '2025-09-11 01:51:00'),
(20, 4, 241, 35.00, '2025-09-11 04:10:00'), (20, 4, 242, 35.00, '2025-09-11 04:11:00'),
(25, 4, 297, 35.00, '2025-09-16 19:55:00'), (25, 4, 298, 35.00, '2025-09-16 19:56:00'),
(30, 4, 353, 35.00, '2025-09-16 22:20:00'), (30, 4, 354, 35.00, '2025-09-16 22:21:00'),
(35, 4, 409, 35.00, '2025-09-21 01:00:00'), (35, 4, 410, 35.00, '2025-09-21 01:01:00'),
(40, 4, 465, 35.00, '2025-09-21 03:30:00'), (40, 4, 466, 35.00, '2025-09-21 03:31:00'),

-- Outubro 2025 (Dias 5, 10, 15, 20, 25)
(1, 4, 43, 35.00, '2025-10-05 21:45:00'), (1, 4, 44, 35.00, '2025-10-05 21:46:00'),
(2, 4, 51, 35.00, '2025-10-05 22:30:00'), (2, 4, 52, 35.00, '2025-10-05 22:31:00'),
(5, 4, 75, 35.00, '2025-10-10 21:50:00'), (5, 4, 76, 35.00, '2025-10-10 21:51:00'),
(10, 4, 131, 35.00, '2025-10-11 00:15:00'), (10, 4, 132, 35.00, '2025-10-11 00:16:00'),
(15, 4, 187, 35.00, '2025-10-15 02:40:00'), (15, 4, 188, 35.00, '2025-10-15 02:41:00'),
(20, 4, 243, 35.00, '2025-10-15 05:00:00'), (20, 4, 244, 35.00, '2025-10-15 05:01:00'),
(25, 4, 299, 35.00, '2025-10-20 20:45:00'), (25, 4, 300, 35.00, '2025-10-20 20:46:00'),
(30, 4, 355, 35.00, '2025-10-20 23:10:00'), (30, 4, 356, 35.00, '2025-10-20 23:11:00'),
(35, 4, 411, 35.00, '2025-10-25 01:50:00'), (35, 4, 412, 35.00, '2025-10-25 01:51:00'),
(40, 4, 467, 35.00, '2025-10-25 04:20:00'), (40, 4, 468, 35.00, '2025-10-25 04:21:00'),

-- Novembro 2025 (Dias 4, 9, 14, 19, 24)
(1, 4, 45, 35.00, '2025-11-04 23:00:00'), (1, 4, 46, 35.00, '2025-11-04 23:01:00'),
(2, 4, 53, 35.00, '2025-11-04 23:45:00'), (2, 4, 54, 35.00, '2025-11-04 23:46:00'),
(5, 4, 77, 35.00, '2025-11-09 22:40:00'), (5, 4, 78, 35.00, '2025-11-09 22:41:00'),
(10, 4, 133, 35.00, '2025-11-10 01:05:00'), (10, 4, 134, 35.00, '2025-11-10 01:06:00'),
(15, 4, 189, 35.00, '2025-11-14 03:30:00'), (15, 4, 190, 35.00, '2025-11-14 03:31:00'),
(20, 4, 245, 35.00, '2025-11-14 05:50:00'), (20, 4, 246, 35.00, '2025-11-14 05:51:00'),
(25, 4, 301, 35.00, '2025-11-19 21:35:00'), (25, 4, 302, 35.00, '2025-11-19 21:36:00'),
(30, 4, 357, 35.00, '2025-11-20 00:00:00'), (30, 4, 358, 35.00, '2025-11-20 00:01:00'),
(35, 4, 413, 35.00, '2025-11-24 02:40:00'), (35, 4, 414, 35.00, '2025-11-24 02:41:00'),
(40, 4, 469, 35.00, '2025-11-24 05:10:00'), (40, 4, 470, 35.00, '2025-11-24 05:11:00'),

-- Dezembro 2025 (Dias 3, 8, 13, 18, 23)
(1, 4, 47, 35.00, '2025-12-03 00:15:00'), (1, 4, 48, 35.00, '2025-12-03 00:16:00'),
(2, 4, 55, 35.00, '2025-12-03 01:00:00'), (2, 4, 56, 35.00, '2025-12-03 01:01:00'),
(5, 4, 79, 35.00, '2025-12-08 23:30:00'), (5, 4, 80, 35.00, '2025-12-08 23:31:00'),
(10, 4, 135, 35.00, '2025-12-09 01:55:00'), (10, 4, 136, 35.00, '2025-12-09 01:56:00'),
(15, 4, 191, 35.00, '2025-12-13 04:20:00'), (15, 4, 192, 35.00, '2025-12-13 04:21:00'),
(20, 4, 247, 35.00, '2025-12-13 06:40:00'), (20, 4, 248, 35.00, '2025-12-13 06:41:00'),
(25, 4, 303, 35.00, '2025-12-18 22:25:00'), (25, 4, 304, 35.00, '2025-12-18 22:26:00'),
(30, 4, 359, 35.00, '2025-12-19 00:50:00'), (30, 4, 360, 35.00, '2025-12-19 00:51:00'),
(35, 4, 415, 35.00, '2025-12-23 03:30:00'), (35, 4, 416, 35.00, '2025-12-23 03:31:00'),
(40, 4, 471, 35.00, '2025-12-23 06:00:00'), (40, 4, 472, 35.00, '2025-12-23 06:01:00'),

-- Janeiro 2026 (Dias 2, 7, 12, 17, 22)
(1, 4, 57, 35.00, '2026-01-02 01:30:00'), (1, 4, 58, 35.00, '2026-01-02 01:31:00'),
(2, 4, 65, 35.00, '2026-01-02 02:15:00'), (2, 4, 66, 35.00, '2026-01-02 02:16:00'),
(5, 4, 89, 35.00, '2026-01-07 00:20:00'), (5, 4, 90, 35.00, '2026-01-07 00:21:00'),
(10, 4, 145, 35.00, '2026-01-07 02:45:00'), (10, 4, 146, 35.00, '2026-01-07 02:46:00'),
(15, 4, 201, 35.00, '2026-01-12 05:10:00'), (15, 4, 202, 35.00, '2026-01-12 05:11:00'),
(20, 4, 257, 35.00, '2026-01-12 07:30:00'), (20, 4, 258, 35.00, '2026-01-12 07:31:00'),
(25, 4, 313, 35.00, '2026-01-17 23:15:00'), (25, 4, 314, 35.00, '2026-01-17 23:16:00'),
(30, 4, 369, 35.00, '2026-01-18 01:40:00'), (30, 4, 370, 35.00, '2026-01-18 01:41:00'),
(35, 4, 425, 35.00, '2026-01-22 04:20:00'), (35, 4, 426, 35.00, '2026-01-22 04:21:00'),
(40, 4, 481, 35.00, '2026-01-22 06:50:00'), (40, 4, 482, 35.00, '2026-01-22 06:51:00');

