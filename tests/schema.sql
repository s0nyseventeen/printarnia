DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS work;

CREATE TABLE users (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	username VARCHAR(256) UNIQUE NOT NULL,
	email VARCHAR(256) UNIQUE NOT NULL,
	password VARCHAR(256) NOT NULL
);

CREATE TABLE work (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	title VARCHAR(256) UNIQUE NOT NULL,
	created VARCHAR(256) NOT NULL,
	description VARCHAR(1000),
	image VARCHAR(256)
);

INSERT INTO work (title, created, description, image) VALUES
	('Test title', '2023-06-05 00:00:00', 'New design', 'someimage.jpg');
