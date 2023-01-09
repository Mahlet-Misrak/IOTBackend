import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "7D_XrVQ3wR5ZY9UbtrhBptLxOIC9HFXSfB4XVedXsGS3Rpc8aS1cp2Qb6cUJN6VM6z89GQ7ZIiki0Y1B-2h_Pw=="
org = "ce77d90151c3f0c2"
url = "https://eastus-1.azure.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="sensor_data"

# write_api = client.write_api(write_options=SYNCHRONOUS)
   
# for value in range(5):
#   point = (
#     Point("measurement1")
#     .tag("tagname1", "tagvalue1")
#     .field("field1", value)
#   )
#   write_api.write(bucket=bucket, org="mahletmisrak1@gmail.com", record=point)
#   time.sleep(1) # separate points by 1 second

query_api = client.query_api()

query = """from(bucket: "sensor_data_norm")
 |> range(start: -30d)
 |> filter(fn: (r) => r._measurement == "apiS105")
 |> filter(fn: (r) => r["_field"] == "sound")
 |> last()"""
tables = query_api.query(query, org=org)
print(tables)
for table in tables:
  for record in table.records:
    print(record.get_vlaus())
