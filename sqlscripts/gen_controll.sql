CREATE TABLE controll (
  devicename   varchar(24) NOT NULL,
  param        varchar(24) NOT NULL,
  value        varchar(24)
);


ALTER TABLE controll
  ADD PRIMARY KEY (devicename, param);
