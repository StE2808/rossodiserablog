CREATE TABLE IF NOT EXISTS comments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post TEXT NOT NULL,
  parent_id INTEGER,
  author TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'visible',
  ip_hash TEXT
);
CREATE INDEX IF NOT EXISTS idx_comments_post ON comments(post, status, created_at);
CREATE INDEX IF NOT EXISTS idx_comments_ip ON comments(ip_hash, created_at);

CREATE TABLE IF NOT EXISTS reactions(
  post TEXT NOT NULL,
  emoji TEXT NOT NULL,
  voter_token TEXT NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_reactions_uniq ON reactions(post, emoji, voter_token);
