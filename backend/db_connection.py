
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#this code is from mdb->cluster->connect->view full inst->sample code
uri = "mongodb+srv://armeghashri:ClusterZero123!@cluster0.nwajae5.mongodb.net/?appName=Cluster0" 

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Movie'] #name of the db
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)