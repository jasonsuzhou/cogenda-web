----------------- drop SQLite Schema ----------------
DROP TABLE IF EXISTS users;

----------------- setup SQLite Schema --------------- 
CREATE TABLE [users] (
    [id] INTEGER  NOT NULL PRIMARY KEY,
    [username] VARCHAR(200)  NOT NULL,
    [password] VARCHAR(200)  NOT NULL,
    [email] VARCHAR(200)  NOT NULL,
    active] BOOLEAN  NULL
);

