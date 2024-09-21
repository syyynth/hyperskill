CREATE TABLE Classes (
    class VARCHAR(50) NOT NULL,
    type VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    numGuns INT NOT NULL,
    bore FLOAT NOT NULL,
    displacement INT NOT NULL,
    PRIMARY KEY (class)
);

CREATE TABLE Ships (
    name VARCHAR(50) NOT NULL,
    class VARCHAR(50) NOT NULL,
    launched INT NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (class) REFERENCES Classes(class) ON DELETE CASCADE
);

CREATE TABLE Battles (
    name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE Outcomes (
    ship VARCHAR(50) NOT NULL,
    battle VARCHAR(50) NOT NULL,
    result VARCHAR(20) NOT NULL,
    PRIMARY KEY (ship, battle),
    FOREIGN KEY (ship) REFERENCES Ships(name) ON DELETE CASCADE,
    FOREIGN KEY (battle) REFERENCES Battles(name) ON DELETE CASCADE
);
-- Inserting more data into the Classes table
DELETE FROM Classes;
DELETE FROM Ships;
DELETE FROM Battles;
DELETE FROM Outcomes;
INSERT INTO Classes (class, type, country, numGuns, bore, displacement)
VALUES
('Nagato', 'bb', 'Japan', 8, 16.1, 31000),
('Hood', 'bc', 'Gt.Britain', 8, 15.0, 41000),
('Bismarck II', 'bb', 'Germany', 8, 15.0, 42000),
('Hood II', 'bc', 'Gt.Britain', 8, 15.0, 35000),
('Ise', 'bb', 'Japan', 10, 16.1, 40000),
('Nelson', 'bb', 'Gt.Britain', 9, 16.0, 55000),
('Yamashiro II', 'bb', 'Japan', 8, 16.1, 60000),
('Nevada', 'bb', 'USA', 10, 14.0, 29000);

-- Inserting more data into the Ships table
INSERT INTO Ships (name, class, launched)
VALUES
('HMS Prince of Wales', 'Hood', 1941),
('Fusō', 'Nagato', 1915),
('HMS Rodney', 'Nelson', 1925),
('Yamagumo', 'Yamashiro II', 1940),
('HMS Warspite', 'Nelson', 1913),
('HMS Queen Elizabeth', 'Nevada', 1913),
('Yamato II', 'Ise', 1917),
('HMS Ark Royal', 'Nelson', 1937),
('Nagato', 'Nagato', 1920),
('HMS Hood', 'Hood', 1918),
('Bismarck', 'Bismarck II', 1939),
('HMS Anson', 'Hood II', 1942),
('Ise', 'Ise', 1917),
('HMS Nelson', 'Nelson', 1925),
('Yamashiro', 'Yamashiro II', 1915),
('USS Nevada', 'Nevada', 1914);

-- Inserting more data into the Battles table
INSERT INTO Battles (name, date)
VALUES
('Battle of Leyte Gulf', '1944-10-23'),
('Battle of Midway', '1942-06-04'),
('Pearl Harbor', '1941-12-07'),
('Battle of Okinawa', '1945-04-01'),
('Battle of the Atlantic', '1940-09-03'),
('Battle of the Denmark Strait', '1941-05-24'),
('Battle of Surigao Strait', '1944-10-25'),
('Battle of the Coral Sea', '1942-05-07');

-- Inserting more data into the Outcomes table
INSERT INTO Outcomes (ship, battle, result)
VALUES
('HMS Prince of Wales', 'Battle of Midway', 'damaged'),
('HMS Prince of Wales', 'Battle of the Denmark Strait', 'sunk'),
('Yamashiro', 'Battle of Surigao Strait', 'sunk'),
('Fusō', 'Battle of Okinawa', 'damaged'),
('HMS Rodney', 'Battle of the Denmark Strait', 'OK'),
('Yamagumo', 'Battle of the Coral Sea', 'OK'),
('Nagato', 'Battle of Okinawa', 'OK'),
('Nagato', 'Battle of the Denmark Strait', 'damaged'),
('HMS Warspite', 'Battle of Midway', 'OK'),
('HMS Queen Elizabeth', 'Battle of the Denmark Strait', 'OK'),
('Yamato II', 'Battle of Surigao Strait', 'sunk'),
('HMS Ark Royal', 'Battle of the Coral Sea', 'damaged'),
('HMS Hood', 'Battle of the Atlantic', 'sunk'),
('Bismarck', 'Battle of the Denmark Strait', 'sunk'),
('Bismarck', 'Battle of the Atlantic', 'damaged'),
('HMS Anson', 'Battle of Okinawa', 'OK'),
('Ise', 'Battle of Leyte Gulf', 'sunk'),
('HMS Nelson', 'Battle of the Atlantic', 'OK'),
('Yamashiro', 'Battle of Leyte Gulf', 'sunk'),
('USS Nevada', 'Battle of the Atlantic', 'OK'),
('HMS Nelson', 'Pearl Harbor', 'damaged'),
('HMS Nelson', 'Battle of the Denmark Strait', 'OK'),
('USS Nevada', 'Battle of the Coral Sea', 'damaged'),
('USS Nevada', 'Pearl Harbor', 'damaged');
