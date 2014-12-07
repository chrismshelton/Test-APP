<?php

function log_error ($errorMessage)
{
	$logFile = APP_DATA_DIR.'/logs/error.log';
	$logLine = "[".date ('Y-m-d H:i:s')."] ERROR: ".$errorMessage."\n";

	file_put_contents ($logFile, $logLine, FILE_APPEND | LOCK_EX);
}

function log_success ($logMessage)
{
	$logFile = APP_DATA_DIR.'/logs/success.log';
	$logLine = "[".date ('Y-m-d H:i:s')."] ".$logMessage."\n";

	file_put_contents ($logFile, $logLine, FILE_APPEND | LOCK_EX);
}
