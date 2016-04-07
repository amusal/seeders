#!/bin/bash

bin_dir=$(cd `dirname $0`; pwd)

$bin_dir/mongod --config=$bin_dir/mongo.conf&

#data_dir='/data/mongodb'
#/usr/local/mongodb/bin/mongod --bind_ip=0.0.0.0 --pidfilepath=$data_dir/pid --dbpath=$data_dir/mongodb_data/ --logpath=$data_dir/mongodb_log --logappend&
