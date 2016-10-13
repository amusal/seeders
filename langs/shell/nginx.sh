#!/bin/bash

root_dir= $(cd `dirname $0`/..; pwd)

case $1 in
	start)
		$root_dir/sbin/nginx
		;;
	restart)
		kill -HUP `cat $root_dir/logs/nginx.pid`
		;;
	test)
		$root_dir/sbin/nginx -t
		;;
	*)
		echo "USAGE: start|restart|test"
esac
