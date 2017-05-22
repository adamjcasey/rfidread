<?php

$user = $_GET["user"];

if (!$link = mysql_connect('localhost', 'adamjcas_rfid', 'adamjcas_rfid')) {
    echo 'Could not connect to mysql';
    exit;
}

if (!mysql_select_db('adamjcas_rfiddemo', $link)) {
    echo 'Could not select database';
    exit;
}

$sql    = "INSERT INTO access (user) VALUES ($user)";
$result = mysql_query($sql, $link);

if (!$result) {
    echo "DB Error, could not query the database\n";
    echo 'MySQL Error: ' . mysql_error();
    exit;
}

?>