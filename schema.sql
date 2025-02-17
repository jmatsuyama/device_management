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
VALUES ('管理者', 'admin', 'scrypt:32768:8:1$UoMRgrb4I9T3t5Hs$3aa0e91ad35828c8793e673621f7d851945b5f36df925425654c5a5a75d0c20944eaf0ae91c5c6dc3b85da93ce453eda92cd269aebb7ee0ee7f939447f7a1b1e', 'JEIS');

-- テスト用JRユーザーの作成（パスワード: jr123）
INSERT INTO users (name, user_id, password, organization)
VALUES ('JRユーザー', 'jr', 'scrypt:32768:8:1$5KxXhHJQWxDxhsS7$5c6a8f0b8b6e1d4c2a9f3b7e5d8c1a4f7b0e3d6c9a2f5b8e1d4c7a0f3b6e9d2c5a8f1b4e7d0c3a6f9b2e5d8c1a4f7b0e3d6c9a2f5b8e1d4c7a0f3b6e9d2', 'JR');
