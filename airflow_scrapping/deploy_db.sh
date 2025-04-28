#!/bin/bash

# Récupération des variables d'environnement
source .env

# Variables
RESOURCE_GROUP="mboumedineRG"              # Nom du groupe de ressources existant
SERVER_NAME=$SERVER_NAME                # Nom du serveur PostgreSQL
LOCATION="France Central"                  # Région Azure
SKU_NAME="standard_d2s_v3"                 # SKU pour le serveur PostgreSQL (inclut la taille de calcul)
TIER="Burstable"                           # Niveau de service
STORAGE_SIZE=32                            # Taille du stockage en GiB
STORAGE_TYPE="Premium_LRS"                 # Type de stockage
PERFORMANCE_TIER="p4"                      # Niveau de performance du stockage
START_IP="0.0.0.0"                         # IP de début pour la règle de pare-feu
END_IP="255.255.255.255"                   # IP de fin pour la règle de pare-feu

# Variables provenant du fichier .env
ADMIN_USER=$POSTGRES_USER
ADMIN_PASSWORD=$POSTGRES_PASSWORD
DATABASE_NAME=$POSTGRES_DB

# Créer un serveur PostgreSQL
az postgres flexible-server create \
  --name $SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location "$LOCATION" \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASSWORD \
  --sku-name $SKU_NAME \
  --storage-size $STORAGE_SIZE \
  --storage-type "$STORAGE_TYPE" \
  --performance-tier "$PERFORMANCE_TIER"

  # --tier $TIER \
# Configurer une règle de pare-feu pour autoriser les connexions
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $SERVER_NAME \
  --rule-name AllowIps \
  --start-ip-address $START_IP \
  --end-ip-address $END_IP

# Créer la base de données
echo "Création de la base de données $DATABASE_NAME sur le serveur $SERVER_NAME..."
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $SERVER_NAME \
  --database-name $DATABASE_NAME

# Afficher les informations de connexion
echo "Serveur PostgreSQL créé avec succès !"
echo "URL de connexion : postgresql://$ADMIN_USER:$ADMIN_PASSWORD@$SERVER_NAME.postgres.database.azure.com:5432/$DATABASE_NAME"



