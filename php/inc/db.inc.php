<?php
  function db_connect($db_params=NULL) {
    static $db_link;

    if(isset($db_link)) {
      return $db_link;
    }

    $db_link = mysqli_connect($db_params->host, $db_params->username, $db_params->password);
    if(!$db_link)
      die("Nelze se p?~Yipojit k MySQL: " . mysql_error());

    if(!mysqli_select_db($db_link, $db_params->name))
      die("Nelze vybrat datab??zi: ". mysql_error());
    //mysql_set_charset("iso8859-2");
    //mysql_set_charset("UTF-8");
    mysqli_query($db_link, "SET CHARACTER SET UTF-8");
    return $db_link;
  }

  function db_verify_device($db, $dev, $hash) {
    $dbdev = mysqli_real_escape_string($db, $dev);
    $dbhash = mysqli_real_escape_string($db, $hash);
    $sql = "SELECT count(*) FROM devices WHERE name = '".$dbdev."' AND hash = '".$dbhash."'";
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when reading from DB. ". mysqli_error($db));
    }

    $row = mysqli_fetch_array($ret);
    if($row[0] == 1)
      return True;

    return False;
  }

  function db_set_current_value($db, $sensor, $value) {
    $dbsensor = mysqli_real_escape_string($db, $sensor);
    $dbval = mysqli_real_escape_string($db, $value);

    $sql = "INSERT INTO sensor_current (sensor, val, time) VALUES ('".$dbsensor."','".$dbval."', now()) ON DUPLICATE KEY UPDATE sensor = '".$dbsensor."', val='".$dbval."', time = now()";
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when inserting to DB. ". mysqli_error($db));
    }

  }

  function db_checkLogin($user, $password) {
    $db = db_connect(NULL);
    $dbuser = mysqli_real_escape_string($db, $user);
    $dbpass = mysqli_real_escape_string($db, hash("sha256",$password));
    $sql = "SELECT count(*) FROM users where name = '".$dbuser."' AND password = '".$dbpass."'";
#    print $sql;
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when reading from DB. ". mysqli_error($db));
    }

    $row = mysqli_fetch_array($ret);
    if($row[0] == 1)
      return True;

    return False;
  }


  function storeTokenForUser($user, $token, $timestamp) {
    $db = db_connect(NULL);
    $dbuser = mysqli_real_escape_string($db, $user);
    $dbtoken = mysqli_real_escape_string($db, $token);
    $dbtm = mysqli_real_escape_string($db, $timestamp);

    $sql = "INSERT INTO sessions VALUES('".$dbtoken."', '".$dbuser."', FROM_UNIXTIME(".$dbtm."))";
#    print $sql;
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when inserting to DB. ". mysqli_error($db));
    }
  }
  function fetchTokenByUserName($user, $timestamp) {
    $db = db_connect(NULL);
    $dbuser = mysqli_real_escape_string($db, $user);
    $dbtm = mysqli_real_escape_string($db, $timestamp);

    $sql = "SELECT id FROM sessions WHERE name = '".$dbuser."' AND time = FROM_UNIXTIME(".$dbtm .")";
#    print $sql;
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when reading from DB. ". mysqli_error($db));
    }

    if(mysqli_num_rows($ret) <= 0)
      return False;

    $row = mysqli_fetch_array($ret);
    return $row[0];
  }

  function setControllValue($dev, $controller, $value) {
    $db = db_connect(NULL);
    $dbcontroller = mysqli_real_escape_string($db,$controller);
    $db_value     = mysqli_real_escape_string($db,$value);
    $db_dev       = mysqli_real_escape_string($db,$dev);

    $sql = "INSERT INTO controll VALUES('".$db_dev."','".$dbcontroller."','".$db_value."') ON DUPLICATE KEY UPDATE value = '".$db_value."'";
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when inserting to DB. ". mysqli_error($db));
    }
  }

  function getControllValue($dev, $controller) {
    $db = db_connect(NULL);
    $dbcontroller = mysqli_real_escape_string($db,$controller);
    $db_dev       = mysqli_real_escape_string($db,$dev);
  
    $sql = "SELECT value FROM controll WHERE devicename = '".$db_dev."' AND param = '".$dbcontroller."'";

    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when reading from DB. ". mysqli_error($db));
    }

    if(mysqli_num_rows($ret) <= 0)
      return False;

    $row = mysqli_fetch_array($ret);
    return $row[0];
  }

  function getSensorsLog($interval, $from ) {
    $db = db_connect(NULL);
    $db_from = mysqli_real_escape_string($db, $from);
    $db_interval = mysqli_real_escape_string($db, $interval);

    $sql = "select time, readinterval, IFNULL(t_in, 'null'), IFNULL(t_out, 'null') from sensors_view where time > '".$db_from."' AND readinterval = '".$db_interval."'";
    $ret = mysqli_query($db, $sql);
    if(!$ret) {
      die("An error when reading from DB. ". mysqli_error($db));
    }

    if(mysqli_num_rows($ret) <= 0)
      return False;
    
    return mysqli_fetch_all($ret);
  }
?>
