#!/bin/bash


# Variables
RESOURCE_GROUP="mboumedineRG"              # Nom du groupe de ressources
CONTAINER_NAME="groupe2-webserver"         # Nom du conteneur
SERVER_NAME="groupe2-server"
ACR_NAME="mboumedineregistry"              # Nom de ton Azure Container Registry
ACR_IMAGE="airflow-webserver"              # Nom de l'image dans le ACR
ACR_URL="$ACR_NAME.azurecr.io"             # URL du registre
CPU="1"                                    # Nombre de CPUs
MEMORY="2"                                 # Mémoire (RAM)
IP_ADDRESS="Public"                        # Type d'IP (Public ou Private)
DNS_LABEL="airflow-webserver"                   # Label DNS pour l'adresse publique
OS_TYPE="Linux"                            # Type d'OS (Linux ou Windows)

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP -y

# Récupération des variables d'environnement
source .env

# Déploiement du conteneur
az container create \
    --name $CONTAINER_NAME \
    --resource-group $RESOURCE_GROUP \
    --image $ACR_URL/$ACR_IMAGE \
    --cpu $CPU \
    --memory $MEMORY \
    --ports 8080 \
    --registry-login-server $ACR_URL \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --ip-address $IP_ADDRESS \
    --os-type $OS_TYPE \
    --dns-name-label $DNS_LABEL \
    --environment-variables \
        AIRFLOW__CORE__EXECUTOR=$AIRFLOW__CORE__EXECUTOR \
        AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=$AIRFLOW__DATABASE__SQL_ALCHEMY_CONN \
        AIRFLOW__CORE__FERNET_KEY=$AIRFLOW__CORE__FERNET_KEY \
        AIRFLOW__CORE__LOAD_EXAMPLES=$AIRFLOW__CORE__LOAD_EXAMPLES 

az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --rule-name DockerAccess \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Affichage des informations
echo "Le déploiement a réussi."


