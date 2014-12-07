<?php

$request_path = $_SERVER['DOCUMENT_URI'];

// Not included in the repo... but there is a "private.sample.php"
// showing the stuff that needs to be defined
require (__DIR__.'/private.php');

// Some dumb functions for error logging
require (__DIR__.'/helperFunctions.php');

$params = [];

/*
 * php-fpm doesn't have any good way of doing rewrites, besides.. php.
 * UP can only redirect to a plain url, not like "url.com?param1=something&.."
 * so we have to have "fancy" urls
 *
 * So here is the crappiest url routing code ever:
 */

if (preg_match ('~^/jb/register/(?P<UniqueId>[A-Fa-f0-9]+)/$~', $request_path, $m))
{
	$params['UniqueId'] = $m['UniqueId'];
	require (__DIR__.'/register.php');
}
elseif (preg_match ('~^/jb/code/(?P<UniqueId>[A-Fa-f0-9]+)/$~', $request_path, $m))
{
	$params['UniqueId'] = $m['UniqueId'];
	require (__DIR__.'/code.php');
}
elseif (preg_match ('~^/jb/done/(?P<Result>[A-Za-z0-9_\-]+=*)/$~', $request_path, $m))
{
	$params['Result'] = $m['Result'];
	require (__DIR__.'/done.php');
}
else
{
	header ("HTTP/1.0 404 Not Found");
}
