<?php
  include("inc/xmlparse.inc.php");
  include("inc/db.inc.php");

  function hum_eval($val) {
//    return "START";
    if($val > 60)
      return "START";
    if($val < 55)
      return "STOPX";

    return "STAYX";
  }

  $xml_config = "cfg/config.xml";

  $db = db_connect(getDbConfig($xml_config)); 
  if(db_verify_device($db, $_GET['dev'], $_GET['k'])) { 
    db_set_current_value($db, $_GET['dev'], $_GET['v']);
    db_set_current_value($db, $_GET['dev']."-2", $_GET['v2']);
  }
  print "\rCMD: ".hum_eval($_GET['v']);
//    print "OK  - ".$_GET['v'];
//  }
//  else {
//    print ":(";
//  }
?>
