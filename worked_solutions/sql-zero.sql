-- Use a new practice database/session.
CREATE TEMP TABLE practice_users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TEMP TABLE practice_transactions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, amount_centavos INTEGER NOT NULL);
INSERT INTO practice_users VALUES (1, 'Aya'), (2, 'Mika'), (3, 'Lea');
INSERT INTO practice_transactions VALUES (1, 1, 1000), (2, 1, 2500), (3, 3, 500);

SELECT u.id AS user_id, u.name,
       COALESCE(SUM(t.amount_centavos), 0) AS total_centavos
FROM practice_users AS u
LEFT JOIN practice_transactions AS t ON t.user_id = u.id
GROUP BY u.id, u.name
ORDER BY u.id;
