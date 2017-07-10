<?php
 
  function get_jsgraph($graphname, $days, $descr) {
    $dt_from = time() -  24*60*60*$days;
    $datefrom = date('Y-m-d H:i:s',$dt_from);


    $interval = 'min';
    $fmt = "H:i";
    if($days >= 30) {
      $fmt = "Y-m-d";
      $interval = 'hour';
    }
 
    $sensordata = getSensorsLog($interval, $datefrom);
  
    for($i=0; $i < sizeof($sensordata); $i++) {
      if($i > 0)
        $jsdata = $jsdata.",\n";
//      $dt = $sensordata[$i][0];
      $dt = date($fmt, strtotime($sensordata[$i][0]));
      $jsdata = $jsdata."['".$dt."'";
  //    $jsdata = $jsdata.", ".$sensordata[$i][1]; //interval
      $jsdata = $jsdata.", ".$sensordata[$i][2];
  //    $jsdata = $jsdata.", ".$sensordata[$i][3];
      $jsdata = $jsdata."]";
    } 
  
      $g1_params['chartdata'] = $jsdata;
      $g1_params['chartname'] = $graphname;
      $g1_params['chart_title'] = $descr;
      return tplParseOnce("chartjs",$g1_params);
  }
?>
