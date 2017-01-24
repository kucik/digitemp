CREATE TABLE temp_sensors (
  time           timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sensor         varchar(24) NOT NULL,
  readinterval   varchar(10) NOT NULL,
  val            NUMERIC(4,2)
);

ALTER TABLE temp_sensors
  ADD PRIMARY KEY (time, sensor, readinterval);
