-- Write an INSERT statement that fails for violating (c).
-- Should fail because seq=2 already exists for aid=100
INSERT INTO Trade VALUES (100, 2, 'buy', '2024-01-01 10:00:00', 'AAPL', 1.00, 100.00);
