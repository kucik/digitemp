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
  
  $mainparams['g1_chart'] = get_jsgraph("TDay", 1, "Day temperature");
  $mainparams['g2_chart'] = get_jsgraph("TMonth",30, "Month temperature");
  $mainparams['g3_chart'] = get_jsgraph("TYear",365, "Year temperature");


  print tplParseOnce("main_charts",$mainparams);
 
//  print date('Y-m-d H:i:s',time() - 24*60*60);

?>
