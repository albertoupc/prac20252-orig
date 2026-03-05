DROP TABLE IF EXISTS planets;
CREATE TABLE planets (
    name VARCHAR(100),
    description TEXT,
    image VARCHAR(250),
    distance VARCHAR(50),
    mass VARCHAR(50),
    gravity VARCHAR(50),
    diameter VARCHAR(50)
);

COPY planets(name, description, image, distance, mass, gravity, diameter)
FROM '/docker-entrypoint-initdb.d/planets-data.csv'
DELIMITER ';'
CSV HEADER;