#!/bin/bash
#=================
# auto deploy
#=================

ROOT_DIR=$(cd `dirname $0`/..; pwd)
SRC_DIR=$ROOT_DIR/src
CONF_DIR=$ROOT_DIR/conf
cd $ROOT_DIR
# echo "root_dir:" ${ROOT_DIR}

function package() {
  cd $SRC_DIR
  update
  conf
  mvn clean package -Dmaven.test.skip=true
  cd $ROOT_DIR
}

function update() {
  cd $SRC_DIR
  git checkout develop
  git pull origin develop
  cd $ROOT_DIR
}

function conf() {
  echo "copy conf to src"
}

function deploy() {
  echo "cp target to webcontainer"
}

case $1 in
  update)
    update
    ;;
  package)
    package
    ;;
  copy_conf)
    copy_conf
    ;;
  deploy)
    deploy
    ;;
  *)
    echo "USAGE:[pakcage|deploy|update|conf]"
esac
