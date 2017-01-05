#!/bin/sh

# JVM options
JAVA_OPTS="-server -Xms256m -Xmx1024m"

# JMX
CATALINA_OPTS="$JAVA_OPTS -Dcom.sun.management.jmxremote.port=10001 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jxmremote.ssl=false"