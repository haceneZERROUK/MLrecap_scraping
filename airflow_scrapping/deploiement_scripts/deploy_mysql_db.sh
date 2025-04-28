#!/bin/bash

# Récupération des variables d'environnement
source .env

# Variables
RESOURCE_GROUP="mboumedineRG"
SERVER_NAME=$SERVER_NAME  # À rendre unique si besoin
LOCATION="France Central"
SKU_NAME="Standard_B1ms"          # Le moins cher et dans l’offre gratuite
TIER="Burstable"
STORAGE_SIZE=20                   # Stockage minimum supporté
MYSQL_VERSION="8.0.21"            # Version récente et prise en charge
START_IP="0.0.0.0"
END_IP="255.255.255.255"

# Variables provenant du fichier .env
ADMIN_USER=$MYSQL_USER
ADMIN_PASSWORD=$MYSQL_PASSWORD
DATABASE_NAME=$MYSQL_DB

# Créer un serveur MySQL Flexible
az mysql flexible-server create \
  --name $SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location "$LOCATION" \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASSWORD \
  --sku-name $SKU_NAME \
  --tier $TIER \
  --storage-size $STORAGE_SIZE \
  --version $MYSQL_VERSION

# Configurer une règle de pare-feu pour autoriser les connexions
az mysql flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --rule-name AllowIps \
  --start-ip-address $START_IP \
  --end-ip-address $END_IP

# Créer la base de données
echo "Création de la base de données $DATABASE_NAME sur le serveur $SERVER_NAME..."
az mysql flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $SERVER_NAME \
  --database-name $DATABASE_NAME

# Afficher les informations de connexion
echo "Serveur MySQL créé avec succès !"
echo "URL de connexion : mysql://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_NAME.mysql.database.azure.com:3306/$DATABASE_NAME"
