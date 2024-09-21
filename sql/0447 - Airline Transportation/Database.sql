DROP TABLE IF EXISTS Pass_in_trip;
DROP TABLE IF EXISTS Trip;
DROP TABLE IF EXISTS Airline_company;
DROP TABLE IF EXISTS Passenger;

CREATE TABLE Airline_company (
    ID_comp INT PRIMARY KEY,
    company_name VARCHAR(255)
);

CREATE TABLE Trip (
    trip_no INT PRIMARY KEY,
    ID_comp INT,
    plane_type VARCHAR(255),
    town_from VARCHAR(255),
    town_to VARCHAR(255),
    time_out DATETIME,
    time_in DATETIME,
    FOREIGN KEY (ID_comp) REFERENCES Airline_company(ID_comp)
);

CREATE TABLE Passenger (
    ID_psg INT PRIMARY KEY,
    passenger_name VARCHAR(255)
);

CREATE TABLE Pass_in_trip (
    trip_no INT,
    trip_date DATETIME,
    ID_psg INT,
    seat_number CHAR(3),
    PRIMARY KEY (trip_no, trip_date, ID_psg),
    FOREIGN KEY (trip_no) REFERENCES Trip(trip_no),
    FOREIGN KEY (ID_psg) REFERENCES Passenger(ID_psg)
);


-- Inserts for Airline_Company
INSERT INTO Airline_company (ID_comp, company_name) VALUES
(1, 'Delta Airlines'),
(2, 'American Airlines'),
(3, 'United Airlines'),
(4, 'Southwest Airlines'),
(5, 'JetBlue Airways');


INSERT INTO Trip (trip_no, ID_comp, plane_type, town_from, town_to, time_out, time_in) VALUES
(1, 1, 'Boeing 737', 'New York', 'Los Angeles', '2024-02-23 08:00:00', '2024-02-23 12:00:00'),
(2, 2, 'Airbus A320', 'Los Angeles', 'Chicago', '2024-02-23 19:00:00', '2024-02-24 00:30:00'),
(3, 3, 'Boeing 777', 'Chicago', 'Dallas', '2024-02-23 15:30:00', '2024-02-23 18:45:00'),
(4, 4, 'Airbus A330', 'Dallas', 'Miami', '2024-02-23 10:45:00', '2024-02-23 14:35:00'),
(5, 5, 'Boeing 747', 'Miami', 'New York', '2024-02-23 13:30:00', '2024-02-23 17:00:00'),
(6, 1, 'Boeing 737', 'New York', 'Los Angeles', '2024-02-24 09:15:00', '2024-02-24 13:30:00'),
(7, 2, 'Airbus A320', 'Los Angeles', 'Chicago', '2024-02-24 12:30:00', '2024-02-24 16:00:00'),
(8, 3, 'Boeing 777', 'Chicago', 'Dallas', '2024-02-24 23:00:00', '2024-02-25 04:15:00'),
(9, 4, 'Airbus A330', 'Dallas', 'Miami', '2024-02-24 11:45:00', '2024-02-24 15:00:00'),
(10, 5, 'Boeing 747', 'Miami', 'New York', '2024-02-24 14:00:00', '2024-02-24 17:30:00'),
(11, 1, 'Boeing 737', 'New York', 'London', '2024-02-25 08:00:00', '2024-02-25 20:00:00'),
(12, 2, 'Airbus A320', 'Los Angeles', 'Tokyo', '2024-02-26 11:00:00', '2024-02-27 09:30:00'),
(13, 3, 'Boeing 777', 'Chicago', 'Paris', '2024-02-27 15:30:00', '2024-02-28 10:45:00'),
(14, 4, 'Airbus A330', 'Dallas', 'Sydney', '2024-02-28 10:45:00', '2024-02-29 00:15:00'),
(15, 5, 'Boeing 747', 'Miami', 'Dubai', '2024-02-29 13:30:00', '2024-03-01 23:00:00'),
(16, 3, 'Boeing 737', 'Dallas', 'Los Angeles', '2024-03-02 08:30:00', '2024-03-02 11:45:00'),
(17, 2, 'Airbus A320', 'Chicago', 'Miami', '2024-03-03 11:15:00', '2024-03-03 15:30:00'),
(18, 4, 'Boeing 777', 'New York', 'Paris', '2024-03-04 13:00:00', '2024-03-04 23:00:00'),
(19, 5, 'Boeing 747', 'Miami', 'Los Angeles', '2024-03-05 09:45:00', '2024-03-05 13:00:00'),
(20, 1, 'Airbus A330', 'Los Angeles', 'New York', '2024-03-06 15:30:00', '2024-03-06 18:45:00');


-- Insert 10 passengers
INSERT INTO Passenger (ID_psg, passenger_name) VALUES
(1, 'John Smith'),
(2, 'Mary Johnson'),
(3, 'James Williams'),
(4, 'Patricia Jones'),
(5, 'Michael Brown'),
(6, 'Jennifer Davis'),
(7, 'Richard Wilson'),
(8, 'Linda Martinez'),
(9, 'David Anderson'),
(10, 'Barbara Taylor');

INSERT INTO Pass_in_trip (trip_no, trip_date, ID_psg, seat_number) VALUES
(1, '2024-02-23 00:00:00', 1, '01A'),
(1, '2024-02-23 00:00:00', 2, '01B'),
(2, '2024-02-23 00:00:00', 3, '02C'),
(2, '2024-02-23 00:00:00', 6, '02D'),
(3, '2024-02-23 00:00:00', 5, '03A'),
(3, '2024-02-23 00:00:00', 6, '13B'),
(4, '2024-02-23 00:00:00', 7, '24C'),
(4, '2024-02-23 00:00:00', 8, '34D'),
(5, '2024-02-23 00:00:00', 9, '15A'),
(5, '2024-02-23 00:00:00', 10, '05B'),
(6, '2024-02-24 00:00:00', 1, '11A'),
(6, '2024-02-24 00:00:00', 2, '13B'),
(7, '2024-02-24 00:00:00', 2, '32C'),
(7, '2024-02-24 00:00:00', 7, '42D'),
(8, '2024-02-24 00:00:00', 1, '23A'),
(8, '2024-02-24 00:00:00', 2, '53B'),
(9, '2024-02-24 00:00:00', 1, '24C'),
(9, '2024-02-24 00:00:00', 7, '14D'),
(10, '2024-02-24 00:00:00', 1, '25A'),
(10, '2024-02-24 00:00:00', 2, '05B'),
(11, '2024-02-25 00:00:00', 1, '73B'),
(11, '2024-02-25 00:00:00', 2, '13C'),
(12, '2024-02-26 00:00:00', 2, '84C'),
(13, '2024-02-27 00:00:00', 1, '34D'),
(14, '2024-02-28 00:00:00', 6, '45A'),
(15, '2024-02-29 00:00:00', 4, '95B'),
(15, '2024-02-29 00:00:00', 6, '08A'),
(16, '2024-03-02 00:00:00', 3, '02B'),
(17, '2024-03-03 00:00:00', 1, '35D'),
(18, '2024-03-04 00:00:00', 2, '28A'),
(18, '2024-03-04 00:00:00', 1, '13A'),
(19, '2024-03-05 00:00:00', 10, '15C'),
(20, '2024-03-06 00:00:00', 6, '17B');








