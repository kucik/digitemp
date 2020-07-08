<?php
  include("inc/xmlparse.inc.php");
  include("inc/db.inc.php");
  include("inc/tpl_parse.inc.php");
  include("inc/login.inc.php");
  include("inc/graph.inc.php");


  $xml_config_file = "cfg/config.xml";
  date_default_timezone_set("UTC");
  $cfg = getXmlConfig($xml_config_file);
  $db = db_connect(getDbConfig($xml_config_file));

  define("HASHKEY",$cfg->hashkey);

  /* Login check */
  if($_POST['action'] == "login") {
    $ret = userLogIn($_POST['login'], $_POST['pass']);
    if(!$ret) {
      print "Bad login!";
    }
  }

  if(getIsLogged()) {
    /* Process set controlls */
    if( $_POST['action'] == "heatset" ) {
      $onoff = 0;
      if($_POST['onoffswitch'])
        $onoff = 1;
      $temp = $_POST['temp'];
      $temp_night = $_POST['temp_night'];
      setControllValue("heating","onoff",$onoff);
      setControllValue("heating","temp",$temp);
      setControllValue("heating","temp_night",$temp_night);
#      print "onoff:".$onoff."<br>";
#      print "temp:".$temp."<br>";
    }

    /* Get controlls values */
    $onoff = getControllValue("heating","onoff");
    $temp  = getControllValue("heating","temp");
    $temp_night  = getControllValue("heating","temp_night");
    $feedback  = getControllValue("heating","feedback");

    /* Show controlls */
    $param["url"] = $_SERVER['PHP_SELF'];
    $param["heating_on"] = "";
    if($onoff == 1)
      $param["heating_on"] = " checked";
    $param["temperature"] = $temp;
    $param["temperature_night"] = $temp_night;

    $param["heatfbimg"] = "loc_stat1.gif";
    if($feedback == 1)
      $param["heatfbimg"] = "loc_stat5.gif";

    $mainparams['controlls'] = tplParseOnce("controlls",$param);
  }
  else {
    $param["url"] = $_SERVER['PHP_SELF'];
    $mainparams['controlls'] = tplParseOnce("login",$param);
  }

  /* Google charts */
  $mainparams['chart_daily'] = get_jsgraph("TDay", 1, "Day temperature");
  $mainparams['waterlevel_daily'] = get_jsgraph("TDay", 30, "Water level", "waterlevel");
/*  $mainparams['chart_mon'] = get_jsgraph("TMonth",30, "Month temperature");
  $mainparams['chart_year'] = get_jsgraph("TYear",365, "Year temperature");
*/
  print tplParseOnce("main",$mainparams);

?>
