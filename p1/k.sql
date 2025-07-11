-- Write an UPDATE statement on Broker that fails for violating (d).
-- Try to update an Owns row so that pid is a broker
UPDATE Owns SET pid = 2002002000 WHERE aid = 100 AND pid = 1001001000;
