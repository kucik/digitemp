CREATE TABLE users (
  name         varchar(24) NOT NULL,
  password     varchar(128)
);


ALTER TABLE users
  ADD PRIMARY KEY (name);
