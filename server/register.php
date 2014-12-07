<?php

/*
 * These are all the UP permissions you can request.
 */
$eventTypes =
	[ "basic_read"
	, "extended_read"
	, "location_read"
	, "friends_read"
	, "mood_read"
	, "mood_write"
	, "move_read"
	, "move_write"
	, "sleep_read"
	, "sleep_write"
	, "meal_read"
	, "meal_write"
	, "weight_read"
	, "weight_write"
	, "generic_event_read"
	, "generic_event_write"
	];

/*
 * We need to forward them to the UP auth url, with some info
 * about our app and what permissions we're requesting
 */
$targetParams = [];
$targetParams['response_type'] = 'code';
$targetParams['scope'] = implode (" ", $eventTypes);
$targetParams['client_id'] = UP_CLIENT_ID;
$targetParams['redirect_uri'] = APP_BASE_URL.'/code/'.$params['UniqueId'].'/';

$url = "https://jawbone.com/auth/oauth2/auth?" . http_build_query ($targetParams);

header ("Location: $url");
