CREATE DATABASE kedozi;

--define a new sequence generator
CREATE SEQUENCE users_seq;

CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY DEFAULT NEXTVAL('users_seq'),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL UNIQUE
);