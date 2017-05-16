<?php
  date_default_timezone_set("Etc/UTC");

  function getDbConfig($xml_file) { 
    $xml_config = simplexml_load_file($xml_file);
    return $xml_config->db;

    foreach($xml_config as $dbc) {
      print "  db=".$dbc->getName()."</br>\n";
      if($dbc->getName() == 'db') {
//        foreach($dbc as $dbp) {
//          $db_params[$dbp->getName()] = 
//        }
        print $dbc->host;
        print $dbc->username;
      }
    }

  }

  function getXmlConfig($xml_file) {
    $xml_config = simplexml_load_file($xml_file);
    return $xml_config;
  }

?>
