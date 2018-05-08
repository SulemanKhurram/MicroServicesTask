# MicroServicesTask
This project contains three different microservices that will contact with each other to convert an xml file to csv data.

This Gui component will take XML file(s) as input and will pass them on to xml-parser service to parse the tables out of it.

Requirements:

 -> RabbitMq  
 -> AspNet Core  
 -> Docker (if you want to use docker, docker file is provided)  

Following are some screenshots to display the working of these services. 

Gui service runs on the port 5000  
Xml parser service runs on port 5051  
Csv converter service runs on port 5002  

![alt text](https://raw.githubusercontent.com/SulemanKhurram/MicroServicesTask/master-1/interface_01.png)
![alt text](https://raw.githubusercontent.com/SulemanKhurram/MicroServicesTask/master-1/interface_02.png)

