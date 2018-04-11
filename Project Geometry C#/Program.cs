using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace ProjectGeometry
{
    class Program
    {

        static void Main(string[] args)
        {
            ProjectGeometry();

            Console.ReadLine();
        }

        private static async void ProjectGeometry()
        {
            string urlToUse = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/EGT18_Gemeentehuizen_ReadOnly/FeatureServer/0";

            //Get Feature from service
            string query = "OBJECTID=1";
            WebClient wc = new WebClient();
            string queryResult = wc.DownloadString(String.Format("{0}/query?f=json&where={1}", urlToUse, query));
            Console.WriteLine(queryResult);

            //get properties from result string
            dynamic feature = Newtonsoft.Json.JsonConvert.DeserializeObject(queryResult);
            dynamic geom = feature.features[0].geometry;
            Console.WriteLine(geom);
            dynamic inSR = feature.spatialReference;

            //creating the post variables
            string outSR = "{\"wkid\" : 4326}";
            string geometries = string.Format("{{\"geometryType\" : \"esriGeometryPoint\",\"geometries\" : [{0}]}}", geom.ToString());
            var values = new Dictionary<string, string>
            {
                {"f", "json" },
                {"inSR",inSR.ToString() },
                {"outSR",outSR },
                {"geometries",geometries }
            };

            //projecting the geometry through a geometryservice
            var content = new FormUrlEncodedContent(values);
            HttpClient client = new HttpClient();
            var response = await client.PostAsync("http://localhost:6080/arcgis/rest/services/Utilities/Geometry/GeometryServer/project", content);
            var responseString = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseString);


        }
    }
}
