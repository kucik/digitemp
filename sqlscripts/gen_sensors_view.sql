/**
 * View joining all sensors to one line select.
 * Each sensor have to have left joint here.
 */

CREATE OR REPLACE VIEW sensors_view AS
  SELECT
    t.time,
    t.readinterval,
    t_in.val t_in,
    t_liv1.val t_liv1,
    t_out1.val t_out1
  FROM temp_sensors t
     LEFT JOIN (temp_sensors as t_in)  on (t_in.sensor  = 'in'  AND t.time = t_in.time AND t.readinterval = t_in.readinterval)
     LEFT JOIN (temp_sensors as t_liv1)  on (t_liv1.sensor  = 'liv1'  AND t.time = t_liv1.time AND t.readinterval = t_liv1.readinterval)
     LEFT JOIN (temp_sensors as t_out1) on (t_out1.sensor = 'out1' AND t.time = t_out1.time AND t.readinterval = t_out1.readinterval);
