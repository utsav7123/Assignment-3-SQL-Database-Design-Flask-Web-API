-- Write a DELETE statement on Broker that fails because the broker
-- being deleted is managing somebody else.

DELETE FROM Broker WHERE pid = 6006006000;