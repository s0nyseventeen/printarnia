INSERT INTO user (username, email, password) VALUES
	('test', 'test@email.ua', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
	('admin', 'admin@email.ua', 'pbkdf2:sha256:600000$X5N5KGOxzPfPJ2NS$05351f0c79ba5ef71cce241341735b4120ea5a9dcfb1632b954b8e7369b89d2d');

INSERT INTO work (title, created, description, image)
VALUES ('Test title', '2023-06-05 00:00:00', 'New design', 'someimage.gpj');
