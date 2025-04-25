#!/bin/bash
set -e  # Arrête le script si une commande échoue

# Variables
RESOURCE_GROUP="kaassiRG"
CONTAINER_GROUP_NAME="airflow-instance"
ACR_NAME="groupe2allocine"
REGION="francecentral"
DNS_LABEL="airflowappdemo"  # doit être unique sur Azure
DOCKER_COMPOSE_FILE="docker-compose.yml"      # Nom de votre fichier docker-compose
WEB_IMAGE_NAME="webserver"
SCHEDULER_IMAGE_NAME="scheduler"
INIT_IMAGE_NAME="airflow-init"
POSTGRES_IMAGE="postgres"

# Charger les variables depuis .env si nécessaire
# . ./.env

echo "Authentification à Azure et récupération des credentials ACR..."
az acr login --name $ACR_NAME
az acr update -n $ACR_NAME --admin-enabled true
REGISTRY_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
REGISTRY_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Optionnel : supprimer l'ancien groupe de conteneurs
echo "Suppression de l'ancien groupe de conteneurs s'il existe..."
az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_GROUP_NAME --yes || true

echo "📦 Build & push des images…"
# Ici on part du principe que vous utilisez l'image officielle Airflow
docker pull apache/airflow:2.9.1-python3.10
for svc in webserver scheduler airflow-init; do
  docker tag apache/airflow:2.9.1-python3.10 \
    "${ACR_NAME}.azurecr.io/${svc}:latest"
  docker push "${ACR_NAME}.azurecr.io/${svc}:latest"
done

# Postgres dans votre ACR
docker pull postgres:13
docker tag postgres:13 "${ACR_NAME}.azurecr.io/postgres:latest"
docker push "${ACR_NAME}.azurecr.io/postgres:latest"

# # Build des images
# echo "Construction des images Docker Airflow..."
# # docker build -t $WEB_IMAGE_NAME -f Dockerfile.webserver .
# # docker build -t $SCHEDULER_IMAGE_NAME -f Dockerfile.scheduler .
# # docker build -t $INIT_IMAGE_NAME -f Dockerfile.airflow-init .
# # docker pull $POSTGRES_IMAGE  # Assurez-vous que l'image Postgres est disponible
# docker-compose -f $DOCKER_COMPOSE_FILE build  # Si vous utilisez docker-compose

# # Tag
# echo "Tag des images..."
# docker tag $WEB_IMAGE_NAME $ACR_NAME.azurecr.io/$WEB_IMAGE_NAME:latest
# docker tag $SCHEDULER_IMAGE_NAME $ACR_NAME.azurecr.io/$SCHEDULER_IMAGE_NAME:latest
# docker tag $INIT_IMAGE_NAME $ACR_NAME.azurecr.io/$INIT_IMAGE_NAME:latest
# docker tag $POSTGRES_IMAGE $ACR_NAME.azurecr.io/$POSTGRES_IMAGE:latest

# # Push
# echo "Push des images vers ACR..."
# docker push $ACR_NAME.azurecr.io/$WEB_IMAGE_NAME:latest
# docker push $ACR_NAME.azurecr.io/$SCHEDULER_IMAGE_NAME:latest
# docker push $ACR_NAME.azurecr.io/$INIT_IMAGE_NAME:latest
# docker push $ACR_NAME.azurecr.io/$POSTGRES_IMAGE:latest

# YAML dynamique pour ACI
echo "Création du fichier aci-deploy.yaml..."
cat > aci-deploy.yaml <<EOF
apiVersion: 2019-12-01
location: ${REGION}
name: ${CONTAINER_GROUP_NAME}
properties:
  containers:
  - name: webserver
    properties:
      image: ${ACR_NAME}.azurecr.io/${WEB_IMAGE_NAME}:latest
      resources:
        requests:
          cpu: 2
          memoryInGb: 4
      environmentVariables:
      - name: AIRFLOW__CORE__EXECUTOR
        value: "LocalExecutor"
      - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
        value: "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
      - name: AIRFLOW__CORE__FERNET_KEY
        value: "fernet_key_dev_123"
      - name: AIRFLOW__CORE__LOAD_EXAMPLES
        value: "false"
      ports:
      - port: 8080
  - name: scheduler
    properties:
      image: ${ACR_NAME}.azurecr.io/${SCHEDULER_IMAGE_NAME}:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
      environmentVariables:
      - name: AIRFLOW__CORE__EXECUTOR
        value: "LocalExecutor"
      - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
        value: "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
      - name: AIRFLOW__CORE__FERNET_KEY
        value: "fernet_key_dev_123"
      - name: AIRFLOW__CORE__LOAD_EXAMPLES
        value: "false"
  - name: postgres
    properties:
      image: ${ACR_NAME}.azurecr.io/${POSTGRES_IMAGE}:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 1.5
      environmentVariables:
      - name: POSTGRES_USER
        value: "airflow"
      - name: POSTGRES_PASSWORD
        value: "airflow"
      - name: POSTGRES_DB
        value: "airflow"
      ports:
      - port: 5432
  osType: Linux
  ipAddress:
    type: Public
    dnsNameLabel: ${DNS_LABEL}
    ports:
    - protocol: tcp
      port: 8080
  imageRegistryCredentials:
  - server: ${ACR_NAME}.azurecr.io
    username: ${REGISTRY_USERNAME}
    password: ${REGISTRY_PASSWORD}
EOF

# Déploiement
echo "Déploiement sur Azure Container Instances..."
az container create --resource-group $RESOURCE_GROUP --file aci-deploy.yaml

# Résultat
CONTAINER_FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_GROUP_NAME --query "ipAddress.fqdn" -o tsv)
echo "✅ Airflow déployé ! Accédez au webserver : http://${CONTAINER_FQDN}:8080"
