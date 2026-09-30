<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");
require('functions.inc.php');

$output = array(
	"error" => false,
	"string" => "",
	"answer" => 0
);

$t = $_GET['text'] ?? '';
if (!is_string($t)) {
    http_response_code(400);
    echo json_encode(['error' => 'text must be a string']);
    exit();
}

$answer=wordcount($t);

$output['string']="Contains ".$answer." words";
$output['answer']=$answer;

echo json_encode($output);
exit();
