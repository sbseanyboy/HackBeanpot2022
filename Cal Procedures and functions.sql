USE cal;

DROP PROCEDURE IF EXISTS add_capacity;

DELIMITER $$

CREATE PROCEDURE add_capacity(IN a_date VARCHAR(8), IN a_dow INT,
    IN a_interval INT,
    IN a_a1 INT,
    IN a_a2 INT,
    IN a_a3 INT,
    IN a_a4 INT,
    IN a_a5 INT,
    IN a_a6 INT)
    
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Adding capacity entry failed';
INSERT INTO Capacity (time_date, time_dow, time_interval, a1, a2, a3, a4, a5, a6 ) 
VALUES (a_date, a_dow, a_interval, a_a1, a_a2, a_a3, a_a4, a_a5, a_a6);
END $$

DELIMITER ;

CALL add_capacity('12/02/22', 5, 1, 30, 47, 68, 31, 25, 23);

DROP PROCEDURE IF EXISTS update_avg;

DELIMITER $$

CREATE PROCEDURE update_avg(IN u_iid INT, IN u_avg1 INT,
IN u_avg2 INT, IN u_avg3 INT, IN u_avg4 INT, IN u_avg5 INT, IN u_avg6 INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Updating average table failed';
UPDATE capacity_avg
SET avg_r1 = u_avg1, avg_r2 = u_avg2, avg_r3 = u_avg3, avg_r4 = u_avg4, 
avg_r5 = u_avg5, avg_r6 = u_avg6, num_entries = num_entries + 1
WHERE iid = u_iid;
END $$

DELIMITER ;

DROP PROCEDURE IF EXISTS add_avg;

DELIMITER $$

CREATE PROCEDURE add_avg(IN id INT, avg_1 INT,
    avg_2 INT,
    avg_3 INT,
    avg_4 INT,
    avg_5 INT,
    avg_6 INT,
    entries INT)
    
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Adding capacity entry failed';
INSERT INTO capacity_avg (iid, avg_r1,
    avg_r2,
    avg_r3,
    avg_r4,
    avg_r5,
    avg_r6,
    num_entries) 
VALUES (id, avg_1,
    avg_2,
    avg_3,
    avg_4,
    avg_5,
    avg_6,
    entries);
END $$

DELIMITER ;


/*
DROP FUNCTION IF EXISTS read_avg

DELIMITER $$


CREATE FUNCTION read_avg(r_did INT)
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE d_avg INT;
SELECT avg_raiting INTO d_avg
FROM capacity_avg 
WHERE did = r_did;
RETURN d_avg;
END $$

DELIMITER ;

SELECT read_avg(1);

DROP FUNCTION IF EXISTS read_entries

DELIMITER $$

CREATE FUNCTION read_entries(r_did INT)
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE d_entries INT;
SELECT num_entries INTO d_entries
FROM capacity_avg 
WHERE did = r_did;
RETURN d_entries;
END $$

DELIMITER ;

SELECT read_entries(1);
*/