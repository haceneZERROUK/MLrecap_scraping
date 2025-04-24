import os
from scrapy.cmdline import execute
from scrapy.utils.project import get_project_settings
# # from azure.identity import ClientSecretCredential
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# from dotenv import load_dotenv


# dotenv_path = "upcoming/.env"
# load_dotenv(dotenv_path=dotenv_path)

# AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", None)
# AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", None)
# AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", None)
# AZURE_VAULT_URL = os.getenv("AZURE_VAULT_URL", None)
# AZURE_STORAGE_URL = os.getenv("AZURE_STORAGE_URL", None)


# # credentials = ClientSecretCredential(
#     client_id = AZURE_CLIENT_ID, 
#     tenant_id = AZURE_TENANT_ID, 
#     client_secret = AZURE_CLIENT_SECRET, 
#     account_url = AZURE_VAULT_URL
# )


# def save_data_to_blob() : 
#     pass


def run():
    spider = "upcomes"
    fichier_sortie = "upcomes"

        # Récupère les settings du projet et désactive le logging interne
    settings = get_project_settings()
    settings.set('LOG_ENABLED', False)

    try:
        
        print(f"\nExecute spider : {spider}\n")
        
        execute([
            'scrapy',
            'crawl',
            spider,
            '-o',
            f'{fichier_sortie}.csv',
            '-o', 
            f'{fichier_sortie}.json'
        ])
        
    except SystemExit as e:
        print(f"\nError, exit script : {e}\n")
        pass

    print(f"\nExtraction {spider} finish.\n")

if __name__ == "__main__":
    run()