CREATE TABLE schemas
(
    id TEXT PRIMARY KEY,
    type   TEXT
);
CREATE TABLE fields
(
    id          INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    schema_id   TEXT, -- FK(1toN) -> schemas
    name        TEXT,
    type        TEXT,
    description TEXT,
    FOREIGN KEY (schema_id) REFERENCES schemas (id)
);
-- add test data
INSERT INTO schemas (id, type)
VALUES ('schema_id1', 'object'),
       ('schema_id2', 'object');
INSERT INTO fields (schema_id, name, type, description)
VALUES ('schema_id1', 'name', 'string', 'user name to identify'),
       ('schema_id1', 'password', 'string', 'user password to verify'),
       ('schema_id2', 'flight_id', 'string', 'flight id'),
       ('schema_id2', 'tail_number', 'string', 'aircraft registration number'),
       ('schema_id2', 'aircraft_type', 'string', 'specific aircraft type');