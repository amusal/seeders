set Axis_Lib=D:/developtools/apache-axis/axis-1_4/lib
set Java_Cmd=java -Djava.ext.dirs=%Axis_Lib% org.apache.axis.wsdl.WSDL2Java  
set Output_Path=notify  
%Java_Cmd% -o%Output_Path% -ptv.icntv.bc.cos.c2.webservice.server -s -Strue resultNotifyRes.wsdl