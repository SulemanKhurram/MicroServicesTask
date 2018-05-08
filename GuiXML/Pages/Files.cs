using System;
/* A model class to hold data for all the XML files uploaded on our system */
namespace GuiXML.Pages
{
    public class Files
    {
        public System.Guid ID { get; set; }
        public string FileName { get; set; }
        public string Status { get; set; }
        public string CsvConverted { get; set; }
        public Files(string File, string CurrentStatus, string Csv)
        {
            ID = Guid.NewGuid();
            FileName = File;
            Status = CurrentStatus;
            CsvConverted = Csv;
        }
        public Files(){ ID = Guid.NewGuid();}


    }
}