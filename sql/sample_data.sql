-- Insert sample data into the Hood table for Upper East Side
INSERT INTO Hood (hood_id, name)
VALUES (1, 'Upper East Side');


-- Insert sample data into the Hood table for Lower East Side
INSERT INTO Hood (hood_id, name)
VALUES (2, 'Lower East Side');


-- Insert sample data into the Block table for Upper East Side
INSERT INTO Block (block_id, hood_id, description, name, coords, radius)
VALUES
    (0, 1, 'My Block', 'For testing', 'POINT(-73.9562956013475 40.76859165)', 100),
    (1, 1, 'Upper East Side Block 1', 'UES Block 1', 'POINT(-73.9550 40.7750)', 100),
    (2, 1, 'Upper East Side Block 2', 'UES Block 2', 'POINT(-73.9575 40.7725)', 100),
    (3, 1, 'Upper East Side Block 3', 'UES Block 3', 'POINT(-73.9525 40.7775)', 100);


-- Insert sample data into the Block table for Lower East Side
INSERT INTO Block (block_id, hood_id, description, name, coords, radius)
VALUES
   (4, 2, 'Lower East Side Block 1', 'LES Block 1', 'POINT(-73.9875 40.7150)', 100),
   (5, 2, 'Lower East Side Block 2', 'LES Block 2', 'POINT(-73.9825 40.7175)', 100),
   (6, 2, 'Lower East Side Block 3', 'LES Block 3', 'POINT(-73.9850 40.7125)', 100);




-- Insert sample data into the Profile table for Upper East Side Block 1
INSERT INTO Profile (user_id, username, block_id, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (10, 'user10', 0, 'Sophia', 'Martinez', 'sophia.martinez@example.com', 'password10', 'Resident of Upper East Side Block 1', 'https://example.com/photo10.jpg', 'POINT(-73.9555 40.7755)', true),
   (11, 'user11', 0, 'Liam', 'Johnson', 'liam.johnson@example.com', 'password11', 'Resident of Upper East Side Block 1', 'https://example.com/photo11.jpg', 'POINT(-73.9553 40.7753)', true);


-- Insert sample data into the Profile table for Upper East Side Block 2
INSERT INTO Profile (user_id, username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (12, 'user12', 'Emma', 'Garcia', 'emma.garcia@example.com', 'password12', 'Resident of Upper East Side Block 2', 'https://example.com/photo12.jpg', 'POINT(-73.9570 40.7727)', true),
   (13, 'user13', 'Noah', 'Brown', 'noah.brown@example.com', 'password13', 'Resident of Upper East Side Block 2', 'https://example.com/photo13.jpg', 'POINT(-73.9568 40.7725)', true);


-- Insert sample data into the Profile table for Upper East Side Block 3
INSERT INTO Profile (user_id, username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (14, 'user14', 'Olivia', 'Martinez', 'olivia.martinez@example.com', 'password14', 'Resident of Upper East Side Block 3', 'https://example.com/photo14.jpg', 'POINT(-73.9530 40.7770)', true),
   (15, 'user15', 'William', 'Rodriguez', 'william.rodriguez@example.com', 'password15', 'Resident of Upper East Side Block 3', 'https://example.com/photo15.jpg', 'POINT(-73.9532 40.7768)', true);


-- Insert sample data into the Profile table for Lower East Side Block 1
INSERT INTO Profile (user_id, username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (16, 'user16', 'Ava', 'Hernandez', 'ava.hernandez@example.com', 'password16', 'Resident of Lower East Side Block 1', 'https://example.com/photo16.jpg', 'POINT(-73.9876 40.7151)', true),
   (17, 'user17', 'James', 'Lopez', 'james.lopez@example.com', 'password17', 'Resident of Lower East Side Block 1', 'https://example.com/photo17.jpg', 'POINT(-73.9874 40.7149)', true);


-- Insert sample data into the Profile table for Lower East Side Block 2
INSERT INTO Profile (user_id, username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (18, 'user18', 'Mia', 'Gonzalez', 'mia.gonzalez@example.com', 'password18', 'Resident of Lower East Side Block 2', 'https://example.com/photo18.jpg', 'POINT(-73.9826 40.7176)', true),
   (19, 'user19', 'Benjamin', 'Perez', 'benjamin.perez@example.com', 'password19', 'Resident of Lower East Side Block 2', 'https://example.com/photo19.jpg', 'POINT(-73.9824 40.7174)', true);


-- Insert sample data into the Profile table for Lower East Side Block 3
INSERT INTO Profile (user_id, username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
VALUES
   (20, 'user20', 'Charlotte', 'Torres', 'charlotte.torres@example.com', 'password20', 'Resident of Lower East Side Block 3', 'https://example.com/photo20.jpg', 'POINT(-73.9851 40.7126)', true),
   (21, 'user21', 'Lucas', 'Ramirez', 'lucas.ramirez@example.com', 'password21', 'Resident of Lower East Side Block 3', 'https://example.com/photo21.jpg', 'POINT(-73.9849 40.7124)', true);