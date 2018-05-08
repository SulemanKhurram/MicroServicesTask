using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using System.IO;
using Microsoft.AspNetCore.Hosting;
using RabbitMQ.Client;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Xml;

namespace xml_parser.Controllers

{
    [Route("api/[controller]")]
    public class XMLParserController : Controller
    {
        private readonly IHostingEnvironment _environment;
        public XMLParserController(IHostingEnvironment environment)
        {
            _environment = environment ?? throw new ArgumentNullException(nameof(environment));
        }
        // GET api/xmlparser
        [HttpGet]
        public IEnumerable<string> Get()
        {
            return new string[] { "test", "test" }; //Just a testing endpoint to check working
        }


        // POST api/xmlparser
        [HttpPost]
        public async Task<string> Post(IFormFile file)
        {
            //Following code block deals with getting File from the GUI and extracting tables from it.
            var result = string.Empty;
            XmlDocument doc = new XmlDocument();
            doc.Load(file.OpenReadStream());
            XmlNodeList elemList = doc.GetElementsByTagName("ComposedBlock");
            for (int i=0; i < elemList.Count; i++)
                {   
                    XmlNode element = elemList[i];
                    if(element.Attributes["TYPE"].Value == "table"){
                        var xmlTable = element.OuterXml;
                        result = result + xmlTable;
                    }
                }  

            Console.WriteLine(result); //Printed results to check if its working fine
            
            //Following code block is responsible for messaging with Python microservice using RabbitMQ
            if(!string.IsNullOrEmpty(result) ){
                var factory = new ConnectionFactory() { HostName = "localhost" };
                using(var connection = factory.CreateConnection())
                using(var channel = connection.CreateModel())
                {
                    channel.QueueDeclare(queue: "xmltocsv",
                                        durable: false,
                                        exclusive: false,
                                        autoDelete: false,
                                        arguments: null);
                    channel.QueuePurge("xmltocsv");

                    var body = Encoding.UTF8.GetBytes(result);

                    channel.BasicPublish(exchange: "",
                                        routingKey: "xmltocsv",
                                        basicProperties: null,
                                        body: body); //It will send the message to python microservice containing XML Tables
                    Console.WriteLine(" [x] Sent {0}", result);
                    var content = new MultipartFormDataContent();
                    using (var client = new HttpClient())
                    {
                        client.BaseAddress = new Uri("http://localhost:5002/");
                        var response =  await client.PostAsync("converter",content).ConfigureAwait(false);
                        Console.WriteLine(response);
                    }
                    connection.Close();
                }
                
            }
            return "Successfully Uploaded";

        }
    }
}
