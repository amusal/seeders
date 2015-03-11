#!/bin/bash
# place 'memcached.sh' in "$MEMCACHED_HOME/bin"

ROOT_DIR=$(cd "`dirname $0`/.."; pwd)
cd $ROOT_DIR

OPTION=$1


function start() {
        bin/memcached -d -c 10240 -m 512m -P $ROOT_DIR/bin/pid
}

function stop() {
        kill -9 `cat bin/pid`
        rm -f bin/pid
}

case $OPTION in
	start)
		start
		echo "memcached started"
		;;
	stop)
		stop
		echo "memcached stopped"
		;;
	restart)
		stop
		start
		echo "restart"
		;;
	*)
		echo "USAGE[start|stop|restart]"
esac
