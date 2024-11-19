
INSERT INTO Video (VideoCode, videoLength) VALUES
(1, 120),
(2, 90),
(3, 150),
(4, 180),
(5, 110);


INSERT INTO Model (ModelNo, width, height, weight, depth, screenSize) VALUES
('M1', 60.00, 35.00, 50.00, 5.00, 55.00),
('M2', 70.00, 40.00, 60.00, 6.00, 65.00),
('M3', 75.00, 42.00, 65.00, 7.00, 70.00),
('M4', 65.00, 38.00, 55.00, 5.50, 60.00),
('M5', 80.00, 45.00, 70.00, 8.00, 75.00);


INSERT INTO Site (siteCode, type, address, phone) VALUES
(1, 'bar', '123 Marvel Ave, NYC', '555-1234'),
(2, 'restaurant', '456 Jedi Way, Coruscant', '555-5678'),
(3, 'bar', '789 Gotham St, Gotham', '555-8765'),
(4, 'restaurant', '101 Stark Tower, NYC', '555-4321'),
(5, 'bar', '202 Daily Planet, Metropolis', '555-2468');


INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES
('D1', 'Smart', 'M1'),
('D2', 'Random', 'M2'),
('D3', 'Virtue', 'M3'),
('D4', 'Smart', 'M4'),
('D5', 'Random', 'M5');


INSERT INTO Client (clientId, name, phone, address) VALUES
(1, 'Bruce Wayne', '555-0001', '1 Wayne Manor, Gotham'),
(2, 'Peter Parker', '555-0002', '20 Ingram St, NYC'),
(3, 'Tony Stark', '555-0003', '10880 Malibu Point, CA'),
(4, 'Clark Kent', '555-0004', '344 Clinton St, Metropolis'),
(5, 'Natasha Romanoff', '555-0005', '53 Red Room, Moscow');


INSERT INTO TechnicalSupport (empId, name, gender) VALUES
(1, 'Sam Wilson', 'M'),
(2, 'Wanda Maximoff', 'F'),
(3, 'Bucky Barnes', 'M'),
(4, 'Carol Danvers', 'F'),
(5, 'Stephen Strange', 'M');


INSERT INTO Administrator (empId, name, gender) VALUES
(1, 'Nick Fury', 'M'),
(2, 'Alfred Pennyworth', 'M'),
(3, 'Pepper Potts', 'F'),
(4, 'Hermione Granger', 'F'),
(5, 'Phil Coulson', 'M');


INSERT INTO Salesman (empId, name, gender) VALUES
(1, 'Barry Allen', 'M'),
(2, 'Clark Kent', 'M'),
(3, 'Peter Parker', 'M'),
(4, 'Diana Prince', 'F'),
(5, 'Steve Rogers', 'M');


INSERT INTO AirtimePackage (packageId, class, startDate, lastDate, frequency, videoCode) VALUES
(1, 'economy', '2024-01-01', '2024-12-31', 30, 1),
(2, 'whole day', '2024-01-01', '2024-06-30', 15, 2),
(3, 'golden hours', '2024-01-01', '2024-03-31', 10, 3),
(4, 'economy', '2024-01-01', '2024-11-30', 25, 4),
(5, 'whole day', '2024-01-01', '2024-05-31', 20, 5);


INSERT INTO AdmWorkHours (empId, day, hours) VALUES
(1, '2024-09-01', 8.00),
(2, '2024-09-02', 7.50),
(3, '2024-09-03', 6.75),
(4, '2024-09-04', 8.50),
(5, '2024-09-05', 7.00);


INSERT INTO Broadcasts (videoCode, siteCode) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


INSERT INTO Administers (empId, siteCode) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);


INSERT INTO Specializes (empId, modelNo) VALUES
(1, 'M1'),
(2, 'M2'),
(3, 'M3'),
(4, 'M4'),
(5, 'M5');


INSERT INTO Purchases (clientId, empId, packageId, commissionRate) VALUES
(1, 1, 1, 5.00),
(2, 2, 2, 4.50),
(3, 3, 3, 6.00),
(4, 4, 4, 5.50),
(5, 5, 5, 4.75);


INSERT INTO Locates (serialNo, siteCode) VALUES
('D1', 1),
('D2', 2),
('D3', 3),
('D4', 4),
('D5', 5);
