
CREATE OR REPLACE VIEW sensors_view AS
  SELECT 
    t.time, 
    t.readinterval, 
    t_in.val t_in, 
    t_out.val t_out 
  FROM temp_sensors t
     LEFT JOIN (temp_sensors as t_in)  on (t_in.sensor  = 'in'  AND t.time = t_in.time AND t.readinterval = t_in.readinterval)
     LEFT JOIN (temp_sensors as t_out) on (t_out.sensor = 'out' AND t.time = t_out.time AND t.readinterval = t_out.readinterval);
