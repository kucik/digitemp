CREATE TABLE sessions (
  id           varchar(256) NOT NULL,
  name         varchar(24) NOT NULL,
  time         timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE sessions
  ADD PRIMARY KEY (id);
