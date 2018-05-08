# MicroServicesTask
This project contains three different microservices that will contact with each other to convert an xml file to csv data.

This microservice handles incoming xml tables data and converts them to comma separated values. It contains both receiveing and sending 
ends of RabbitMQ. It shares data with Gui to display csv converted data. Some of the output of service is shown below.

Requirements:  
Flask  
Flask-Resful  
pirka  


![alt text](https://raw.githubusercontent.com/SulemanKhurram/MicroServicesTask/master-3/console_ouput_csvconverter.png)
