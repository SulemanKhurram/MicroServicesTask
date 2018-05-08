using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using Microsoft.AspNetCore.Hosting;
using System.Net.Http;
using System.Net.Http.Headers;
using RabbitMQ.Client;
using System.Text;
using System.Xml;
using RabbitMQ.Client.Events;

namespace GuiXML.Pages
{
    public class IndexModel : PageModel
    {
        public string Message { get; set; }
        public string CsvData { get; set; } //Will keep track of csv data of current uploaded file
        public string CurrentFile { get; set; } // Will keep track of the current file getting processed
        [BindProperty]
        public IList<IFormFile> uploadedFiles { get; set; } //all the files that got uploaded using user interface
        public List<Files> filesInformation { get; set; } //all the information of files is contained in this list
        public Files CurrentUpload{ get; set; }
        private IHostingEnvironment _environment;
        public IndexModel(IHostingEnvironment environment)
        {
            _environment = environment;
            filesInformation = new List<Files>();
        }
        /* A method to keep contact with the queue in RabbitMQ to receive converted csv data */
        public void GetCsv(){
            var factory = new ConnectionFactory() { HostName = "localhost" };
            using(var connection = factory.CreateConnection())
            using(var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: "csvconversion",
                                    durable: false,
                                    exclusive: false,
                                    autoDelete: false,
                                    arguments: null); //This same queue is used at python end as well for csv converted data

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (model, ea) =>
                {
                    var body = ea.Body;
                    var message = Encoding.UTF8.GetString(body);
                    Console.WriteLine(" [x] Received {0}", message);
                };
                var data = channel.BasicGet("csvconversion", true); // will take only one message
                var convertedCsv = "";
                //this condition checks whether there exists any ComposedBlock in XML with type table or not, if not then just update status
                if(data == null){
                    convertedCsv = "No XML table found in this document.";
                }
                else{
                    convertedCsv = System.Text.Encoding.UTF8.GetString(data.Body);
                }
                Console.WriteLine(convertedCsv);
                filesInformation.Remove(CurrentUpload); //remove old entry of current upload without csv data field filled
                CurrentUpload.CsvConverted = convertedCsv;
                filesInformation.Add(CurrentUpload); //add it again after filling csv data
                connection.Close();
            }
        }
        public async Task OnPostAsync()
        {    
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri("http://localhost:5051/"); //url to contact with other .Net core microservice
                CsvData = "";
                //A loop on all multiple/ single uploaded file(s)
                foreach(IFormFile file in uploadedFiles){
                    CurrentFile = file.FileName;
                    if (file.Length <= 0)
                        continue;
                    Files upload = new Files();
                    upload.FileName = file.FileName;
                    upload.Status = "Uploading";
                    upload.CsvConverted = "";
                    
                    filesInformation.Add(upload);

                    var fileName = ContentDispositionHeaderValue.Parse(file.ContentDisposition).FileName.Trim('"');
                    //Following code block manages connected with other .Net core webservice which handles XML parsing 
                    using (var content = new MultipartFormDataContent())
                    {
                        content.Add(new StreamContent(file.OpenReadStream())
                        {
                            Headers =
                            {
                                ContentLength = file.Length,
                                ContentType = new MediaTypeHeaderValue(file.ContentType)
                            }
                        }, "File", fileName);
                       
                        var response = await client.PostAsync("api/xmlparser", content).ConfigureAwait(false);
                        Console.WriteLine(response); // to check if its working or getting blocked
                    }
                    filesInformation.Remove(upload); // remove old entry without status updated
                    upload.Status = "Uploaded";
                    filesInformation.Add(upload); // add new entry with status field added
                    CurrentUpload = upload;
                    this.GetCsv(); //after contacting with xml-parser contact with csv converter to get that from the queue created by it
                }
                
                
            }
            
        }
    }
}
