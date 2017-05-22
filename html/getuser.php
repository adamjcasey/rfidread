<?php

if (!$link = mysql_connect('localhost', 'adamjcas_rfid', 'adamjcas_rfid')) {
    echo 'Could not connect to mysql';
    exit;
}

if (!mysql_select_db('adamjcas_rfiddemo', $link)) {
    echo 'Could not select database';
    exit;
}

$sql    = 'SELECT user FROM access ORDER BY timestamp DESC LIMIT 1';
$result = mysql_query($sql, $link);

if (!$result) {
    echo "DB Error, could not query the database\n";
    echo 'MySQL Error: ' . mysql_error();
    exit;
}

$row = mysql_fetch_assoc($result)
echo $row['user'];

mysql_free_result($result);

?>