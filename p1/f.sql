-- Write an INSERT statement on Account that fails because the
-- account's brokerpid doesn't refer to an existing broker.
INSERT INTO Account VALUES (999, 1234567890);