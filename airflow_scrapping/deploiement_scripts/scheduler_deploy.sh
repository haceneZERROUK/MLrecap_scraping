#!/bin/bash

# Récupération des variables d'environnement
source .env

# Variables
RESOURCE_GROUP=$RESOURCE_GROUP
CONTAINER_NAME="groupe2-scheduler"         # Nom du conteneur
ACR_NAME=$ACR_NAME
ACR_IMAGE="scheduler-airflow"              # Nom de l'image dans le ACR
ACR_URL="$ACR_NAME.azurecr.io"             # URL du registre
CPU="1"                                    # Nombre de CPUs
MEMORY="2"                                 # Mémoire (RAM)
IP_ADDRESS="Public"                        # Type d'IP (Public ou Private)
DNS_LABEL="scheduler-airflow"                   # Label DNS pour l'adresse publique
OS_TYPE="Linux"                            # Type d'OS (Linux ou Windows)

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP -y || true

# Déploiement du conteneur
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
