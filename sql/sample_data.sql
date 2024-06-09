INSERT INTO Hood (name) VALUES
('Upper East Side'),
('Upper West Side');


-- Insert blocks for Upper East Side
WITH upper_east_side AS (
    SELECT hood_id
    FROM Hood
    WHERE name = 'Upper East Side'
)
INSERT INTO Block (hood_id, description, name, coords, radius)
SELECT 
    hood_id,
    'Lenox Hill Block' AS description,
    'Lenox Hill' AS name,
    ST_SetSRID(ST_MakePoint(-73.9626, 40.7681), 4326) AS coords,
    600.0
FROM upper_east_side
UNION ALL
SELECT 
    hood_id,
    'Yorkville Block' AS description,
    'Yorkville' AS name,
    ST_SetSRID(ST_MakePoint(-73.9493, 40.7769), 4326) AS coords,
    600.0
FROM upper_east_side
UNION ALL
SELECT 
    hood_id,
    'Central Park East Block' AS description,
    'Central Park East' AS name,
    ST_SetSRID(ST_MakePoint(-73.9654, 40.7812), 4326) AS coords,
    600.0
FROM upper_east_side;

-- Insert blocks for Upper West Side
WITH upper_west_side AS (
    SELECT hood_id
    FROM Hood
    WHERE name = 'Upper West Side'
)
INSERT INTO Block (hood_id, description, name, coords, radius)
SELECT 
    hood_id,
    'Lincoln Square Block' AS description,
    'Lincoln Square' AS name,
    ST_SetSRID(ST_MakePoint(-73.9842, 40.7738), 4326) AS coords,
    600.0
FROM upper_west_side
UNION ALL
SELECT 
    hood_id,
    'Manhattan Valley Block' AS description,
    'Manhattan Valley' AS name,
    ST_SetSRID(ST_MakePoint(-73.9681, 40.7990), 4326) AS coords,
    600.0
FROM upper_west_side
UNION ALL
SELECT 
    hood_id,
    'Bloomingdale Block' AS description,
    'Bloomingdale' AS name,
    ST_SetSRID(ST_MakePoint(-73.9712, 40.7985), 4326) AS coords,
    600.0
FROM upper_west_side;



-- Insert users into the Profile table
INSERT INTO Profile (username, first_name, last_name, address, email, password, description, photo_url, block_id, coords, location_confirmed)
VALUES
('user1', 'John', 'Doe', '123 Lenox Hill St', 'johndoe@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Lenox Hill', 'http://example.com/photo1.jpg', 1, ST_SetSRID(ST_MakePoint(-73.9626, 40.7681), 4326), TRUE),
('user2', 'Jane', 'Doe', '456 Yorkville Ave', 'janedoe@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Yorkville', 'http://example.com/photo2.jpg', 2, ST_SetSRID(ST_MakePoint(-73.9493, 40.7769), 4326), TRUE),
('user3', 'Alice', 'Smith', '789 Central Park East', 'alicesmith@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Central Park East', 'http://example.com/photo3.jpg', 3, ST_SetSRID(ST_MakePoint(-73.9654, 40.7812), 4326), TRUE),
('user4', 'Bob', 'Brown', '123 Lincoln Square', 'bobbrown@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Lincoln Square', 'http://example.com/photo4.jpg', 4, ST_SetSRID(ST_MakePoint(-73.9842, 40.7738), 4326), TRUE),
('user5', 'Charlie', 'Davis', '456 Manhattan Valley', 'charliedavis@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Manhattan Valley', 'http://example.com/photo5.jpg', 5, ST_SetSRID(ST_MakePoint(-73.9681, 40.7990), 4326), TRUE),
('user6', 'David', 'Evans', '789 Bloomingdale', 'davidevans@example.com', 'pbkdf2_sha256$720000$3BpPXCw3Uki35tWh5ELcr1$hJ9pMEfLAzbxWzm89N9TOlc+tVviVFkspFjimqVjAoA=', 'Resident of Bloomingdale', 'http://example.com/photo6.jpg', 6, ST_SetSRID(ST_MakePoint(-73.9712, 40.7985), 4326), TRUE);
