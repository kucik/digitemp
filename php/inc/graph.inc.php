<?php
 
  function get_jsgraph($graphname, $days, $descr, $sensor='all') {
    $dt_from = time() -  24*60*60*$days;
    $datefrom = date('Y-m-d H:i:s',$dt_from);


    $interval = 'min';
    $fmt = "H:i";

    if($days >= 30) {
      $fmt = "Y-m-d";
      $interval = 'hour';
    }

    if($sensor == 'waterlevel') {
      $interval = 'min';
      $fmt = "m-d H:i";
    }

    if($sensor == 'all') {
      $sensordata = getSensorsLog($interval, $datefrom);
    }
    else {
      $sensordata = getSingleLog($interval, $datefrom, $sensor);
    }

    for($i=0; $i < sizeof($sensordata); $i++) {
      if($i > 0)
        $jsdata = $jsdata.",\n";
//      $dt = $sensordata[$i][0];
      $dt = date($fmt, strtotime($sensordata[$i][0]));
      $jsdata = $jsdata."['".$dt."'";
  //    $jsdata = $jsdata.", ".$sensordata[$i][1]; //interval
      $jsdata = $jsdata.", ".$sensordata[$i][2];
//
      if($sensor == 'all') {
        $jsdata = $jsdata.", ".$sensordata[$i][3];
        $jsdata = $jsdata.", ".$sensordata[$i][4];
      }
      $jsdata = $jsdata."]";
    } 
  
      $g1_params['chartdata'] = $jsdata;
      if($sensor == 'all') {
        $g1_params['chartname'] = $graphname;
      }
      else {
        $g1_params['chartname'] = $sensor.$graphname;
      }
      $g1_params['chart_title'] = $descr;
      if($sensor == 'all') {
        return tplParseOnce("chartjs",$g1_params);
      }
      else {
        return tplParseOnce("chart_singlejs",$g1_params);
      }
  }
?>
