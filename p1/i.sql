-- Write a DELETE statement that fails for violating (c).
DELETE FROM Trade WHERE aid = 100 AND seq = 1;
