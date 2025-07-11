-- Write an INSERT statement on Trade that fails for violating (e).
-- Try to sell more AAPL than currently held in account 100
INSERT INTO Trade VALUES (100, 11, 'sell', '2024-01-01 10:00:00', 'AAPL', 100.00, 100.00);
