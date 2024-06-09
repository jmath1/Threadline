CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE Hood (
    hood_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE Block (
    block_id SERIAL PRIMARY KEY,
    hood_id INT,
    description TEXT,
    name VARCHAR(100) UNIQUE,
    coords GEOGRAPHY(POINT, 4326),
    radius DECIMAL(10,6),
    FOREIGN KEY (hood_id) REFERENCES Hood(hood_id)
);

CREATE TABLE Profile (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(200),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    description TEXT,
    photo_url VARCHAR(255),
    block_id INT,
    FOREIGN KEY (block_id) REFERENCES Block(block_id),
    coords GEOGRAPHY(POINT, 4326),
    location_confirmed BOOLEAN
);

CREATE TABLE ProfileBlockApproval (
    block_id INT,
    user_id INT,
    approver_id INT,
    FOREIGN KEY (block_id) REFERENCES Block(block_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    FOREIGN KEY (approver_id) REFERENCES Profile(user_id),
    PRIMARY KEY (block_id, user_id, approver_id)
);

CREATE TABLE UserFollowBlock (
    block_id INT,
    user_id INT,
    FOREIGN KEY (block_id) REFERENCES Block(block_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    PRIMARY KEY (block_id, user_id)
);

CREATE TABLE UserFollowHood (
    hood_id INT,
    user_id INT,
    FOREIGN KEY (hood_id) REFERENCES Hood(hood_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    PRIMARY KEY (hood_id, user_id)
);

CREATE TABLE Friendship (
    follower_id INT,
    followee_id INT,
    confirmed BOOLEAN,
    request BOOLEAN DEFAULT FALSE, 
    FOREIGN KEY (follower_id) REFERENCES Profile(user_id),
    FOREIGN KEY (followee_id) REFERENCES Profile(user_id),
    PRIMARY KEY (follower_id, followee_id)
);

CREATE TABLE Thread (
    thread_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    block_id INT,
    hood_id INT,
    author_user_id INT,
    user_id INT,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (author_user_id) REFERENCES Profile(user_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    FOREIGN KEY (hood_id) REFERENCES Hood(hood_id),
    FOREIGN KEY (block_id) REFERENCES Block(block_id)
);

CREATE TABLE Message (
    message_id SERIAL PRIMARY KEY,
    thread_id INT,
    user_id INT,
    coords GEOGRAPHY(POINT, 4326),
    body TEXT,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id)
);

CREATE TABLE UserAccess (
    user_id INT,
    thread_id INT NULL,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id)
);

CREATE TABLE Notifications (
    notification_id SERIAL PRIMARY KEY,
    to_user INT,
    user_id INT,
    notification_type VARCHAR(50),
    thread_id INT,
    message_id INT,
    datetime TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (to_user) REFERENCES Profile(user_id),
    FOREIGN KEY (user_id) REFERENCES Profile(user_id),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id),
    FOREIGN KEY (message_id) REFERENCES Message(message_id)
);

