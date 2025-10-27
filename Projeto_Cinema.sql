CREATE DATABASE IF NOT EXISTS cineplus;
USE cineplus;
DROP TABLE IF EXISTS Filmes;

CREATE TABLE Filmes (
    ID_Filme INT AUTO_INCREMENT PRIMARY KEY,
    Titulo_Filme VARCHAR(255) NOT NULL,
    Genero VARCHAR(50),
    Duracao INT,
    Classificacao VARCHAR(10),
    Cartaz_Path VARCHAR(500)
);

-- Inserir os filmes com os caminhos dos cartazes
INSERT INTO Filmes (Titulo_Filme, Genero, Duracao, Classificacao, Cartaz_Path) VALUES
('predador terras selvagens', 'terror, suspense, Aventura, Ficção científica', 98, '12', 'utilidades/images/predador.jpg'),
('zootopia', 'Ficção policial, infantil, animação, Aventura, Animação', 108, 'LIVRE', 'utilidades/images/zootopia.jpg'),
('Matrix', 'Ação, Aventura, Ficção científica, Cyberpunk', 109, '14', 'utilidades/images/matrix.jpg'),
('Interstellar', 'Ficção científica, Ação, Suspense, Aventura', 87, '10', 'utilidades/images/interstellar.jpg'),
('Jumanji', 'Comédia, Infantil, Aventura, Ação', 90, 'LIVRE', 'utilidades/images/jumanji.jpg'),
('Demon Slayer - Castelo Infinito', 'Ação, Aventura, Fantasia Sombria e Artes Marciais', 156, '18', 'utilidades/images/Demon Slayer.jpg'),
('Homem-Aranha Sem Volta Para Casa', 'Filme super-herói, Ação, Aventura, Comédia, Suspense', 98, '12', 'utilidades/images/Homem-aranha Sem volta para casa.jpg'),
('Invocação do Mal', 'Terror, Sobrenatural, Mistério, Suspense', 135, '14', 'utilidades/images/invocação do mal.jpg');

CREATE TABLE Salas (
    ID_Sala INT AUTO_INCREMENT PRIMARY KEY,
    Nome_Sala VARCHAR(50) NOT NULL,
    Capacidade INT
);

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


CREATE TABLE Ingressos (
    ID_Ingresso INT AUTO_INCREMENT PRIMARY KEY,
    ID_Sessao INT,
    ID_Cliente INT,
    Valor DECIMAL(10,2),
    Data_Compra DATE,
    FOREIGN KEY (ID_Sessao) REFERENCES Sessoes(ID_Sessao),
    FOREIGN KEY (ID_Cliente) REFERENCES Clientes(ID_Cliente)
);

CREATE TABLE IF NOT EXISTS Assentos (
    ID_Assento INT AUTO_INCREMENT PRIMARY KEY,
    ID_Sala INT,
    Linha VARCHAR(1),
    Coluna INT,
    Status ENUM('disponivel', 'ocupado') DEFAULT 'disponivel',
    FOREIGN KEY (ID_Sala) REFERENCES Salas(ID_Sala)
);

-- Criar salas
INSERT INTO Salas (Nome_Sala, Capacidade) VALUES
('Sala 1', 56),
('Sala 2', 56),
('Sala 3', 56),
('Sala 4', 56),
('Sala 5', 56),
('Sala 6', 56),
('Sala 7', 56),
('Sala 8', 56);

-- Inserir assentos para cada sala (7 linhas x 8 colunas = 56 assentos por sala)
DELIMITER //
CREATE PROCEDURE InserirAssentos()
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
        
        -- Inserir assentos para esta sala
        INSERT INTO Assentos (ID_Sala, Linha, Coluna) VALUES
        (sala_id, 'A', 1), (sala_id, 'A', 2), (sala_id, 'A', 3), (sala_id, 'A', 4), (sala_id, 'A', 5), (sala_id, 'A', 6), (sala_id, 'A', 7), (sala_id, 'A', 8),
        (sala_id, 'B', 1), (sala_id, 'B', 2), (sala_id, 'B', 3), (sala_id, 'B', 4), (sala_id, 'B', 5), (sala_id, 'B', 6), (sala_id, 'B', 7), (sala_id, 'B', 8),
        (sala_id, 'C', 1), (sala_id, 'C', 2), (sala_id, 'C', 3), (sala_id, 'C', 4), (sala_id, 'C', 5), (sala_id, 'C', 6), (sala_id, 'C', 7), (sala_id, 'C', 8),
        (sala_id, 'D', 1), (sala_id, 'D', 2), (sala_id, 'D', 3), (sala_id, 'D', 4), (sala_id, 'D', 5), (sala_id, 'D', 6), (sala_id, 'D', 7), (sala_id, 'D', 8),
        (sala_id, 'E', 1), (sala_id, 'E', 2), (sala_id, 'E', 3), (sala_id, 'E', 4), (sala_id, 'E', 5), (sala_id, 'E', 6), (sala_id, 'E', 7), (sala_id, 'E', 8),
        (sala_id, 'F', 1), (sala_id, 'F', 2), (sala_id, 'F', 3), (sala_id, 'F', 4), (sala_id, 'F', 5), (sala_id, 'F', 6), (sala_id, 'F', 7), (sala_id, 'F', 8),
        (sala_id, 'G', 1), (sala_id, 'G', 2), (sala_id, 'G', 3), (sala_id, 'G', 4), (sala_id, 'G', 5), (sala_id, 'G', 6), (sala_id, 'G', 7), (sala_id, 'G', 8);
        
    END LOOP;
    
    CLOSE cur;
END//
DELIMITER ;

-- Executar a procedure para inserir assentos
CALL InserirAssentos();

-- Inserir sessões para os filmes COM TIPO DE SESSÃO
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

-- Limpar a procedure após uso
DROP PROCEDURE InserirAssentos;

INSERT INTO Usuarios(Nome_Usuario,Nome_Login,Senha,Email,telefone,Genero,Data_Nascimento,Tipo_Usuario) VALUES
("Frederico Lopes","frico_admin","@Caligula10","fhrl@cineplus.com","(91)981731270","M","1996-08-19","funcionario");

