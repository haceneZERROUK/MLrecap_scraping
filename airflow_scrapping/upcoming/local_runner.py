import os
from scrapy.cmdline import execute
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv


dotenv_path = ".env"
load_dotenv(dotenv_path=dotenv_path)
# load_dotenv()

spider = "upcomes"
saving_file = os.getenv("saving_file")

try:
    
    print(f"\nExecute spider : {spider}\n")
    
    execute([
        'scrapy',
        'crawl',
        spider,
        '-o', 
        f'{saving_file}.json'
    ])
    
except SystemExit as e:
    print(f"\nError, exit script : {e}\n")
    pass

print(f"\nExtraction {spider} finish.\n")


##########################################

# enregistrement dans le blob

account_name = os.getenv("ACCOUNT_NAME")
account_key = os.getenv("ACCOUNT_KEY")
container_name = os.getenv("CONTAINER_NAME")

# Création du service d'accès aux blobs
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

# blob de destination
blob_client = blob_service_client.get_blob_client(container=container_name,blob=saving_file + ".json")

# Ouvre le fichier local et upload-le dans le blob
local_file_path = f"{saving_file}.json"

with open(local_file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
    print(f"Fichier {local_file_path} uploadé dans le blob Azure '{container_name}'.")
