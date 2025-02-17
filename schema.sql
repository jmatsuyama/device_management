DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS lockers;

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
