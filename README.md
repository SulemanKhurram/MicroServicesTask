# MicroServicesTask
This project contains three different microservices that will contact with each other to convert an xml file to csv data.

This is the service for parsing the xml file got from gui. In this parser, ComposedBlock with type = "table" is parsed and separated out
and then sent to python csv-converter using RabbitMQ. Whole ouput of the task is shown in branch master-1 but some console logs for 
displaying the parsing of xml is shown in the following.



![alt text](https://raw.githubusercontent.com/SulemanKhurram/MicroServicesTask/master-2/console_ouput_csvconverter.png)
