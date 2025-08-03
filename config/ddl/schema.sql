CREATE TABLE urls
(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url TEXT,
    description TEXT
);
CREATE TABLE apis
(
    id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url_id INT,  -- FK(1toN) -> urls
    path TEXT,
    method TEXT,
    description TEXT,
    FOREIGN KEY (url_id) REFERENCES urls(id)
);
CREATE TABLE schemas (
    api_id INT PRIMARY KEY,  -- FK(1to1) -> apis
    type TEXT,
    FOREIGN KEY (api_id) REFERENCES apis(id) ON DELETE CASCADE
);
CREATE TABLE fields (
    id   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    schema_id INT,  -- FK(1toN) -> schemas
    name TEXT,
    type TEXT,
    description TEXT,
    FOREIGN KEY (schema_id) REFERENCES schemas(api_id)
);