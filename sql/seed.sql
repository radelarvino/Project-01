INSERT OR IGNORE INTO users (id, username, password, role) VALUES 
(1, 'admin', 'admin123', 'admin'),
(2, 'test-user', 'user123', 'user');

INSERT OR IGNORE INTO menus (id, name, price, stock) VALUES 
(1, 'Rendang', 13000, 10),
(2, 'Ayam Pop', 12000, 15),
(3, 'Gulai Ayam', 14000, 8),
(4, 'Ikan Bakar', 25000, 5),
(5, 'Sate Padang', 35000, 12),
(6, 'Telur Balado', 7000, 20),
(7, 'Nasi Putih', 3000, 50),
(8, 'Teh Manis', 5000, 30),
(9, 'Es Jeruk', 5000, 15);
