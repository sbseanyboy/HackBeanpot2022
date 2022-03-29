
CREATE DATABASE cal;

USE cal;

CREATE TABLE capacity(
    time_date VARCHAR(8),
    time_dow INT,
    time_interval INT,
    a1 INT,
    a2 INT,
    a3 INT,
    a4 INT,
    a5 INT,
    a6 INT,
    PRIMARY KEY(time_date, time_interval)
);

SELECT * FROM capacity;

CREATE TABLE capacity_avg(
    iid INT PRIMARY KEY,
    avg_r1 INT,
    avg_r2 INT,
    avg_r3 INT,
    avg_r4 INT,
    avg_r5 INT,
    avg_r6 INT,
    num_entries INT
);

SELECT * FROM capacity_avg;