CREATE TABLE urls
(
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    host        TEXT,
    port        TEXT,
    description TEXT
);
CREATE TABLE apis
(
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url_id      INT, -- FK(1toN) -> urls
    "key"       TEXT UNIQUE,
    path        TEXT,
    method      TEXT,
    description TEXT,
    FOREIGN KEY (url_id) REFERENCES urls (id)
);
CREATE TABLE schemas
(
    api_id INT PRIMARY KEY, -- FK(1to1) -> apis
    type   TEXT,
    FOREIGN KEY (api_id) REFERENCES apis (id) ON DELETE CASCADE
);
CREATE TABLE fields
(
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    schema_id   INT, -- FK(1toN) -> schemas
    name        TEXT,
    type        TEXT,
    description TEXT,
    FOREIGN KEY (schema_id) REFERENCES schemas (api_id)
);
-- add test data
INSERT INTO urls (host, port, description)
VALUES ('http://localhost', '8000', 'Sample host');
INSERT INTO apis (url_id, "key", path, method, description)
VALUES (1, 'unique_key', '/users', 'POST', 'Get user data using user name and password');
INSERT INTO schemas (api_id, type)
VALUES (1, 'object');
INSERT INTO fields (schema_id, name, type, description)
VALUES (1, 'name', 'string', 'user name to identify'),
       (1, 'password', 'string', 'user password to verify');