<?php
#  include("inc/db.inc.php");

function GenerateRandomToken() {
    return bin2hex(openssl_random_pseudo_bytes(32));
}

function onLogin($user) {
    $token = GenerateRandomToken(); // generate a token, should be 128 - 256 bit
    $time = time();
    storeTokenForUser( $user, $token, $time);
    $cookie = $user . ':' .$time. ':' . $token;
    $mac = hash_hmac('sha256', $cookie, HASHKEY);
    $cookie .= ':' . $mac;
    setcookie('rememberme', $cookie);
#    print "setcookie: ".$cookie;
#    print "<br>cook".$_COOKIE['rememberme'];
}

function rememberMe() {
#    print "cookie check";
#    print $_COOKIE['rememberme'];
    $cookie = isset($_COOKIE['rememberme']) ? $_COOKIE['rememberme'] : '';
    if ($cookie) {
#        print "cookie:".$cookie;
        list ($user, $time, $token, $mac) = explode(':', $cookie);
        if (!hash_equals(hash_hmac('sha256', $user . ':' .$time. ':' . $token, HASHKEY), $mac)) {
            return false;
        }
        $usertoken = fetchTokenByUserName($user, $time);
        if ($usertoken && hash_equals($usertoken, $token)) {
            logUserIn($user);
        }
    }
}

function logUserIn($user) {
  $_SESSION['user'] = $user;
}


function getIsLogged() {
  if($_SESSION['user'])
    return True;

  rememberMe();
  if($_SESSION['user'])
    return True;

  return False;
}

function userLogIn($user, $password) {
  if(db_checkLogin($user, $password)) {
    logUserIn($user);
    onLogin($user);
    return True;
  }
  return False;
}

?>
