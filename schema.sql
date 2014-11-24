CREATE TABLE IF NOT EXISTS users 
  (id INTEGER PRIMARY KEY,
   email TEXT,
   password TEXT,
   display_name TEXT,
   last_login TEXT,
   icon TEXT);

CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY,
  owner INTEGER,
  subject TEXT,
  summary TEXT,
  message TEXT,
  markup TEXT,
  timestamp DATE,
  link_furaffinity TEXT,
  link_weasyl TEXT,
  link_twitter TEXT,
  link_facebook TEXT,
  FOREIGN KEY(owner) REFERENCES users(id)
);
