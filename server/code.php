<?php

// Sanitize our unique id (should only have hexadecimal characters in it)
$UniqueId = preg_replace ('~[^A-Fa-f0-9]~', '', $params['UniqueId']);
$AuthCode = $_GET['code'];

$tokenUrl = "https://jawbone.com/auth/oauth2/token";

// We only have ten minutes to use the auth code before it becomes invalid,
// so we might as well do it on the server immediately rather than wait for
// the app to sync up
$targetParams = [];
$targetParams['client_id'] = UP_CLIENT_ID;
$targetParams['client_secret'] = UP_CLIENT_SECRET;
$targetParams['grant_type'] = 'authorization_code';
$targetParams['code'] = $AuthCode;

$url = $tokenUrl . '?' . http_build_query ($targetParams);

// We need to send a request to them, and in response we get
// a json object 
$ch = curl_init($url);
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec ($ch);

$resultObject = json_decode ($result, true);

if (array_key_exists ('error', $resultObject))
{
	// Oh no! An error!
	// I'm not sure if these will ever contain secure information, so lets
	// not show it to the user just in case
	header("HTTP/1.1 500 Internal Server Error");
	echo "There has been an error.";

	// We should log it so we can see what went wrong
	log_error ("Error obtaining auth token: ".$result);
}
else
{
	$userInfo = [];
	$userInfo['UniqueId'] = $UniqueId;
	$userInfo['AuthCode'] = $AuthCode;
	$userInfo['Token'] = $resultObject;

	// They give us the number of seconds the token lasts for;
	// We should keep track of when we originally got it
	$userInfo['TokenCreated'] = time();

	$filename = APP_USER_DATA_DIR."/{$UniqueId}.json";
	file_put_contents ($filename, json_encode ($userInfo));

	log_success ("Got token for user '".$UniqueId."'");

	$returnToken = $resultObject;
	$returnToken['token_created'] = time();

	$encodedToken = base64_encode (json_encode ($returnToken));
	$urlSafeEncodedToken = strtr ($encodedToken, '+/', '_-');

	# Forward them so they don't refresh or something and screw
	# up their code
	header ('Location: '.APP_BASE_URL.'/done/'.$urlSafeEncodedToken.'/');
}
