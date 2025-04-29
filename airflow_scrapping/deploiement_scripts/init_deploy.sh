#!/bin/bash

# Récupération des variables d'environnement
source .env

# Variables
RESOURCE_GROUP=$RESOURCE_GROUP
CONTAINER_NAME="groupe2-init"
ACR_NAME=$ACR_NAME
ACR_IMAGE="init-airflow"
ACR_URL="$ACR_NAME.azurecr.io"
CPU="1"
MEMORY="2"
IP_ADDRESS="Public"
DNS_LABEL="init-airflow"
OS_TYPE="Linux"

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP -y || true

# Création du partage Azure Files (si pas déjà fait)
az storage share create \
  --account-name $BLOB_ACCOUNT_NAME \
  --name $FILE_SHARE_NAME \
  --account-key $BLOB_ACCOUNT_KEY

# Création des sous-dossiers dans le partage
az storage directory create --name "dags" --share-name $FILE_SHARE_NAME --account-name $BLOB_ACCOUNT_NAME --account-key $BLOB_ACCOUNT_KEY
az storage directory create --name "logs" --share-name $FILE_SHARE_NAME --account-name $BLOB_ACCOUNT_NAME --account-key $BLOB_ACCOUNT_KEY
az storage directory create --name "plugins" --share-name $FILE_SHARE_NAME --account-name $BLOB_ACCOUNT_NAME --account-key $BLOB_ACCOUNT_KEY
az storage directory create --name "data" --share-name $FILE_SHARE_NAME --account-name $BLOB_ACCOUNT_NAME --account-key $BLOB_ACCOUNT_KEY
az storage directory create --name "upcoming" --share-name $FILE_SHARE_NAME --account-name $BLOB_ACCOUNT_NAME --account-key $BLOB_ACCOUNT_KEY

# Déploiement du conteneur avec le volume monté
az container create \
    --name $CONTAINER_NAME \
    --resource-group $RESOURCE_GROUP \
    --image $ACR_URL/$ACR_IMAGE \
    --cpu $CPU \
    --memory $MEMORY \
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
        AIRFLOW__CORE__LOAD_EXAMPLES=$AIRFLOW__CORE__LOAD_EXAMPLES \
        ACCOUNT_NAME=$BLOB_ACCOUNT_NAME \
        ACCOUNT_KEY=$BLOB_ACCOUNT_KEY \
        CONTAINER_NAME=$BLOB_CONTAINER_NAME \
        saving_file=$saving_file \
        AIRFLOW__CORE__DAGS_FOLDER=/mnt/airflow-files/dags \
        AIRFLOW__LOGGING__BASE_LOG_FOLDER=/mnt/airflow-files/logs \
        AIRFLOW__CORE__PLUGINS_FOLDER=/mnt/airflow-files/plugins \
    --azure-file-volume-share-name $FILE_SHARE_NAME \
    --azure-file-volume-account-name $BLOB_ACCOUNT_NAME \
    --azure-file-volume-account-key $BLOB_ACCOUNT_KEY \
    --azure-file-volume-mount-path $MOUNT_PATH
  
# Affichage des informations
echo "Le déploiement a réussi."

