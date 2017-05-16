<?php
  include("inc/xmlparse.inc.php");
  include("inc/db.inc.php");
  include("inc/tpl_parse.inc.php");
  include("inc/login.inc.php");

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
    if( $_POST['action'] == "heatset" ) {
      $onoff = 0;
      if($_POST['onoffswitch'])
        $onoff = 1;
      $temp = $_POST['temp'];
      setControllValue("heating","onoff",$onoff);
      setControllValue("heating","temp",$temp);
#      print "onoff:".$onoff."<br>";
#      print "temp:".$temp."<br>";
    }
    $onoff = getControllValue("heating","onoff");
    $temp  = getControllValue("heating","temp");

    $param["url"] = $_SERVER['PHP_SELF'];
    $param["heating_on"] = "";
    if($onoff == 1)
      $param["heating_on"] = " checked";
    $param["temperature"] = $temp;

    $mainparams['controlls'] = tplParseOnce("controlls",$param);
  }
  else {
    $param["url"] = $_SERVER['PHP_SELF'];
    $mainparams['controlls'] = tplParseOnce("login",$param);
  }


  print tplParseOnce("main",$mainparams);

?>
