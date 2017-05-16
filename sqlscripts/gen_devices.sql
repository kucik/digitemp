CREATE TABLE devices (
  name         varchar(24) NOT NULL,
  hash         varchar(32)
);


ALTER TABLE devices
  ADD PRIMARY KEY (name);
