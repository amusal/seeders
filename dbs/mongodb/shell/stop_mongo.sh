#/bin/bash

#kill -9 `ps -ef|grep mongo|grep -v 'grep'|awk '{print $2}'`

bin_dir=$(cd `dirname $0`; pwd)

$bin_dir/mongod --shutdown --config=$bin_dir/mongo.conf
