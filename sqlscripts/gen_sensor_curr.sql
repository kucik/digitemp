CREATE TABLE sensor_current (
  time           timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sensor         varchar(24) NOT NULL,
  val            NUMERIC(4,2)
);

ALTER TABLE sensor_current
  ADD PRIMARY KEY (sensor);
