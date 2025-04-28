#!/bin/bash
set -e

# Récupération des variables d'environnement
source .env

# Variables
RESOURCE_GROUP=$RESOURCE_GROUP
CONTAINER_NAME="groupe2-mysqlserver"
ACR_NAME=$ACR_NAME
ACR_IMAGE="mysql-custom"
ACR_URL="$ACR_NAME.azurecr.io"
CPU="1"
MEMORY="2"
IP_ADDRESS="Public"
DNS_LABEL="g2mysqlserver"
OS_TYPE="Linux"

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant (ignore l'erreur si inexistant)
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
    --ports 3306 \
    --environment-variables \
      MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
      AIRFLOW_DB=$AIRFLOW_DB \
      AIRFLOW_USER=$AIRFLOW_USER \
      AIRFLOW_PASSWORD=$AIRFLOW_PASSWORD \
      DJANGO_DB=$DJANGO_DB \
      DJANGO_USER=$DJANGO_USER \
      DJANGO_PASSWORD=$DJANGO_PASSWORD \
      API_DB=$API_DB \
      API_USER=$API_USER \
      API_PASSWORD=$API_PASSWORD \
      MYSQL_ROOT_HOST="%"

echo "Serveur MySQL créé avec succès !"
