<?php

  function tpl_inc($filename, $values=NULL, $lng="") {
    $dir="tpl/";
    $extension = ".htm";
    if(file_exists($dir.$filename."_".$lng.$extension)) {
      $filename = $filename."_".$lng;
    }
    $file = file_get_contents($dir.$filename.$extension);

    return $file;

  }
  function tplParseOnce($filename, $values, $lng="") {
    $dir="tpl/";
    $extension = ".htm";
    if(file_exists($dir.$filename."_".$lng.$extension)) {
      $filename = $filename."_".$lng;
    }
    $file = file_get_contents($dir.$filename.$extension);

    if($values != NULL) {
      foreach($values as $key => $value) {
        $file = str_replace("<$".$key.">",$value,$file);

      }
    }

    return $file;

  }

  function tplParseArray($filename, $values, $lng="") {
    $dir="tpl/";
    $extension = ".htm";
    if(file_exists($dir.$filename."_".$lng.$extension)) {
      $filename = $filename."_".$lng;
    }
    $plain_file = file_get_contents($dir.$filename.$extension);
    $out = "";
    for($i=0;$i < sizeof($values);$i++) {
      $file = $plain_file;
      foreach($values[$i] as $key => $value) {
        $file = str_replace("<$".$key.">",$value,$file);

      }
      $out = $out."\n".$file;
    }

    return $out;

  }

?>
