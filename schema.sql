DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS lockers;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    organization TEXT CHECK(organization IN ('JEIS', 'JR')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    pc_id TEXT NOT NULL,
    status TEXT DEFAULT '準備中',
    release_date DATE,
    is_replacement BOOLEAN DEFAULT 0,
    locker_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (locker_id) REFERENCES lockers (id)
);

CREATE TABLE lockers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT DEFAULT '施錠',
    password TEXT,
    password_expiry TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 初期管理者ユーザーの作成（パスワード: admin123）
INSERT INTO users (name, user_id, password, organization) 
VALUES ('管理者', 'admin', 'pbkdf2:sha256:260000$GhGdVGmP0Gz3cqWx$f6240d7f5c6c13eb3465bb1a257b9d47c095ea111f2644d896952a0e1ce0bb51', 'JEIS');
