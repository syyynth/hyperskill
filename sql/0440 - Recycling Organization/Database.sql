-- Table for recording income at collection points
-- Drop tables if they exist
DROP TABLE IF EXISTS Income_one_day;
DROP TABLE IF EXISTS Outcome_one_day;
DROP TABLE IF EXISTS Income;
DROP TABLE IF EXISTS Outcome;

CREATE TABLE Income_one_day (
    pick_up_point INT,
    date DATE,
    money_in DECIMAL(10, 2),
    PRIMARY KEY (pick_up_point, date)
);

-- Table for recording money issuance to recyclable materials distributors
CREATE TABLE Outcome_one_day (
    pick_up_point INT,
    date DATE,
    money_out DECIMAL(10, 2),
    PRIMARY KEY (pick_up_point, date)
);

-- Table for recording income at collection points with a code as primary key
CREATE TABLE Income (
    code INT PRIMARY KEY,
    pick_up_point INT,
    date DATE,
    money_in DECIMAL(10, 2)
);

-- Table for recording money issuance to recyclable materials distributors with a code as primary key
CREATE TABLE Outcome (
    code INT PRIMARY KEY,
    pick_up_point INT,
    date DATE,
    money_out DECIMAL(10, 2)
);
-- Clear existing data from tables
DELETE FROM Income_one_day;
DELETE FROM Outcome_one_day;
DELETE FROM Income;
DELETE FROM Outcome;

INSERT INTO Income_one_day (pick_up_point, date, money_in)
VALUES
    (1, '2021-03-22', 15000.0000),
    (1, '2021-03-23', 15000.0000),
    (1, '2021-03-24', 3400.0000),
    (1, '2021-04-13', 5000.0000),
    (1, '2021-05-11', 4500.0000),
    (2, '2021-03-22', 10000.0000),
    (2, '2021-03-24', 1500.0000),
    (3, '2021-09-13', 11500.0000),
    (3, '2021-10-02', 18000.0000);
    
INSERT INTO Income (code, pick_up_point, date, money_in)
VALUES
    (1, 1, '2021-03-22', 15000.0000),
    (10, 1, '2021-04-13', 5000.0000),
    (11, 1, '2021-03-24', 3400.0000),
    (12, 3, '2021-09-13', 1350.0000),
    (13, 3, '2021-09-13', 1750.0000),
    (2, 1, '2021-03-23', 15000.0000),
    (3, 1, '2021-03-24', 3600.0000),
    (4, 2, '2021-03-22', 10000.0000),
    (5, 2, '2021-03-24', 1500.0000),
    (6, 1, '2021-04-13', 5000.0000),
    (7, 1, '2021-05-11', 4500.0000),
    (8, 1, '2021-03-22', 15000.0000),
    (9, 2, '2021-03-24', 1500.0000);

INSERT INTO Outcome_one_day (pick_up_point, date, money_out)
VALUES
    (1, '2021-03-14', 15348.0000),
    (1, '2021-03-24', 3663.0000),
    (1, '2021-03-26', 1221.0000),
    (1, '2021-03-28', 2075.0000),
    (1, '2021-03-29', 2004.0000),
    (1, '2021-04-11', 3195.0000),
    (1, '2021-04-13', 4490.0000),
    (1, '2021-04-27', 3110.0000),
    (1, '2021-05-11', 2530.0000),
    (2, '2021-03-22', 1440.0000),
    (2, '2021-03-29', 7848.0000),
    (2, '2021-04-02', 2040.0000),
    (3, '2021-09-13', 1500.0000),
    (3, '2021-09-14', 2300.0000),
    (3, '2022-09-16', 2150.0000);
    
INSERT INTO Outcome (code, pick_up_point, date, money_out)
VALUES
    (1, 1, '2021-03-14', 15348.0000),
    (10, 2, '2021-03-22', 1440.0000),
    (11, 2, '2021-03-29', 7848.0000),
    (12, 2, '2021-04-02', 2040.0000),
    (13, 1, '2021-03-24', 3500.0000),
    (14, 2, '2021-03-22', 1440.0000),
    (15, 1, '2021-03-29', 2006.0000),
    (16, 3, '2021-09-13', 1200.0000),
    (17, 3, '2021-09-13', 1500.0000),
    (18, 3, '2021-09-14', 1150.0000),
    (2, 1, '2021-03-24', 3663.0000),
    (3, 1, '2021-03-26', 1221.0000),
    (4, 1, '2021-03-28', 2075.0000),
    (5, 1, '2021-03-29', 2004.0000),
    (6, 1, '2021-04-11', 3195.0400),
    (7, 1, '2021-04-13', 4490.0000),
    (8, 1, '2021-04-27', 3110.0000),
    (9, 1, '2021-05-11', 2530.0000),
    (19, 1, '2022-01-11', 4670.0000);


